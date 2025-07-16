#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
运行所有实验的脚本
这个脚本会按顺序运行所有实验，包括：
1. 生成数据集
2. 运行实验1-5（通过simulation.py）
3. 运行实验6（故障容错测试）
4. 分析所有实验结果
"""

import os
import sys
import time
import subprocess
import logging
from datetime import datetime

# 设置日志
LOG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'log'))
os.makedirs(LOG_DIR, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, f'run_all_experiments_{timestamp}.log')),
        logging.StreamHandler()
    ]
)

# 项目根目录
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def run_command(cmd, cwd=ROOT_DIR):
    """运行命令并返回结果"""
    logging.info(f"运行命令: {cmd}")
    try:
        result = subprocess.run(
            cmd, 
            cwd=cwd, 
            shell=True, 
            check=True,
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True
        )
        logging.info(f"命令成功完成: {cmd}")
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        logging.error(f"命令执行失败: {cmd}")
        logging.error(f"错误输出: {e.stderr}")
        return False, e.stderr

def check_hardhat_running():
    """检查Hardhat节点是否在运行"""
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect(("localhost", 8545))
        s.close()
        return True
    except:
        s.close()
        return False

def main():
    """主函数，按顺序运行所有实验"""
    logging.info("====== 开始运行所有实验 ======")
    
    # 步骤1: 生成数据集
    logging.info("步骤1: 生成证书数据集")
    success, output = run_command("python scripts/generate_dataset.py")
    if not success:
        logging.error("数据集生成失败，终止实验")
        return
    
    # 步骤2: 检查Hardhat节点是否在运行，如果没有则启动
    logging.info("步骤2: 检查Hardhat节点")
    if not check_hardhat_running():
        logging.info("Hardhat节点未运行，正在启动...")
        # 启动Hardhat节点作为后台进程
        hardhat_process = subprocess.Popen(
            "npx hardhat node", 
            shell=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            cwd=ROOT_DIR
        )
        # 等待Hardhat节点启动
        time.sleep(10)
        if not check_hardhat_running():
            logging.error("Hardhat节点启动失败，终止实验")
            return
        logging.info("Hardhat节点已成功启动")
    else:
        logging.info("Hardhat节点已在运行")
    
    # 步骤3: 运行实验1-5
    logging.info("步骤3: 运行实验1-5")
    success, output = run_command("python scripts/simulation.py")
    if not success:
        logging.error("实验1-5运行失败，继续运行其他实验")
    
    # 步骤4: 运行实验6（故障容错测试）
    logging.info("步骤4: 运行实验6（故障容错测试）")
    # 先停止之前的Hardhat节点（如果我们启动了的话）
    if 'hardhat_process' in locals():
        hardhat_process.terminate()
        time.sleep(5)
    
    # 运行故障容错测试
    success, output = run_command("python scripts/run_fault_test.py")
    if not success:
        logging.error("实验6运行失败，继续运行分析")
    
    # 步骤5: 分析所有实验结果
    logging.info("步骤5: 分析所有实验结果")
    # 分析实验1-5的结果
    success, output = run_command("python scripts/analyze_results.py")
    if not success:
        logging.error("实验1-5分析失败")
    
    # 分析实验6的结果
    success, output = run_command("python scripts/analyze_fault_tolerance.py")
    if not success:
        logging.error("实验6分析失败")
    
    logging.info("====== 所有实验运行完成 ======")
    logging.info("请查看 data/ 目录和 analysis/ 目录获取实验结果和分析")

if __name__ == "__main__":
    main()
