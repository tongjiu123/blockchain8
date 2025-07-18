#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
区块链学术凭证系统论文图表生成脚本

根据 simulation.js 生成的实验数据，绘制性能图表。
"""

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

# --- Configuration ---
# Set global styles for the plots
plt.style.use('seaborn-v0_8-paper')
matplotlib.rcParams['font.family'] = 'sans-serif'
matplotlib.rcParams['font.sans-serif'] = ['Helvetica'] # A common, professional font
matplotlib.rcParams['font.size'] = 12
matplotlib.rcParams['figure.figsize'] = (8, 5)
matplotlib.rcParams['figure.dpi'] = 300

# Define data source directory and chart output format
DATA_DIR = '../../代码实现/result/'
OUTPUT_FORMAT = 'png'  # Options: 'pdf', 'svg' for better quality

# --- Data Translation ---
# Map Chinese operation names to English for professional, publication-ready charts.
OPERATION_NAME_MAP = {
    '凭证颁发': 'Issue Credential',
    '颁发凭证': 'Issue Credential',
    '凭证验证请求': 'Verify Credential',
    '创建验证请求': 'Verify Credential',
    '凭证验证': 'Verify Credential',
    '凭证撤销': 'Revoke Credential',
    '撤销凭证': 'Revoke Credential',
}

# --- Chart Generation Functions ---

def plot_throughput_chart():
    """Generate the throughput chart."""
    print("Generating throughput chart...")
    file_path = os.path.join(DATA_DIR, 'throughput_data.csv')
    if not os.path.exists(file_path):
        print(f"Error: Data file not found at {file_path}")
        return

    df = pd.read_csv(file_path)
    # Translate operation names to English
    df['Operation'] = df['Operation'].map(OPERATION_NAME_MAP).fillna(df['Operation'])
    pivot_df = df.pivot(index='BatchSize', columns='Operation', values='TPS')

    fig, ax = plt.subplots()
    pivot_df.plot(kind='bar', ax=ax, width=0.8, colormap='viridis')

    ax.set_title('System Throughput vs. Batch Size', fontsize=16, pad=20)
    ax.set_xlabel('Batch Size', fontsize=12)
    ax.set_ylabel('Throughput (TPS)', fontsize=12)
    ax.legend(title='Operation')
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)
    plt.xticks(rotation=0)
    plt.tight_layout()

    output_path = f'throughput_chart.{OUTPUT_FORMAT}'
    plt.savefig(output_path)
    plt.close()
    print(f"Throughput chart saved to {output_path}")

def plot_latency_chart():
    """Generate the latency chart."""
    print("Generating latency chart...")
    file_path = os.path.join(DATA_DIR, 'latency_data.csv')
    if not os.path.exists(file_path):
        print(f"Error: Data file not found at {file_path}")
        return

    df = pd.read_csv(file_path)
    # Translate operation names to English
    df['Operation'] = df['Operation'].map(OPERATION_NAME_MAP).fillna(df['Operation'])
    pivot_df = df.pivot(index='ConcurrentUsers', columns='Operation', values='LatencyMs')

    fig, ax = plt.subplots()
    pivot_df.plot(kind='line', ax=ax, marker='o', linestyle='-')

    ax.set_title('Average System Latency vs. Concurrent Users', fontsize=16, pad=20)
    ax.set_xlabel('Number of Concurrent Users', fontsize=12)
    ax.set_ylabel('Average Latency (ms)', fontsize=12)
    ax.legend(title='Operation')
    ax.grid(True, which='both', linestyle='--', alpha=0.7)
    plt.tight_layout()

    output_path = f'latency_chart.{OUTPUT_FORMAT}'
    plt.savefig(output_path)
    plt.close()
    print(f"Latency chart saved to {output_path}")

def plot_gas_usage_chart():
    """Generate the gas usage chart."""
    print("Generating gas usage chart...")
    file_path = os.path.join(DATA_DIR, 'gas_usage.csv')
    if not os.path.exists(file_path):
        print(f"Error: Data file not found at {file_path}")
        return

    df = pd.read_csv(file_path)
    # Translate operation names to English
    df['Operation'] = df['Operation'].map(OPERATION_NAME_MAP).fillna(df['Operation'])
    df = df.set_index('Operation')

    fig, ax = plt.subplots()
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
    bars = ax.bar(df.index, df['GasUsed'], color=colors)

    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval, f'{int(yval):,}', va='bottom', ha='center')

    ax.set_title('Gas Consumption for Core Operations', fontsize=16, pad=20)
    ax.set_xlabel('Operation Type', fontsize=12)
    ax.set_ylabel('Gas Consumed', fontsize=12)
    ax.get_yaxis().set_major_formatter(
        matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    ax.grid(True, axis='y', linestyle='--', alpha=0.7)
    plt.xticks(rotation=0)
    plt.tight_layout()

    output_path = f'gas_usage_chart.{OUTPUT_FORMAT}'
    plt.savefig(output_path)
    plt.close()
    print(f"Gas usage chart saved to {output_path}")


def generate_all_charts():
    """主函数，生成所有图表"""
    # 切换到脚本所在目录，以确保输出文件保存在正确位置
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print(f"图表将保存在: {os.getcwd()}")

    plot_throughput_chart()
    plot_latency_chart()
    plot_gas_usage_chart()

    print("\n所有图表已成功生成!")

if __name__ == "__main__":
    generate_all_charts()
