#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
分别运行每个实验的脚本
这个脚本会单独运行每个实验，并捕获可能的错误
"""

import os
import sys
import time
import subprocess
import logging
import textwrap
from datetime import datetime

# 设置日志
LOG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'log'))
os.makedirs(LOG_DIR, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, f'run_experiments_separately_{timestamp}.log')),
        logging.StreamHandler()
    ]
)

# 项目根目录
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def run_command(cmd, cwd=ROOT_DIR, timeout=None):
    """运行命令并返回结果"""
    # 确保命令是列表形式，以便正确处理带空格的参数
    if isinstance(cmd, str):
        # 为了安全，我们只对非常简单的命令使用shell=True
        # 对于python脚本执行，最好使用列表形式
        pass

    logging.info(f"运行命令：{cmd} (CWD: {cwd})")
    try:
        result = subprocess.run(
            cmd, 
            cwd=cwd, 
            shell=isinstance(cmd, str),
            check=True,
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout
        )
        logging.info(f"命令成功完成：{cmd}")
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        logging.error(f"命令执行失败：{cmd}")
        logging.error(f"错误输出：{e.stderr}")
        return False, e.stderr
    except subprocess.TimeoutExpired as e:
        logging.error(f"命令执行超时：{cmd}")
        return False, "命令执行超时"

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

def create_temp_experiment_script(experiment_number, experiment_function_name, with_helper=False):
    """创建临时实验脚本

    Args:
        experiment_number: 实验编号
        experiment_function_name: 实验函数名称
        with_helper: 是否需要传递helper和合约工厂参数
    """
    
    # 根据实验编号生成特定的初始化和调用代码
    init_and_call_code = ""
    if with_helper:
        # 通用的初始化代码
        common_init = """
        from dotenv import load_dotenv
        from simulation import BlockchainHelper, DATASET_PATH
        import pandas as pd
        import asyncio

        load_dotenv()
        HARDHAT_RPC_URL = "http://localhost:8545"
        DEPLOYER_PRIVATE_KEY = os.getenv("PRIVATE_KEY")
        if not DEPLOYER_PRIVATE_KEY:
            logging.error("FATAL: PRIVATE_KEY not found in .env file. Please set it up.")
            sys.exit(1)
        
        helper = BlockchainHelper(HARDHAT_RPC_URL, DEPLOYER_PRIVATE_KEY)
        logging.info("Blockchain helper initialized.")
"""
        
        if experiment_number in [1, 2, 3]:
            init_and_call_code = common_init + f"""
        from simulation import CERTIFICATE_ARTIFACT_PATH
        import simulation

        logging.info("Loading dataset...")
        dataset = pd.read_csv(DATASET_PATH, nrows=10000)
        logging.info("Creating contract factory...")
        cert_factory = helper.get_contract_factory(CERTIFICATE_ARTIFACT_PATH)
        logging.info("Deploying contract...")
        contract, _ = helper.deploy_contract("Certificate_Exp123", cert_factory, helper.account.address)
        logging.info(f"Contract deployed at {{contract.address}}.")
        helper.authorize_institution(contract)
        logging.info("Institution authorized.")
        
        logging.info("Starting experiment function: {experiment_function_name}...")
        if {experiment_number == 2}:
            asyncio.run(simulation.{experiment_function_name}(helper, contract, dataset))
        else:
            simulation.{experiment_function_name}(helper, contract, dataset)
"""
        elif experiment_number == 4:
            init_and_call_code = common_init + f"""
        from simulation import CERTIFICATE_ARTIFACT_PATH, CERTIFICATE_ONCHAIN_ARTIFACT_PATH
        import simulation

        dataset = pd.read_csv(DATASET_PATH, nrows=1000)
        cert_factory = helper.get_contract_factory(CERTIFICATE_ARTIFACT_PATH)
        cert_onchain_factory = helper.get_contract_factory(CERTIFICATE_ONCHAIN_ARTIFACT_PATH)
        
        logging.info("Deploying contracts...")
        cert_contract, deploy_gas_hybrid = helper.deploy_contract("Certificate_Exp4", cert_factory, helper.account.address)
        cert_onchain_contract, deploy_gas_onchain = helper.deploy_contract("CertOnChain_Exp4", cert_onchain_factory, helper.account.address)
        logging.info(f"Contracts deployed at {{cert_contract.address}} and {{cert_onchain_contract.address}}.")

        logging.info("Starting experiment function: {experiment_function_name}...")
        simulation.{experiment_function_name}(helper, cert_contract, cert_onchain_contract, dataset, deploy_gas_hybrid, deploy_gas_onchain)
"""
        elif experiment_number == 5:
            init_and_call_code = common_init + f"""
        from simulation import CERTIFICATE_ARTIFACT_PATH, BASELINE_REVOCATION_ARTIFACT_PATH
        import simulation

        logging.info("Creating contract factories...")
        cert_factory = helper.get_contract_factory(CERTIFICATE_ARTIFACT_PATH)
        baseline_revocation_factory = helper.get_contract_factory(BASELINE_REVOCATION_ARTIFACT_PATH)
        logging.info("Contract factories created.")

        logging.info("Starting experiment function: {experiment_function_name}...")
        simulation.{experiment_function_name}(helper, cert_factory, baseline_revocation_factory)
"""
    else:
        init_and_call_code = f"{experiment_function_name}()"

    # 完整的临时脚本内容
    script_content = f"""
import tempfile
import time
import logging
import os
import sys
import subprocess
from datetime import datetime
import time

# Add project root to Python path
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Setup logging
LOG_DIR = os.path.join(ROOT_DIR, 'log')
os.makedirs(LOG_DIR, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
log_file = os.path.join(LOG_DIR, f'experiment{experiment_number}_{{timestamp}}.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

def main_logic():
{textwrap.indent(init_and_call_code, '    ')}

# --- 主逻辑 ---
if __name__ == '__main__':
    logging.info(f"====== 开始运行实验 {experiment_number} ======")
    logging.info(f"Log file: {{log_file}}")
    start_time = time.time()
    try:
        main_logic()
        end_time = time.time()
        logging.info(f"====== 实验 {experiment_number} 运行成功, 耗时: {{end_time - start_time:.2f}}s ======")
    except Exception as e:
        logging.error(f"实验 {experiment_number} 运行失败: {{e}}", exc_info=True)
        sys.exit(1)
"""
    temp_script_path = os.path.join(os.path.dirname(__file__), f'temp_exp{experiment_number}.py')
    with open(temp_script_path, 'w') as f:
        f.write(script_content)
    return temp_script_path

def run_experiment(experiment_number, experiment_name, experiment_function_name, with_helper=False):
    """通用实验运行函数"""
    logging.info(f"运行实验{experiment_number} - {experiment_name}")

    # 检查是函数名还是脚本文件
    if experiment_function_name.endswith('.py'):
        # 这是一个外部脚本，直接运行
        script_path = os.path.join(os.path.dirname(__file__), experiment_function_name)
        if not os.path.exists(script_path):
            logging.error(f"脚本文件未找到: {script_path}")
            return False
        
        logging.info(f"直接运行外部脚本: {script_path}")
        # 使用 run_command 函数来执行
        success, output = run_command(['python', script_path], cwd=os.path.dirname(script_path), timeout=1800)
        return success
    else:
        # 这是内部函数，创建并运行临时脚本
        temp_script_path = create_temp_experiment_script(experiment_number, experiment_function_name, with_helper)
        if not temp_script_path:
            return False
        
        scripts_dir = os.path.dirname(os.path.abspath(__file__))
        success, output = run_command(["python", os.path.basename(temp_script_path)], cwd=scripts_dir, timeout=1800)
        
        # 删除临时脚本
        if os.path.exists(temp_script_path):
            os.remove(temp_script_path)
            
        return success

def run_experiment_6():
    """运行实验6 - 节点故障恢复测试"""
    logging.info("运行实验6 - 节点故障恢复测试")
    # 运行实验6
    success, output = run_command(["python", os.path.join(ROOT_DIR, "scripts", "run_fault_test.py")], timeout=600)
    return success

def analyze_results():
    """分析所有实验结果"""
    logging.info("分析所有实验结果")
    # 分析实验1-5的结果
    success1, output1 = run_command(["python", "analyze_results.py"], cwd=os.path.join(ROOT_DIR, "scripts"), timeout=300)
    # 分析实验6的结果
    success2, output2 = run_command(["python", "analyze_fault_tolerance.py"], cwd=os.path.join(ROOT_DIR, "scripts"), timeout=300)
    return success1 and success2

def main():
    """主函数，按顺序运行所有实验"""
    logging.info("====== 开始分别运行所有实验 ======")

    # 步骤1: 生成数据集
    logging.info("步骤1: 生成证书数据集")
    success, _ = run_command(["python", "generate_dataset.py"], cwd=os.path.join(ROOT_DIR, "scripts"))
    if not success:
        logging.error("数据集生成失败，尝试继续运行实验")

    # 步骤2: 检查Hardhat节点是否在运行，如果没有则启动
    logging.info("步骤2: 检查Hardhat节点")
    hardhat_process = None
    if not check_hardhat_running():
        logging.info("Hardhat节点未运行，正在启动...")
        # Use a non-blocking Popen to start the Hardhat node as a background process
        log_file_path = os.path.join(LOG_DIR, 'hardhat_node.log')
        with open(log_file_path, 'w') as log_file:
            hardhat_process = subprocess.Popen(
                ["npx", "hardhat", "node"], 
                cwd=ROOT_DIR, 
                stdout=log_file, 
                stderr=subprocess.STDOUT
            )
        time.sleep(10)  # 等待节点启动
        if not check_hardhat_running():
            logging.error("Hardhat节点启动失败，终止实验")
            if hardhat_process: hardhat_process.terminate()
            return
        logging.info("Hardhat节点已成功启动")
    else:
        logging.info("Hardhat节点已在运行")

    try:
        # 步骤3: 运行实验
        experiments = {
            1: ("基础性能评估", "run_experiment_1_baseline", True),
            2: ("吞吐量分析", "run_experiment_2_throughput", True),
            3: ("可扩展性分析", "run_experiment_3_scalability", True),
            4: ("存储成本对比分析", "run_experiment_4_storage", True),
            5: ("撤销机制效率分析", "run_experiment_5_revocation", True),
        }

        for exp_num, (name, func_name, with_helper) in experiments.items():
            logging.info(f"运行 实验{exp_num}: {name}")
            success = run_experiment(exp_num, name, func_name, with_helper)
            if success:
                logging.info(f"实验{exp_num}: {name} 运行成功")
            else:
                logging.error(f"实验{exp_num}: {name} 运行失败，继续下一个实验")

        # 步骤4: 运行实验6 (故障容错测试)
        if hardhat_process:
            hardhat_process.terminate()
            hardhat_process.wait()
            logging.info("已关闭通用Hardhat节点，准备运行实验6")
            time.sleep(5)

        logging.info("运行 实验6: 节点故障恢复测试")
        # Note: For experiment 6, we pass the script name relative to the current script's directory.
        success = run_experiment(6, "节点故障恢复测试", 'fault_tolerance_test.py', False)
        if success:
            logging.info("实验6: 节点故障恢复测试 运行成功")
        else:
            logging.error("实验6: 节点故障恢复测试 运行失败")

        # 步骤5: 分析所有实验结果
        logging.info("分析所有实验结果")
        if analyze_results():
            logging.info("实验结果分析成功")
        else:
            logging.error("实验结果分析失败")

    finally:
        # 确保所有进程都被清理
        if hardhat_process and hardhat_process.poll() is None:
            hardhat_process.terminate()
            logging.info("Hardhat节点已关闭")

    logging.info("====== 所有实验运行完成 ======")
    logging.info("请查看 data/ 目录和 analysis/ 目录获取实验结果和分析")

if __name__ == "__main__":
    main()
