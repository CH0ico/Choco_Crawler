#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
先知道（xz.aliyun.com）文章批量爬 → Markdown + 本地图片
并发加速版（线程池 + 每线程独立driver），可 Ctrl-C 安全退出
"""

import os
import time
import random
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import markdownify

# -------------------- 配置全局变量 --------------------
# 网站配置
BASE_URL = "https://forum.butian.net"
ARTICLE_URL_TEMPLATE = f"{BASE_URL}/article/{{}}"

# 爬取配置(id范围)
START_ID = 1
END_ID = 5
CREATE_DRIVER_COOLDOWN = 4      # 创建浏览器实例的时间间隔，可自行微调, 太小容易503
WORKERS = 1                    # 线程池大小，可根据实际情况调整

# 文件保存路径
SAVE_DIR = "G:/exps/butian2"

# -------------------- 全局锁 / 会话 --------------------
print_lock = threading.Lock()
file_lock  = threading.Lock()

sess = requests.Session()
retries = Retry(total=3, backoff_factor=0.3, status_forcelist=[500, 502, 503, 504])
sess.mount("http://",  HTTPAdapter(max_retries=retries))
sess.mount("https://", HTTPAdapter(max_retries=retries))

# -------------------- 线程局部存储：每个线程独享一个 driver
thread_local = threading.local()



def get_driver():
    """返回当前线程的独立浏览器实例（带创建冷却）"""
    if not hasattr(thread_local, "driver"):
        driver_path = r"G:\\SecTools\\Crawler\\chromedriver\\chromedriver.exe"
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--ignore-certificate-errors")
        # 如要无头，再加 chrome_options.add_argument("--headless=new")
        thread_local.driver = webdriver.Chrome(
            service=Service(driver_path), options=chrome_options
        )
        # ===== 关键：创建后先睡 =====
        time.sleep(CREATE_DRIVER_COOLDOWN)
    return thread_local.driver

# -------------------- 工具函数 --------------------
def filename_filter(filename: str) -> str:
    for ch in r'\/:*?"<>|':
        filename = filename.replace(ch, " ")
    return filename

# -------------------- 单个任务 --------------------
def crawl_one(i: int) -> str:
    """单篇文章抓取"""
    try:
        id_ = str(i)
        url = ARTICLE_URL_TEMPLATE.format(id_)

        # 1. 先拿到 driver（已内置冷却）
        driver = get_driver()

        # 2. 访问前再 human-like 随机睡 0~2 秒
        time.sleep(random.uniform(0, 2))

        with print_lock:
            print(url)
        driver.get(url)
        headers = {
            "Referer": BASE_URL + "/",
            # 下面 Cookie 请换成自己有效 Cookie，太长已折叠
            # "Cookie": "customer_timezone=8; arms_uid=de74db3f-a544-4abf-9709-11b8479fbca4; ..."
        }

        soup = BeautifulSoup(driver.page_source, "html.parser")

        # 1. 标题
        title_tag = soup.find("title")
        title_text = title_tag.text if title_tag else None
        article_title = soup.find("h1", class_="article-title")
        if article_title:
            title_text = article_title.text.strip()

        if not title_text or "400 -" in title_text:
            return f"{id_} 跳过（无标题或404）"

        # 2. 文件名、目录
        f_name = filename_filter(title_text)
        md_path = f"{SAVE_DIR}/{id_}-{f_name}.md"
        with file_lock:
            os.makedirs(f"{SAVE_DIR}/images", exist_ok=True)

        # 3. 找正文容器
        article_content = None
        for container in [
            soup.find("div", class_="article-content"),
            soup.find("div", class_="content"),
            soup.find("article"),
            soup.find("div", id="content"),
            soup.find("div", class_="article-body"),
        ]:
            if container:
                article_content = container
                break
        if not article_content:
            article_content = soup.body or soup

        # 4. 下载图片
        img_tags = article_content.find_all("img")
        for img in img_tags:
            try:
                img_url = img.get("src", "").strip()
                if not img_url:
                    continue
                if not img_url.startswith(("http://", "https://")):
                    img_url = BASE_URL + img_url
                img_name = f"{id_}_{os.path.basename(img_url)}"
                img_data = sess.get(img_url, headers=headers, timeout=10).content
                with open(f"{SAVE_DIR}/images/{img_name}", "wb") as f_img:
                    f_img.write(img_data)
            except Exception as img_e:
                with print_lock:
                    print(f"{id_} 下载图片失败: {img_e}")

        # 5. 转 Markdown + 替换图片路径
        md_content = markdownify.markdownify(str(article_content), heading_style="ATX")
        for img in img_tags:
            try:
                img_url = img.get("src", "")
                if not img_url:
                    continue
                if not img_url.startswith(("http://", "https://")):
                    img_url = BASE_URL + img_url
                new_name = f"{id_}_{os.path.basename(img_url)}"
                md_content = md_content.replace(img_url, f"images/{new_name}")
            except Exception as img_e:
                with print_lock:
                    print(f"{id_} 替换图片路径失败: {img_e}")

        # 6. 写文件
        md_full = f"# {title_text}\n\n来源: {url}\n\n{md_content}"
        with file_lock:
            with open(md_path, "w", encoding="utf-8") as f:
                f.write(md_full)
        return f"{id_} 成功 -> {md_path}"

    except Exception as e:
        return f"{i} 异常: {e}"
    finally:
        time.sleep(1)   # 保持原有节奏，防止瞬间过高并发

# -------------------- 主入口 --------------------
if __name__ == "__main__":
    try:
        workers = WORKERS
        with ThreadPoolExecutor(max_workers=workers) as pool:
            futures = [pool.submit(crawl_one, i) for i in range(START_ID, END_ID)]
            for fu in as_completed(futures):
                with print_lock:
                    print(fu.result())
    except KeyboardInterrupt:
        with print_lock:
            print("\n收到 Ctrl-C，正在终止任务……")
        pool.shutdown(wait=False)   # 立即停掉线程池
    finally:
        # 关闭所有线程里的浏览器
        if hasattr(thread_local, "driver"):
            thread_local.driver.quit()