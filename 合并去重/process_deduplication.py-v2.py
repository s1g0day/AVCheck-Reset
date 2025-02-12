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
import os
import logging
from datetime import datetime
from typing import Dict, List

def ensure_directories() -> None:
    """确保必要的目录存在"""
    directories = ['logs', 'output']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            logging.info(f"创建目录: {directory}")

def setup_logging(timestamp: str) -> None:
    """设置日志配置"""
    # 确保目录存在
    ensure_directories()
    
    # 配置日志
    timestamp = timestamp.split('_')[0]
    log_file = f'logs/process_{timestamp}.log'
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file, encoding='utf-8'),
            logging.StreamHandler()
        ]
    )

def get_file_name_without_ext(file_path: str) -> str:
    """获取文件名（不含扩展名）"""
    return os.path.splitext(os.path.basename(file_path))[0]

def process_file(input_file: str = "avlist.txt") -> None:
    """处理文件的主函数"""
    # 获取时间戳并设置日志
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    setup_logging(timestamp)
    
    # 定义常量
    # priority_keywords = [
    #     "防病毒", "杀毒", "antivirus", "anti-virus", "防护", "agent",
    #     "监控", "monitor", "安全", "security", "防御", "defense",
    #     "检测", "detection", "EDR", "edr", "XDR", "xdr"
    # ]
    # 定义常量
    priority_keywords = [
        "已知杀软进程名称暂未收录",
        "已知杀软进程,名称暂未收录",
        "疑似杀软进程"
    ]
    
     # 生成输出文件名（包含时间戳和输入文件名）
    input_name = get_file_name_without_ext(input_file)
    sorted_output = os.path.join('output', f"{timestamp}_{input_name}_sorted.txt")
    final_output = os.path.join('output', f"{timestamp}_{input_name}_quchong.txt")
    
    logging.info(f"开始处理文件: {input_file}")
    
    try:
        # 读取文件
        with open(input_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
        logging.info(f"成功读取输入文件，共 {len(lines)} 行")
        
        # 按进程名分组
        groups = group_by_process(lines)
        logging.info(f"进程分组完成，共 {len(groups)} 个不同的进程")
        
        # 写入排序后的文件
        with open(sorted_output, "w", encoding="utf-8") as f:
            for process_name in sorted(groups.keys()):
                for line in groups[process_name]:
                    f.write(line)
        logging.info(f"已将排序结果写入文件: {sorted_output}")
        
        # 处理优先级并写入最终文件
        result = process_by_priority(groups, priority_keywords)
        with open(final_output, "w", encoding="utf-8") as f:
            for line in result.values():
                f.write(line)
        logging.info(f"已将去重结果写入文件: {final_output}")
        
    except Exception as e:
        logging.error(f"处理过程中发生错误: {str(e)}")
        raise

def group_by_process(lines: List[str]) -> Dict[str, List[str]]:
    """按进程名分组"""
    groups = {}
    for line in lines:
        if not line.strip():
            continue
        process_name = line.split(':')[0].strip('"').lower()
        groups.setdefault(process_name, []).append(line)
    return groups

def process_by_priority(groups: Dict[str, List[str]], priority_keywords: List[str]) -> Dict[str, str]:
    """根据优先级处理重复的进程名（保持小写排序）"""
    result = {}
    duplicate_count = 0
    
    for process_name in sorted(groups.keys()):
        lines = groups[process_name]
        if len(lines) > 1:
            duplicate_count += 1
            # 先过滤掉包含关键词的行
            clean_lines = [line for line in lines if not any(keyword in line.lower() for keyword in priority_keywords)]
            
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
    
    logging.info(f"处理完成，共发现 {duplicate_count} 个重复进程")
    return result

def main():
    """主函数"""
    process_file()

if __name__ == "__main__":
    main()
