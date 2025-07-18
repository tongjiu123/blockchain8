import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import traceback

# --- Boilerplate for standalone execution ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'data'))
ANALYSIS_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'analysis'))
sns.set_theme(style="whitegrid", palette="viridis")
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

def save_plot(fig, name):
    os.makedirs(ANALYSIS_DIR, exist_ok=True)
    path = os.path.join(ANALYSIS_DIR, f"{name}.png")
    fig.savefig(path, dpi=300, bbox_inches='tight')
    print(f"Plot saved to {path}")
    plt.close(fig)
    # Use relative path for markdown
    return f"![{name.replace('_', ' ').title()}](./{name}.png)"

# --- Analysis Function ---
def analyze_exp1_baseline(summary_file):
    try:
        df_latency = pd.read_csv(os.path.join(DATA_DIR, 'exp1_latency.csv'))
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.histplot(df_latency['latency_seconds'], kde=True, ax=ax)
        ax.set_title('Distribution of Certificate Issuance Latency', fontsize=16, fontweight='bold')
        ax.set_xlabel('Latency (seconds)', fontsize=12)
        ax.set_ylabel('Frequency', fontsize=12)
        avg_latency = df_latency['latency_seconds'].mean()
        ax.axvline(avg_latency, color='red', linestyle='--', label=f'Average: {avg_latency:.4f}s')
        ax.legend()
        plot_md = save_plot(fig, 'fig1a_issuance_latency')
        summary_file.write("\n### Experiment 1: Baseline Performance\n")
        avg_latency_ms = avg_latency * 1000
        summary_file.write(f"This experiment measured the time to issue {len(df_latency)} certificates. The average latency was **{avg_latency:.4f} seconds ({avg_latency_ms:.2f} ms)**. The distribution of these latencies is shown below.\n\n")
        summary_file.write(plot_md + "\n")

        df_gas = pd.read_csv(os.path.join(DATA_DIR, 'exp1_gas_cost.csv'))
        fig, ax = plt.subplots(figsize=(8, 5))
        sns.barplot(x='operation', y='gas_cost', data=df_gas, ax=ax, palette='viridis', hue='operation', legend=False)
        ax.set_title('Gas Cost for Core Operations', fontsize=16, fontweight='bold')
        ax.set_xlabel('Operation', fontsize=12)
        ax.set_ylabel('Gas Cost', fontsize=12)
        ax.ticklabel_format(style='plain', axis='y')
        for container in ax.containers:
            ax.bar_label(container, fmt='{:,.0f}')
        plot_md = save_plot(fig, 'fig1b_gas_cost')
        summary_file.write("\nIt also measured the gas cost for fundamental operations.\n\n")
        summary_file.write(plot_md + "\n")
    except FileNotFoundError as e:
        summary_file.write(f"\n*   Data file not found for Experiment 1. Skipping analysis. Error: {e}*\n")
    except Exception as e:
        summary_file.write(f"\n*   An error occurred during Experiment 1 analysis: {e}*\n")
        traceback.print_exc()
    finally:
        plt.close('all')

# --- Main Execution ---
if __name__ == '__main__':
    summary_part_path = os.path.join(ANALYSIS_DIR, '_exp1_summary.md')
    with open(summary_part_path, 'w') as f:
        analyze_exp1_baseline(f)
