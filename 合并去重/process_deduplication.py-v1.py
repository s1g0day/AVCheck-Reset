#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
杀软进程列表去重工具

功能描述：
    1. 读取杀软进程列表文件(avlist.txt)
    2. 对数据进行去重和排序处理
    3. 生成两个结果文件：
       - sorted.txt: 完全去重并按进程名排序
       - quchong.txt: 按进程名去重(考虑优先级)并排序

输入文件格式：
    "进程名":"描述"
    例如: "safedogsiteiis.exe":"网站安全狗(iis)"

处理规则：
    1. 所有排序基于进程名转小写后的结果
    2. 当同一进程存在多个描述时，优先选择不包含以下关键词的描述：
       - "已知杀软进程名称暂未收录"
       - "已知杀软进程,名称暂未收录"
       - "疑似杀软进程"

作者：s1g0day
创建日期：2025-02-11
最后修改：2025-02-11
版本：1.0.0
"""
import logging
from datetime import datetime
from typing import List, Dict, Tuple

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 获取当前时间戳
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# 定义常量
INPUT_FILE = "avlist.txt"
SORTED_OUTPUT = f"output/{timestamp}_avlist_sorted.txt"
FINAL_OUTPUT = f"output/{timestamp}_avlist_quchong.txt"
PRIORITY_KEYWORDS = [
    "已知杀软进程名称暂未收录",
    "已知杀软进程,名称暂未收录",
    "疑似杀软进程"
]

def read_av_list(file_path: str) -> List[str]:
    """
    读取杀软列表文件。

    Args:
        file_path (str): 输入文件路径

    Returns:
        List[str]: 文件内容行列表

    Raises:
        Exception: 文件读取错误时记录到日志
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.readlines()
    except Exception as e:
        logging.error(f"读取文件失败: {e}")
        return []

def parse_process_line(line: str) -> Tuple[str, str]:
    """
    解析每行数据，提取进程名并转换为小写。

    Args:
        line (str): 输入行，格式为 "进程名":"描述"

    Returns:
        Tuple[str, str]: (小写进程名, 原始行)
    """
    process_name = line.strip().replace(',','').split(':')[0]
    return process_name.lower(), line  # 转换为小写

def group_by_process_name(lines: List[str]) -> Dict[str, List[str]]:
    """
    按进程名分组，使用小写进程名作为键。

    Args:
        lines (List[str]): 输入行列表

    Returns:
        Dict[str, List[str]]: 以小写进程名为键，原始行列表为值的字典
    """
    groups = {}
    for line in lines:
        process_name_lower, original_line = parse_process_line(line)
        if process_name_lower not in groups:
            groups[process_name_lower] = []
        groups[process_name_lower].append(original_line)
    return groups

def write_sorted_unique(groups: Dict[str, List[str]], output_file: str) -> None:
    """写入去重并按进程名（小写）排序后的文件"""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            # 使用小写进程名排序
            for process_name in sorted(groups.keys()):
                for line in groups[process_name]:
                    f.write(line)
        logging.info(f"成功写入文件: {output_file}")
    except Exception as e:
        logging.error(f"写入文件失败: {e}")

def select_priority_line(lines: List[str]) -> str:
    """
    根据优先级规则选择要保留的行。

    优先级规则：
    1. 优先选择不包含特定关键词的描述
    2. 如果所有描述都包含关键词，选择第一个描述

    Args:
        lines (List[str]): 同一进程名的所有行

    Returns:
        str: 选中的行
    """
    # 检查是否有不含关键词的行
    clean_lines = [line for line in lines if not any(keyword in line for keyword in PRIORITY_KEYWORDS)]
    
    # 如果有不含关键词的行，返回第一个
    if clean_lines:
        return clean_lines[0]
    # 如果所有行都含关键词，返回第一行
    return lines[0]

def process_by_priority(groups: Dict[str, List[str]]) -> Dict[str, str]:
    """根据优先级处理重复的进程名（保持小写排序）"""
    result = {}
    for process_name in sorted(groups.keys()):
        lines = groups[process_name]
        if len(lines) > 1:
            # 先过滤掉包含关键词的行
            clean_lines = [line for line in lines if not any(keyword in line for keyword in PRIORITY_KEYWORDS)]
            
            if len(clean_lines) > 1:
                # 如果还有多个描述，将它们合并成列表格式
                descriptions = []
                for line in clean_lines:
                    # 提取描述部分（第二个引号内的内容）
                    parts = line.split(':', 1)
                    if len(parts) == 2:
                        desc = parts[1].strip().strip('"')
                        if desc:  # 确保描述不为空
                            # 去除描述中可能存在的多余逗号
                            desc = desc.replace('",', '').replace(',"', '')
                            descriptions.append(f'"{desc}"')  # 给每个描述加上引号
                
                # 构建新格式的行："进程名":["描述1","描述2",...]
                process = clean_lines[0].split(':', 1)[0].strip()
                # 使用join直接连接，避免多余逗号
                result[process_name] = f'{process}:[{",".join(descriptions)}]\n'
            elif len(clean_lines) == 1:
                # 处理单行情况，确保格式正确
                line = clean_lines[0].strip()
                if line.count('"') == 2:  # 简单格式："进程名":"描述"
                    result[process_name] = line + '\n'
                else:  # 复杂格式，需要清理
                    parts = line.split(':', 1)
                    if len(parts) == 2:
                        desc = parts[1].strip().strip('"')
                        desc = desc.replace('",', '').replace(',"', '')
                        result[process_name] = f'{parts[0].strip()}:"{desc}"\n'
            else:
                # 如果没有干净的行，使用原始行中的第一个
                line = lines[0].strip()
                if line.count('"') == 2:  # 简单格式
                    result[process_name] = line + '\n'
                else:  # 复杂格式，需要清理
                    parts = line.split(':', 1)
                    if len(parts) == 2:
                        desc = parts[1].strip().strip('"')
                        desc = desc.replace('",', '').replace(',"', '')
                        result[process_name] = f'{parts[0].strip()}:"{desc}"\n'
        else:
            # 处理单行情况
            line = lines[0].strip()
            if line.count('"') == 2:  # 简单格式
                result[process_name] = line + '\n'
            else:  # 复杂格式，需要清理
                parts = line.split(':', 1)
                if len(parts) == 2:
                    desc = parts[1].strip().strip('"')
                    desc = desc.replace('",', '').replace(',"', '')
                    result[process_name] = f'{parts[0].strip()}:"{desc}"\n'
    return result

def write_final_result(result: Dict[str, str], output_file: str) -> None:
    """写入最终结果（按小写进程名排序）"""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for process_name in sorted(result.keys()):  # 按小写进程名排序
                f.write(result[process_name])
        logging.info(f"成功写入文件: {output_file}")
    except Exception as e:
        logging.error(f"写入文件失败: {e}")

def print_statistics(original: List[str], groups: Dict[str, List[str]], final: Dict[str, str]) -> None:
    """打印统计信息"""
    print("\n统计信息:")
    print(f"原始行数: {len(original)}")
    print(f"去重并排序后行数: {sum(len(lines) for lines in groups.values())}")
    print(f"进程名去重后行数: {len(final)}")
    print(f"不同进程数: {len(groups)}")

def main():
    """
    主函数，执行以下步骤：
    1. 读取输入文件
    2. 去重并按进程名（小写）排序
    3. 根据优先级规则处理重复进程
    4. 输出结果文件和统计信息
    """
    
    
    # 1. 读取文件
    av_list = read_av_list(INPUT_FILE)
    if not av_list:
        return

    # 2. 去重并按进程名（小写）排序
    process_groups = group_by_process_name(list(dict.fromkeys(av_list)))
    write_sorted_unique(process_groups, SORTED_OUTPUT)

    # 3. 根据优先级规则处理
    final_result = process_by_priority(process_groups)
    write_final_result(final_result, FINAL_OUTPUT)

    # 4. 打印统计信息
    print_statistics(av_list, process_groups, final_result)

if __name__ == "__main__":
    main()
