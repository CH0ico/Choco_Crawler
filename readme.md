# ChocoCrawler

轻量级爬虫工具，支持将「先知（XZ）社区」和「补天（Butian）社区」文章批量保存为本地 Markdown，并自动下载配图，方便离线阅读与知识归档。

---

## 功能亮点
- ✅ 支持先知和补天两个社区文章爬取  
- ✅ 自动遍历指定文章 ID 区间，生成 `.md` 文件  
- ✅ 正文、标题智能提取，支持多级「内容容器」匹配  
- ✅ 图片自动下载到本地 `images/` 目录，并修正引用路径  
- ✅ 内置 `clean_xz.py & clean_file.py`，一键去除页头页尾冗余信息（登录提示、收藏数等）  
- ✅ 断点友好：已爬文件不会重复覆盖，可随时终止后继续  
- ✅ 配置灵活：支持自定义爬取范围、保存路径和线程数

---

## 目录结构

```
ChocoCrawler/
├─ ChocoCrawler.py   # 主爬虫脚本（先知社区）
├─ clean_xz.py       # 清洗多余图片文件和失效页面（先知）
├─ clean_bt.py       # 清洗多余图片文件和失效页面（补天）
├─ clean_file.py     # 清洗单文件冗余头尾信息
├─ requirement.txt   # 依赖列表
├─ README.md         # 本文档
├─ butian/          # 补天文章保存目录（运行后自动生成）
└─ xianzhi/          # 先知文章保存目录（运行后自动生成）
   └─ images/        # 文章配图

```


## 快速开始

### 1. 安装依赖

```
# 建议使用 Python ≥ 3.8
pip install -r requirement.txt
# 或手动安装
pip install selenium==4.15.0 beautifulsoup4 markdownify requests
```

### 2. 安装 ChromeDriver（务必完成）
1. 查看本地 Chrome 版本：  
   地址栏输入 `chrome://version/`  
2. 前往 [ChromeDriver 官网](https://chromedriver.chromium.org/downloads) 下载**与 Chrome 大版本一致**的驱动  
3. 将解压后的 `chromedriver.exe` 放到爬虫脚本所在目录  

> ⚠️ 若路径或版本不一致，脚本会抛出 `WebDriverException`！

### 3. 运行先知社区爬虫
```bash
python ChocoCrawler.py
```
- 默认 ID 区间可在脚本内修改  
- 每篇间隔 5 s，降低封禁风险；如需提速请自行权衡  

### 4. 运行补天社区爬虫
```bash
cd ..
python ChocoCrawler.py
```
- 配置参数（爬取范围、保存路径、线程数等）已集中在脚本顶部的全局变量中，可直接修改  

### 5. 清洗冗余信息
爬完后执行
```bash
# 批量清洗
python clean_xz.py

# 清洗文件内容(需要同级目录)
python clean_file.py
```
即可去除文章头部与尾部的冗余信息
