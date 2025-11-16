#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量清洗先知社区 Markdown 头尾冗余内容
头：从“来源:”到“[登录]...”的一整段
尾：从“[...人收藏]”开始到文件结尾的一整段
用法：python clean_xianzhi.py
"""

import re
import glob
import shutil
import os

# 头尾正则（re.DOTALL 让 . 匹配换行）
HEAD_RE = re.compile(r'来源: https://xz\.aliyun\.com/news/\d+[\s\S]*?\d+浏览 · \d{4}-\d{2}-\d{2} \d{2}:\d{2}\n')
FOOT_RE = re.compile(r'\[0 人收藏\][\s\S]*', re.MULTILINE)

def clean_file(path):
    with open(path, encoding='utf-8') as f:
        text = f.read()

    # 去头
    text = HEAD_RE.sub('', text, count=1)
    # 去尾
    text = FOOT_RE.sub('', text, count=1)

    # 备份
    #shutil.move(path, path + '.bak')
    # 写新文件
    with open(path, 'w', encoding='utf-8') as f:
        f.write(text.strip() + '\n')
    print(f'[+] cleaned -> {path}')

def main():
    for fp in glob.glob('*.md'):
        # 跳过已备份文件
        #if fp.endswith('.bak'):
            #continue
        clean_file(fp)

if __name__ == '__main__':
    main()