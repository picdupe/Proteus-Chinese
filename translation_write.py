#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import sys

# ========== 在这里配置输入输出文件 ==========
source_file = 'qt_zh_CN_translated.ts'  # 源文件（包含中文翻译）
target_file = 'qt_zh_CN.ts'       # 目标文件（需要填充空翻译）
output_file = 'qt_zh_CN_filled.ts' # 输出文件（填充后的新文件）
# =========================================

def parse_ts_file_regex(filename):
    """使用正则表达式解析.ts文件"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        source_trans_map = {}
        
        # 匹配所有message块（非贪婪模式）
        message_pattern = re.compile(r'<message>(.*?)</message>', re.DOTALL)
        
        for message in message_pattern.finditer(content):
            message_text = message.group(1)
            
            # 提取source
            source_match = re.search(r'<source>(.*?)</source>', message_text, re.DOTALL)
            # 提取translation
            translation_match = re.search(r'<translation>(.*?)</translation>', message_text, re.DOTALL)
            
            if source_match and translation_match:
                source_text = source_match.group(1).strip()
                translation_text = translation_match.group(1)
                
                # 检查是否有中文翻译
                if translation_text and contains_chinese(translation_text):
                    if source_text not in source_trans_map:
                        source_trans_map[source_text] = translation_text
                        print(f"找到翻译: {source_text[:50]} -> {translation_text[:50]}")
        
        print(f"\n总共找到 {len(source_trans_map)} 个有中文翻译的条目")
        return source_trans_map
        
    except FileNotFoundError:
        print(f"文件未找到: {filename}")
        return {}
    except Exception as e:
        print(f"解析文件出错: {e}")
        return {}

def contains_chinese(text):
    """检查文本是否包含中文字符"""
    if not text:
        return False
    # 匹配中文字符（包括基本汉字和扩展）
    chinese_pattern = re.compile(r'[\u4e00-\u9fff\u3400-\u4dbf\uf900-\ufaff]')
    return bool(chinese_pattern.search(text))

def fill_empty_translations(target_filename, output_filename, source_map):
    """读取目标文件，填充空翻译标签，写入新文件"""
    try:
        # 读取目标文件内容
        with open(target_filename, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 找到所有message块并处理
        def replace_translation(match):
            message_text = match.group(1)
            
            # 提取source
            source_match = re.search(r'<source>(.*?)</source>', message_text, re.DOTALL)
            # 提取translation
            translation_match = re.search(r'<translation>(.*?)</translation>', message_text, re.DOTALL)
            
            if source_match and translation_match:
                source_content = source_match.group(1).strip()
                trans_content = translation_match.group(1)
                
                # 检查translation是否为空
                is_empty = (trans_content is None or trans_content.strip() == '')
                
                # 如果为空，且source在映射中
                if is_empty and source_content in source_map:
                    # 替换translation内容
                    new_message = message_text.replace(
                        f'<translation>{trans_content}</translation>',
                        f'<translation>{source_map[source_content]}</translation>'
                    )
                    print(f"填充翻译: {source_content[:50]} -> {source_map[source_content][:50]}")
                    return f'<message>{new_message}</message>'
            
            # 不需要修改，返回原内容
            return match.group(0)
        
        # 执行替换
        message_pattern = re.compile(r'<message>(.*?)</message>', re.DOTALL)
        new_content = message_pattern.sub(replace_translation, content)
        
        # 写入输出文件
        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"\n处理完成！输出文件: {output_filename}")
        
        # 统计填充数量
        filled_count = sum(1 for _ in re.finditer(r'<message>', content)) - sum(1 for _ in re.finditer(r'<message>', new_content))
        return True
        
    except FileNotFoundError:
        print(f"目标文件未找到: {target_filename}")
        return False
    except Exception as e:
        print(f"处理文件时出错: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("步骤1: 从源文件提取有中文翻译的条目...")
    print("-" * 50)
    translation_map = parse_ts_file_regex(source_file)
    
    if not translation_map:
        print("未找到有效的翻译数据")
        return
    
    print("\n步骤2: 填充目标文件中的空翻译标签并生成新文件...")
    print("-" * 50)
    fill_empty_translations(target_file, output_file, translation_map)
    
    print("\n完成!")

if __name__ == '__main__':
    main()