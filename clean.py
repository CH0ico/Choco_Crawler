#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量清洗先知社区 Markdown 头尾冗余内容
头：从"来源:"到"[登录]..."的一整段
尾：从"[...人收藏]"开始到文件结尾的一整段
用法python clean.py
新增功能：
1. 删除 G:/exps/xianzhi 中 *--.先知社区.md 文件
2. 删除 G:/exps/xianzhi/images 中特定图片文件
"""

import re
import glob
import shutil
import os

# 全局配置 - 方便修改管理
XIANZHI_DIR = 'G:/exps/xianzhi'  # 先知社区文件目录（使用正斜杠避免转义问题）

# 头尾正则（re.DOTALL 让 . 匹配换行）
# 修改后的正则表达式，以匹配用户提供的实际格式
HEAD_RE = re.compile(r'来源: https://xz\.aliyun\.com/news/\d+[\s\S]*?\d+浏览[\s\S]*?发表于[\s\S]*?\d+浏览.*?\n', re.DOTALL)
# 更宽松的尾部匹配
FOOT_RE = re.compile(r'\[\d* 人收藏\][\s\S]*', re.DOTALL)

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

def delete_specific_files():
    """删除指定目录下的特定文件"""
    # 1. 删除特定格式的 Markdown 文件
    if os.path.exists(XIANZHI_DIR):
        print(f"[+] 检查目录: {XIANZHI_DIR}")
        # 使用更宽松的模式匹配
        pattern = os.path.join(XIANZHI_DIR, '*--*.md')
        matching_files = glob.glob(pattern)
        
        if not matching_files:
            print(f"[-] 没有找到匹配 '*--*.md' 的文件")
            # 显示目录中的所有文件，以便调试
            # all_files = os.listdir(xianzhi_dir)
            # md_files = [f for f in all_files if f.endswith('.md')]
            # if md_files:
            #     print(f"[*] 目录中的 .md 文件: {', '.join(md_files)}")
        else:
            print(f"[+] 找到 {len(matching_files)} 个匹配文件")
            for file_path in matching_files:
                # 确保文件名包含"先知社区"字符串
                if '先知社区' in os.path.basename(file_path):
                    try:
                        os.remove(file_path)
                        print(f'[+] deleted -> {file_path}')
                    except Exception as e:
                        print(f'[-] failed to delete {file_path}: {e}')
                else:
                    print(f'[-] 跳过（不包含"先知社区"）: {file_path}')
    else:
        print(f'[-] directory not found: {XIANZHI_DIR}')
    
    # 2. 删除特定格式的图片文件
    images_dir = os.path.join(XIANZHI_DIR, 'images')
    if os.path.exists(images_dir):
        print(f"[+] 检查图片目录: {images_dir}")
        
        # 删除 *_pic_default_secret.png 文件
        secret_files = glob.glob(os.path.join(images_dir, '*_pic_default_secret.png'))
        print(f"[+] 找到 {len(secret_files)} 个 secret 图片文件")
        for file_path in secret_files:
            try:
                os.remove(file_path)
                print(f'[+] deleted -> {file_path}')
            except Exception as e:
                print(f'[-] failed to delete {file_path}: {e}')
        
        # 删除 *_public 文件
        public_files = glob.glob(os.path.join(images_dir, '*_public'))
        print(f"[+] 找到 {len(public_files)} 个 public 文件")
        for file_path in public_files:
            try:
                os.remove(file_path)
                print(f'[+] deleted -> {file_path}')
            except Exception as e:
                print(f'[-] failed to delete {file_path}: {e}')
        
        # 删除所有 .svg 文件
        svg_files = glob.glob(os.path.join(images_dir, '*.svg'))
        print(f"[+] 找到 {len(svg_files)} 个 svg 文件")
        for file_path in svg_files:
            try:
                os.remove(file_path)
                print(f'[+] deleted -> {file_path}')
            except Exception as e:
                print(f'[-] failed to delete {file_path}: {e}')
    else:
        print(f'[-] 图片目录不存在: {images_dir}')

def main():
    print("开始清理 Markdown 文件...")
    # 清理当前目录下的 markdown 文件
    md_files = glob.glob('*.md')
    if not md_files:
        print("[-] 当前目录没有找到 .md 文件")
    else:
        print(f"[+] 找到 {len(md_files)} 个 .md 文件")
        for fp in md_files:
            # 跳过已备份文件
            #if fp.endswith('.bak'):
                #continue
            clean_file(fp)
    
    print("\n开始删除特定文件...")
    # 删除特定目录下的文件
    delete_specific_files()
    print("\n所有操作完成！")

if __name__ == '__main__':
    main()