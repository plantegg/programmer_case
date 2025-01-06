#! /usr/bin/python3

"""
每秒读取一次 /proc/net/netstat 文件的内容
比较相邻两次读取的差异
只显示发生变化的项目
显示以下信息：
指标名称
当前值
变化量（与上次的差值）
变化率（百分比）
保存并显示最近5次的变化历史
使用清屏功能使
"""

import time
from collections import defaultdict
import os

def read_netstat():
    """读取 /proc/net/netstat 文件内容并解析"""
    stats = {}
    try:
        with open('/proc/net/netstat', 'r') as f:
            lines = f.readlines()
            
        # 每两行为一组，第一行是标签行，第二行是值行
        for i in range(0, len(lines), 2):
            header = lines[i].strip().split()
            values = lines[i+1].strip().split()
            
            # 确保标签行和值行的第一列匹配
            if header[0] != values[0]:
                continue
                
            # 将标签和对应的值组合成字典
            for j in range(1, len(header)):
                key = f"{header[0]}{header[j]}"
                stats[key] = int(values[j])
                
    except Exception as e:
        print(f"Error reading netstat: {e}")
        return None
        
    return stats

def main():
    # 存储上一次的数据
    last_stats = None
    
    # 存储变化的历史记录
    changes_history = defaultdict(list)
    
    try:
        while True:
            # 清屏（Unix/Linux系统）
            os.system('clear')
            
            # 读取当前数据
            current_stats = read_netstat()
            
            if current_stats and last_stats:
                print("\n变化项：")
                print("-" * 80)
                print(f"{'指标名称':<40} {'当前值':<15} {'变化量':<15} {'变化率'}")
                print("-" * 80)
                
                # 比较并显示变化
                for key in current_stats:
                    current_value = current_stats[key]
                    last_value = last_stats[key]
                    
                    if current_value != last_value:
                        change = current_value - last_value
                        change_rate = (change / last_value * 100) if last_value != 0 else float('inf')
                        
                        # 记录变化
                        changes_history[key].append(change)
                        # 只保留最近5次变化
                        if len(changes_history[key]) > 8:
                            changes_history[key].pop(0)
                            
                        print(f"{key:<40} {current_value:<15} {change:<15} {change_rate:.2f}%")
                
                # 显示变化趋势
                print("\n最近变化趋势（最近8次变化）：")
                print("-" * 80)
                for key, changes in changes_history.items():
                    if changes:  # 只显示有变化的项
                        changes_str = " -> ".join(map(str, changes))
                        print(f"{key:<40} {changes_str}")
                
            last_stats = current_stats
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("\n监控已停止")

if __name__ == "__main__":
    main()

