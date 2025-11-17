# ChocoCrawler

轻量级爬虫工具，用于将「先知（XZ）社区」或「补天（Butian）社区」文章批量保存为本地 Markdown，并自动下载配图，方便离线阅读与知识归档。

---

## 功能亮点
- ✅ 自动遍历指定文章 ID 区间，生成 `.md` 文件  
- ✅ 正文、标题智能提取，支持多级「内容容器」匹配  
- ✅ 图片自动下载到本地 `images/` 目录，并修正引用路径  
- ✅ 内置 `clean.py & clean_file.py`，一键去除页头页尾冗余信息（登录提示、收藏数等）  
- ✅ 断点友好：已爬文件不会重复覆盖，可随时终止后继续  

---

## 目录结构（推荐）

```
ChocoCrawler/
├─ ChocoCrawler.py   # 主爬虫脚本
├─ clean.py          # 清洗多余图片文件和失效页面
├─ chromedriver.exe  # Chrome 驱动（需自己下载并放于此）
├─ README.md         # 本文档
└─ xianzhi/          # 运行后自动生成
   ├─ images/        # 文章配图
   ├─ *.md
   └─ clean_file.py     # 清洗单文件冗余头尾信息 (注意：手动放置在 xianzhi/ 目录下)
```



## 快速开始

### 1. 安装依赖

```
# 建议使用 Python ≥ 3.8
pip install selenium==4.15.0 beautifulsoup4 markdownify requests
```

1. 安装 ChromeDriver（务必完成）
2. 查看本地 Chrome 版本：  
   地址栏输入 `chrome://version/`  
3. 前往 [ChromeDriver 官网](https://chromedriver.chromium.org/downloads) 下载**与 Chrome 大版本一致**的驱动  
4. 将解压后的 `chromedriver.exe` 放到本项目根目录（即与 `ChocoCrawler.py` 同级）  

> ⚠️ 若路径或版本不一致，脚本会抛出 `WebDriverException`！

### 3. 运行爬虫
```bash
python ChocoCrawler.py
```
- 默认 ID 区间 `15079–20000`，可在脚本内修改 `range(15079, 20000)`  
- 每篇间隔 5 s，降低封禁风险；如需提速请自行权衡  

### 4. 清洗冗余信息(针对先知社区)
爬完后执行
```bash
python clean.py
```
即可批量去除每篇文章头部与尾部的冗余
