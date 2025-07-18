import os
import subprocess
import traceback
import sys

# --- Configuration ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ANALYSIS_DIR = os.path.abspath(os.path.join(BASE_DIR, '..', 'analysis'))

EXPERIMENT_SCRIPTS = [
    'analyze_exp1.py',
    'analyze_exp2.py',
    'analyze_exp3.py',
    'analyze_exp4.py',
    'analyze_exp5.py',
    'analyze_exp6.py',
]

def run_analysis_script(script_name):
    """Runs a single analysis script as a robust, isolated subprocess."""
    print(f"--- Running {script_name} ---")
    script_path = os.path.join(BASE_DIR, script_name)
    exp_num = script_name.split('.')[0].split('_')[1][-1]
    partial_md_path = os.path.join(ANALYSIS_DIR, f'_exp{exp_num}_summary.md')

    # Clean up previous partial file if it exists
    if os.path.exists(partial_md_path):
        os.remove(partial_md_path)

    try:
        process = subprocess.Popen([sys.executable, script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate(timeout=120)  # 2-minute timeout

        if process.returncode == 0:
            print(f"{script_name} completed successfully.")
            if stderr:
                print(f"Warning (stderr):\n{stderr}")
            return partial_md_path
        else:
            print(f"ERROR: {script_name} failed with return code {process.returncode}.")
            print(f"Stderr:\n{stderr}")
            return None

    except subprocess.TimeoutExpired:
        print(f"ERROR: {script_name} timed out.")
        process.kill()
        return None
    except FileNotFoundError:
        print(f"ERROR: Script not found at {script_path}")
        return None
    except Exception as e:
        print(f"ERROR: An unexpected error occurred while running {script_name}: {e}")
        traceback.print_exc()
        return None

def main():
    """Main function to orchestrate all analyses and generate a summary report."""
    os.makedirs(ANALYSIS_DIR, exist_ok=True)
    final_summary_path = os.path.join(ANALYSIS_DIR, 'analysis_summary.md')
    all_partial_files = []

    # Step 1: Run all analysis scripts and collect the paths of the partial files.
    # This ensures all subprocesses complete before we try to read their output.
    for script in EXPERIMENT_SCRIPTS:
        partial_file = run_analysis_script(script)
        if partial_file:
            all_partial_files.append(partial_file)

    # Step 2: Assemble the final report from the partial files.
    with open(final_summary_path, 'w') as final_summary_file:
        final_summary_file.write("# Blockchain Certificate System: Experiment Analysis\n")
        final_summary_file.write("This report presents a detailed quantitative analysis of the blockchain-based academic certificate system.\n")

        for i, script_name in enumerate(EXPERIMENT_SCRIPTS):
            exp_num = script_name.split('.')[0].split('_')[1][-1]
            partial_path = os.path.join(ANALYSIS_DIR, f'_exp{exp_num}_summary.md')
            
            if partial_path in all_partial_files and os.path.exists(partial_path):
                with open(partial_path, 'r') as pf:
                    final_summary_file.write(pf.read())
                final_summary_file.write('\n\n---\n\n')
            else:
                final_summary_file.write(f"\n*   **Failed to generate results for {script_name}. See console for details.**\n")
                final_summary_file.write('\n\n---\n\n')

    # Clean up partial files
    for f in all_partial_files:
        try:
            os.remove(f)
        except OSError as e:
            print(f"Warning: Could not remove partial file {f}: {e}")

    print(f"\nAnalysis complete. Final summary saved to {final_summary_path}")

if __name__ == '__main__':
    main()
