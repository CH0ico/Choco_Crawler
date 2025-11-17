#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量处理补天社区 Markdown 文件
功能：删除包含"404 Not Found"的失效页面文件
用法：python clean_bt.py
"""

import os
import re
import glob

# 全局配置 - 方便修改管理
BUTIAN_DIR = 'G:/exps/butian'  # 补天社区文件目录（使用正斜杠避免转义问题）

def main():
    """主函数：批量删除包含404的失效文件"""
    print(f"开始清理 {BUTIAN_DIR} 目录中的404文件...")
    
    # 获取目录中所有md文件
    md_files = glob.glob(os.path.join(BUTIAN_DIR, '*.md'))
    deleted_count = 0
    
    for md_file in md_files:
        # 检查文件名是否包含"404 Not Found"
        if "404 Not Found" in os.path.basename(md_file):
            try:
                os.remove(md_file)
                print(f"已删除: {os.path.basename(md_file)}")
                deleted_count += 1
            except Exception as e:
                print(f"删除失败 {os.path.basename(md_file)}: {str(e)}")
    
    print(f"清理完成！共删除 {deleted_count} 个404文件。")

if __name__ == '__main__':
    main()