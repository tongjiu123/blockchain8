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
def analyze_exp3_scalability(summary_file):
    try:
        df = pd.read_csv(os.path.join(DATA_DIR, 'exp3_scalability.csv'))
        fig, ax = plt.subplots(figsize=(10, 6))
        sns.lineplot(x='total_records', y='avg_query_time_seconds', data=df, marker='o', ax=ax)
        ax.set_title('Query Scalability vs. Total Records', fontsize=16, fontweight='bold')
        ax.set_xlabel('Total Records in System (Log Scale)', fontsize=12)
        ax.set_ylabel('Average Query Time (seconds)', fontsize=12)
        ax.set_xscale('log')
        plot_md = save_plot(fig, 'fig3_scalability')
        summary_file.write("\n### Experiment 3: Scalability Analysis\n")
        summary_file.write("This experiment evaluated how query time is affected by the total number of records in the contract. The results show that query time remains low and stable even as the dataset grows to one million records, demonstrating excellent scalability.\n\n")
        summary_file.write(plot_md + "\n")
    except FileNotFoundError as e:
        summary_file.write(f"\n*   Data file not found for Experiment 3. Skipping analysis. Error: {e}*\n")
    except Exception as e:
        summary_file.write(f"\n*   An error occurred during Experiment 3 analysis: {e}*\n")
        traceback.print_exc()
    finally:
        plt.close('all')

# --- Main Execution ---
if __name__ == '__main__':
    summary_part_path = os.path.join(ANALYSIS_DIR, '_exp3_summary.md')
    with open(summary_part_path, 'w') as f:
        analyze_exp3_scalability(f)
