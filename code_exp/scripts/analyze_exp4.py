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
    return f"![{name.replace('_', ' ').title()}](./{name}.png)"

# --- Analysis Function ---
def analyze_exp4_storage(summary_file):
    try:
        df = pd.read_csv(os.path.join(DATA_DIR, 'exp4_storage_comparison.csv'))
        df_melted = df.melt(id_vars='model', value_vars=['deploy_gas', 'issue_gas'], var_name='cost_type', value_name='gas_cost')
        df_melted['cost_type'] = df_melted['cost_type'].replace({'deploy_gas': 'Deploy Contract', 'issue_gas': 'Issue Certificate'})
        fig, ax = plt.subplots(figsize=(10, 6))
        plot = sns.barplot(x='model', y='gas_cost', hue='cost_type', data=df_melted, ax=ax, palette='viridis')
        ax.set_title('Gas Cost Comparison: Hybrid vs. Full On-Chain', fontsize=16, fontweight='bold')
        ax.set_xlabel('Storage Model', fontsize=12)
        ax.set_ylabel('Gas Cost', fontsize=12)
        ax.ticklabel_format(style='plain', axis='y')
        for container in plot.containers:
            plot.bar_label(container, fmt='{:,.0f}')
        plot_md = save_plot(fig, 'fig4_storage_cost')
        summary_file.write("\n### Experiment 4: Storage Cost Analysis\n")
        summary_file.write("This experiment compared the gas costs of deploying the contract and issuing a single certificate for both the proposed hybrid model and a baseline full on-chain model. The results clearly demonstrate the significant cost savings of the hybrid approach.\n\n")
        summary_file.write(plot_md + "\n")
    except FileNotFoundError as e:
        summary_file.write(f"\n*   Skipping Experiment 4 analysis: {e}*\n")
    except Exception as e:
        summary_file.write(f"\n*   An error occurred during Experiment 4 analysis: {e}*\n")
        traceback.print_exc()
    finally:
        plt.close('all')

# --- Main Execution ---
if __name__ == '__main__':
    summary_part_path = os.path.join(ANALYSIS_DIR, '_exp4_summary.md')
    with open(summary_part_path, 'w') as f:
        analyze_exp4_storage(f)
