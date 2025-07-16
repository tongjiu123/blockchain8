"""
Script to analyze fault tolerance test results
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Constants
BASE_DIR = "/Users/yangzongyou/Downloads/iccip 2022/code_exp"
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "analysis")
FAULT_TOLERANCE_FILE = "fault_tolerance_test.csv"

def analyze_fault_tolerance():
    """Analyze fault tolerance test results"""
    print("Analyzing fault tolerance test results...")
    
    # Create output directory if it doesn't exist
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Read the fault tolerance test data
    fault_data_path = os.path.join(DATA_DIR, FAULT_TOLERANCE_FILE)
    if not os.path.exists(fault_data_path):
        print(f"Fault tolerance data file not found at {fault_data_path}")
        return
    
    df = pd.read_csv(fault_data_path)
    
    # Calculate failed nodes
    df['failed_nodes'] = df['total_nodes'] - df['active_nodes']
    
    # Create a figure with two subplots
    fig, axes = plt.subplots(1, 2, figsize=(15, 6))
    
    # Plot 1: Availability vs Failed Nodes
    sns.barplot(x='failed_nodes', y='availability', data=df, ax=axes[0], color='skyblue')
    axes[0].set_title('System Availability vs Failed Nodes')
    axes[0].set_xlabel('Number of Failed Nodes')
    axes[0].set_ylabel('Availability (Success Rate)')
    axes[0].set_ylim(0, 1.1)
    
    # Add value labels on top of bars
    for i, v in enumerate(df['availability']):
        axes[0].text(i, v + 0.05, f'{v:.2f}', ha='center')
    
    # Plot 2: Recovery Time vs Failed Nodes
    sns.barplot(x='failed_nodes', y='recovery_time', data=df, ax=axes[1], color='lightgreen')
    axes[1].set_title('Recovery Time vs Failed Nodes')
    axes[1].set_xlabel('Number of Failed Nodes')
    axes[1].set_ylabel('Recovery Time (seconds)')
    
    # Add value labels on top of bars
    for i, v in enumerate(df['recovery_time']):
        axes[1].text(i, v + 2, f'{v:.1f}', ha='center')
    
    plt.tight_layout()
    
    # Save the figure
    output_path = os.path.join(OUTPUT_DIR, 'fig6_fault_tolerance.png')
    plt.savefig(output_path)
    print(f"Plot saved to {output_path}")
    
    # Generate markdown summary
    summary_path = os.path.join(OUTPUT_DIR, 'fault_tolerance_summary.md')
    with open(summary_path, 'w') as f:
        f.write("# Fault Tolerance Test Results\n\n")
        f.write("## Overview\n")
        f.write("This experiment evaluated the system's resilience to node failures in a multi-node blockchain network. ")
        f.write("We tested three scenarios with varying numbers of failed nodes and measured availability, recovery time, and data consistency.\n\n")
        
        f.write("## Test Scenarios\n")
        f.write("| Scenario | Active Nodes | Failed Nodes | Fault Duration (s) |\n")
        f.write("|----------|-------------|-------------|-------------------|\n")
        for _, row in df.iterrows():
            f.write(f"| {row['scenario']} | {row['active_nodes']} | {row['failed_nodes']} | {row['fault_duration']} |\n")
        
        f.write("\n## Availability Results\n")
        f.write("| Scenario | Availability | Successful Txs | Failed Txs |\n")
        f.write("|----------|-------------|---------------|------------|\n")
        for _, row in df.iterrows():
            f.write(f"| {row['scenario']} | {row['availability']:.2f} | {row['successful_txs']} | {row['failed_txs']} |\n")
        
        f.write("\n## Recovery Results\n")
        f.write("| Scenario | Recovery Time (s) | Sync Complete | Data Consistent |\n")
        f.write("|----------|------------------|---------------|----------------|\n")
        for _, row in df.iterrows():
            f.write(f"| {row['scenario']} | {row['recovery_time']:.2f} | {row['sync_complete']} | {row['data_consistent']} |\n")
        
        f.write("\n## Key Findings\n")
        
        # Calculate average availability and recovery time
        avg_availability = df['availability'].mean()
        avg_recovery = df['recovery_time'].mean()
        
        f.write(f"- **Average System Availability**: {avg_availability:.2f} (or {avg_availability*100:.1f}%)\n")
        f.write(f"- **Average Recovery Time**: {avg_recovery:.2f} seconds\n")
        
        # Find the scenario with the highest availability
        best_scenario = df.loc[df['availability'].idxmax()]['scenario']
        f.write(f"- **Best Availability Scenario**: {best_scenario}\n")
        
        # Find the scenario with the lowest recovery time
        fastest_recovery = df.loc[df['recovery_time'].idxmin()]['scenario']
        f.write(f"- **Fastest Recovery Scenario**: {fastest_recovery}\n")
        
        # Check data consistency
        consistent_scenarios = df[df['data_consistent'] == True]['scenario'].tolist()
        if consistent_scenarios:
            f.write(f"- **Data Consistency**: Maintained in {', '.join(consistent_scenarios)}\n")
        else:
            f.write("- **Data Consistency**: Not maintained in any scenario\n")
        
        f.write("\n## Visualization\n")
        f.write("![Fault Tolerance Test Results](./fig6_fault_tolerance.png)\n")
        
        f.write("\n## Conclusion\n")
        f.write("The fault tolerance test demonstrates that our blockchain-based academic credential system ")
        
        if avg_availability > 0.7:
            f.write("maintains good availability even when multiple nodes fail. ")
        elif avg_availability > 0.5:
            f.write("maintains moderate availability when nodes fail. ")
        else:
            f.write("shows reduced availability when multiple nodes fail. ")
        
        if any(df['data_consistent']):
            f.write("Data consistency is maintained in scenarios with limited node failures, ")
        else:
            f.write("Data consistency is challenging to maintain across all failure scenarios, ")
        
        f.write("and recovery times increase with the number of failed nodes. ")
        f.write("These results highlight the trade-offs between availability, consistency, and recovery time ")
        f.write("in distributed blockchain systems and provide insights for optimizing fault tolerance mechanisms.")
    
    print(f"Summary saved to {summary_path}")
    return summary_path

if __name__ == "__main__":
    analyze_fault_tolerance()
