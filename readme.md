# ChocoCrawler

轻量级爬虫工具，用于将「先知（XZ）社区」文章批量保存为本地 Markdown，并自动下载配图，方便离线阅读与知识归档。

---

## 功能亮点
- ✅ 自动遍历指定文章 ID 区间，生成 `.md` 文件  
- ✅ 正文、标题智能提取，支持多级「内容容器」匹配  
- ✅ 图片自动下载到本地 `images/` 目录，并修正引用路径  
- ✅ 内置 `clean.py`，一键去除页头页尾冗余信息（登录提示、收藏数等）  
- ✅ 断点友好：已爬文件不会重复覆盖，可随时终止后继续  

---

## 目录结构（推荐）

ChocoCrawler-XZ/
├─ ChocoCrawler.py   # 主爬虫脚本
├─ clean.py          # 清洗冗余头尾
├─ chromedriver.exe  # Chrome 驱动（需自己下载并放于此）
├─ README.md         # 本文档
└─ xianzhi/          # 运行后自动生成
   ├─ images/        # 文章配图

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

### 4. 清洗冗余信息
爬完后执行
```bash
python clean.py
```
即可批量去除每篇文章头部的「来源：…浏览 · 时间」与尾部的「[0 人收藏]…」等无用段落。

---

## 手动清理空白/无效文章
先知平台存在大量无效路径，爬虫会生成空白或仅含标题的 `.md` 文件，请**自行批量删除**：

### PowerShell（Windows）
```powershell
# 删除文件名中包含「先知社区」的空白文章
Remove-Item *`--先知社区.md
# 或按大小过滤（例如 < 1 KB）
Get-ChildItem *.md | Where-Object { $_.Length -lt 1KB } | Remove-Item
```

### Bash（macOS / Linux）
```bash
# 删除文件名中包含「先知社区」的空白文章
rm *--先知社区.md
# 或按大小过滤（例如 < 1 KB）
find . -name "*.md" -size -1k -delete
```

---

## 自定义配置
| 配置项       | 所在文件          | 说明                                |
| ------------ | ----------------- | ----------------------------------- |
| 文章 ID 区间 | `ChocoCrawler.py` | 修改 `for i in range(start, end)`   |
| 保存路径     | `ChocoCrawler.py` | 修改 `filename = "./xianzhi/..."`   |
| 头尾正则     | `clean.py`        | 自行调整 `HEAD_RE` / `FOOT_RE` 模式 |

---

## 免责声明
本工具仅供个人学习、研究与备份资料之用。  
请遵守先知社区 [《用户协议》](https://xz.aliyun.com/protocol) 与相关法律法规，**勿进行高频、大规模抓取或商业用途**，否则后果自负。

---

## 更新日志
| 日期    | 版本 | 说明                                         |
| ------- | ---- | -------------------------------------------- |
| 2025-11 | v1.1 | 补充 ChromeDriver 安装步骤与空白文章清理示例 |

---

如果对你有帮助，记得点个 ⭐ 哦！