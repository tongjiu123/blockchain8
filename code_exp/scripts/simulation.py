import os
import json
import time
import logging
import asyncio
from datetime import datetime
import threading
import random

import pandas as pd
from tqdm import tqdm
from web3 import Web3
from web3.middleware import geth_poa_middleware
from dotenv import load_dotenv

# --- Configuration & Setup ---
load_dotenv()

# --- Constants ---
HARDHAT_RPC_URL = "http://127.0.0.1:8545"
DEPLOYER_PRIVATE_KEY = os.getenv("PRIVATE_KEY")

# --- File Paths ---
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ARTIFACTS_DIR = os.path.join(ROOT_DIR, 'artifacts', 'contracts')
CERTIFICATE_ARTIFACT_PATH = os.path.join(ARTIFACTS_DIR, 'Certificate.sol', 'Certificate.json')
CERTIFICATE_ONCHAIN_ARTIFACT_PATH = os.path.join(ARTIFACTS_DIR, 'CertificateOnChain.sol', 'CertificateOnChain.json')
BASELINE_REVOCATION_ARTIFACT_PATH = os.path.join(ARTIFACTS_DIR, 'BaselineRevocation.sol', 'BaselineRevocation.json')
DATASET_PATH = os.path.join(os.path.dirname(__file__), '..', 'dataset', 'certificates_data.csv')

# --- Output Directories ---
CODE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DATA_DIR = os.path.join(CODE_DIR, 'data')
LOG_DIR = os.path.join(CODE_DIR, 'log')

# --- Experiment Parameters ---
LATENCY_TEST_RECORDS = 1000
THROUGHPUT_CONCURRENCY_LEVELS = [1, 10, 50, 100, 200, 500, 1000]
THROUGHPUT_TEST_DURATION_SECONDS = 60
SCALABILITY_LEVELS = [10000, 50000, 100000, 500000, 1000000]
SCALABILITY_VERIFICATION_QUERIES = 1000

# --- Logging Setup ---
os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(DATA_DIR, exist_ok=True)
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, f'simulation_run_{timestamp}.log')),
        logging.StreamHandler()
    ]
)

# --- Web3 Helper Class ---
class BlockchainHelper:
    """A helper class to manage interaction with the blockchain."""

    def __init__(self, rpc_url, private_key):
        self.w3 = Web3(Web3.HTTPProvider(rpc_url, request_kwargs={'timeout': 120}))
        time.sleep(5) # Add a 5-second delay to allow the node to initialize
        if not self.w3.is_connected():
            raise ConnectionError("Failed to connect to the Hardhat RPC node after delay.")
        self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)
        self.account = self.w3.eth.account.from_key(private_key)
        self.w3.eth.default_account = self.account.address
        logging.info(f"Connected to Web3. Default account: {self.account.address}")

    def get_contract_factory(self, artifact_path):
        with open(artifact_path, 'r') as f:
            artifact = json.load(f)
        return self.w3.eth.contract(abi=artifact['abi'], bytecode=artifact['bytecode'])

    def deploy_contract(self, contract_name, contract_factory, *args):
        """Deploys a contract and waits for the transaction to be mined."""
        logging.info(f"Deploying {contract_name}...")
        tx_hash = contract_factory.constructor(*args).transact({'from': self.account.address})
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        contract_address = tx_receipt.contractAddress
        contract = self.w3.eth.contract(address=contract_address, abi=contract_factory.abi)
        logging.info(f"{contract_name} deployed at {contract_address}. Gas used: {tx_receipt.gasUsed}")
        return contract, tx_receipt.gasUsed

    def authorize_institution(self, contract, is_onchain=False):
        """Authorizes the deployer account as an institution on the given contract."""
        logging.info(f"Authorizing deployer as an institution for {contract.address}...")
        if is_onchain:
            logging.info(f"Skipping institution authorization for on-chain contract {contract.address} (owner is default issuer).")
            return

        tx_hash = contract.functions.addInstitution(self.account.address).transact()
        self.w3.eth.wait_for_transaction_receipt(tx_hash)
        logging.info("Authorization successful.")

# --- Simulation Experiments ---

def run_experiment_1_baseline(helper, contract, dataset):
    """Experiment 1: Baseline Performance & Cost Assessment."""
    logging.info("--- Starting Experiment 1: Baseline Performance & Cost ---")
    results = []

    logging.info(f"Measuring latency for {LATENCY_TEST_RECORDS} 'issueCertificate' transactions...")
    issue_hashes_exp1 = dataset.iloc[0:LATENCY_TEST_RECORDS]['certificate_hash'].tolist()

    for cert_hash in tqdm(issue_hashes_exp1, desc="Exp 1: Latency Test"):
        start_time = time.time()
        tx_hash = contract.functions.issueCertificate(Web3.to_bytes(hexstr=cert_hash)).transact()
        helper.w3.eth.wait_for_transaction_receipt(tx_hash)
        end_time = time.time()
        latency = end_time - start_time
        results.append({'operation': 'issueCertificate', 'latency_seconds': latency})

    df_latency = pd.DataFrame(results)
    df_latency.to_csv(os.path.join(DATA_DIR, 'exp1_latency.csv'), index=False)
    logging.info(f"Latency results saved to exp1_latency.csv")

    logging.info("Measuring gas cost for core operations...")
    gas_issue_hash = dataset.iloc[LATENCY_TEST_RECORDS]['certificate_hash']
    gas_revoke_hash = dataset.iloc[LATENCY_TEST_RECORDS + 1]['certificate_hash']

    gas_issue = contract.functions.issueCertificate(Web3.to_bytes(hexstr=gas_issue_hash)).estimate_gas()
    
    tx_hash = contract.functions.issueCertificate(Web3.to_bytes(hexstr=gas_revoke_hash)).transact()
    helper.w3.eth.wait_for_transaction_receipt(tx_hash)
    gas_revoke = contract.functions.revokeCertificate(Web3.to_bytes(hexstr=gas_revoke_hash)).estimate_gas()

    gas_verify = contract.functions.getCertificateStatus(Web3.to_bytes(hexstr=gas_issue_hash)).estimate_gas()

    df_gas = pd.DataFrame([
        {'operation': 'issueCertificate', 'gas_cost': gas_issue},
        {'operation': 'revokeCertificate', 'gas_cost': gas_revoke},
        {'operation': 'verifyCertificate', 'gas_cost': gas_verify}
    ])
    df_gas.to_csv(os.path.join(DATA_DIR, 'exp1_gas_cost.csv'), index=False)
    logging.info(f"Gas cost results saved to exp1_gas_cost.csv")
    logging.info("--- Experiment 1 Finished ---")
    return LATENCY_TEST_RECORDS

async def run_experiment_2_throughput(helper, contract, dataset):
    """Experiment 2: Throughput & Stress Test."""
    logging.info("--- Starting Experiment 2: Throughput & Stress Test ---")
    results = []

    # Use a dedicated, non-overlapping subset of data from the end of the dataset
    # to avoid polluting the state for Experiment 3.
    test_data_subset = dataset.tail(10000).copy()
    logging.info(f"Running throughput test with {len(test_data_subset)} unique records from the end of the dataset.")

    for level in THROUGHPUT_CONCURRENCY_LEVELS:
        logging.info(f"Testing throughput with concurrency level: {level}")
        
        # Use a thread-safe counter for successful transactions
        successful_tx = 0
        lock = threading.Lock()
        
        # Set a fixed duration for the test
        test_duration = 60  # seconds
        test_end_time = time.time() + test_duration

        def task_body():
            nonlocal successful_tx
            # Each thread gets its own Web3 instance to avoid nonce and connection issues
            local_helper = BlockchainHelper(helper.w3.provider.endpoint_uri, helper.account.key)
            local_contract = local_helper.w3.eth.contract(address=contract.address, abi=contract.abi)

            while time.time() < test_end_time:
                try:
                    # Sample a random record from the dedicated test set
                    row = test_data_subset.sample(1).iloc[0]
                    # Add a random element to the hash to ensure it's unique for every single call
                    cert_hash = Web3.keccak(text=f"{row['student_name']}{row['degree_type']}{row['institution_name']}{random.random()}")
                    
                    tx_hash = local_contract.functions.issueCertificate(cert_hash).transact()
                    # Wait for receipt to confirm the transaction was actually successful
                    receipt = local_helper.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=30)
                    
                    if receipt.status == 1:
                        with lock:
                            successful_tx += 1
                except Exception as e:
                    # In a high-concurrency test, some failures (e.g., timeouts, nonce gaps) are expected.
                    # We log them but continue the test.
                    logging.warning(f"Transaction failed in thread with error: {e}")
        
        try:
            threads = [threading.Thread(target=task_body) for _ in range(level)]
            
            start_time = time.time()
            for t in threads:
                t.start()
            for t in threads:
                t.join()
            duration = time.time() - start_time

            # Ensure duration is at least the planned test duration
            actual_duration = max(duration, test_duration)
            tps = successful_tx / actual_duration if actual_duration > 0 else 0
        
        except RuntimeError as e:
            if "can't start new thread" in str(e):
                logging.error(f"Failed to start threads for concurrency level {level}: {e}")
                tps = 0  # Record TPS as 0 since the test couldn't run
                actual_duration = test_duration # Use the planned duration
            else:
                raise # Re-raise other runtime errors
        
        logging.info(f"Level {level}: {successful_tx} successful transactions in {actual_duration:.2f}s. TPS: {tps:.2f}")
        results.append({'concurrency_level': level, 'tps': tps})

    df = pd.DataFrame(results)
    df.to_csv(os.path.join(DATA_DIR, 'exp2_throughput.csv'), index=False)
    logging.info(f"Throughput results saved to exp2_throughput.csv")
    logging.info("--- Experiment 2 Finished ---")

def run_experiment_3_scalability(helper, contract, dataset, initial_records=0):
    """Experiment 3: Large-Scale Scalability Test."""
    logging.info("--- Starting Experiment 3: Scalability Test ---")
    results = []
    
    last_level = initial_records
    for level in SCALABILITY_LEVELS:
        records_to_issue_count = level - last_level
        if records_to_issue_count <= 0:
            continue

        logging.info(f"Issuing {records_to_issue_count} new certificates to reach {level} total records...")
        issue_hashes_to_reach_level = dataset.iloc[last_level:level]['certificate_hash'].tolist()
            
        for cert_hash in tqdm(issue_hashes_to_reach_level, desc=f"Issuing to reach {level}"):
            tx_hash = contract.functions.issueCertificate(Web3.to_bytes(hexstr=cert_hash)).transact()
            helper.w3.eth.wait_for_transaction_receipt(tx_hash)

        # For verification, we query the hashes just added in this batch
        # This measures the query time at the current total number of records
        total_query_time = 0
        query_hashes = issue_hashes_to_reach_level[:SCALABILITY_VERIFICATION_QUERIES]

        if query_hashes:
            start_query_time = time.time()
            for q_hash in query_hashes:
                contract.functions.getCertificateStatus(Web3.to_bytes(hexstr=q_hash)).call()
            end_query_time = time.time()
            total_query_time = end_query_time - start_query_time
        
        avg_query_time = (total_query_time / len(query_hashes)) if query_hashes else 0
        logging.info(f"Total Records: {level}, Average Query Time: {avg_query_time:.6f}s")
        results.append({'total_records': level, 'avg_query_time_seconds': avg_query_time})

        last_level = level

    df_scalability = pd.DataFrame(results)
    df_scalability.to_csv(os.path.join(DATA_DIR, 'exp3_scalability.csv'), index=False)
    logging.info(f"Scalability results saved to exp3_scalability.csv")
    logging.info("--- Experiment 3 Finished ---")
    return records_to_issue_count

def run_experiment_4_storage(helper, cert_contract, cert_onchain_contract, dataset, deploy_gas_hybrid, deploy_gas_onchain):
    """Experiment 4: Storage Cost Comparative Analysis."""
    logging.info("--- Starting Experiment 4: Storage Cost Comparison ---")
    
    df_gas_hybrid = pd.read_csv(os.path.join(DATA_DIR, 'exp1_gas_cost.csv'))
    gas_hybrid_issue = df_gas_hybrid[df_gas_hybrid['operation'] == 'issueCertificate']['gas_cost'].iloc[0]

    record = dataset.iloc[0]
    gas_onchain_issue = cert_onchain_contract.functions.issueCertificate(
        record['student_name'],
        record['degree_type'],
        record['institution_name']
    ).estimate_gas()

    df_comparison = pd.DataFrame([
        {'model': 'Hybrid (Ours)', 'deploy_gas': deploy_gas_hybrid, 'issue_gas': gas_hybrid_issue},
        {'model': 'Full On-Chain (Baseline)', 'deploy_gas': deploy_gas_onchain, 'issue_gas': gas_onchain_issue}
    ])
    df_comparison.to_csv(os.path.join(DATA_DIR, 'exp4_storage_comparison.csv'), index=False)
    logging.info(f"Storage cost comparison results saved to exp4_storage_comparison.csv")
    logging.info("--- Experiment 4 Finished ---")

def run_experiment_5_revocation(helper, cert_factory, baseline_revocation_factory):
    """Experiment 5: Revocation Mechanism Efficiency."""
    logging.info("--- Starting Experiment 5: Revocation Mechanism ---")

    os.makedirs(DATA_DIR, exist_ok=True)

    revocation_sizes = [1, 10, 100, 1000, 5000]
    num_verifications = 100
    num_hashes_needed = max(revocation_sizes) + num_verifications + 1
    certificate_hashes = [helper.w3.keccak(text=f"exp5-cert-{i}") for i in range(num_hashes_needed)]

    results = []

    for size in revocation_sizes:
        logging.info(f"Deploying new contracts for size {size}...")
        cert_contract, _ = helper.deploy_contract(f"Certificate_Exp5_{size}", cert_factory, helper.account.address)
        helper.authorize_institution(cert_contract)
        baseline_contract, _ = helper.deploy_contract(f"BaselineRevocation_Exp5_{size}", baseline_revocation_factory)
        logging.info(f"Testing revocation set size: {size}")

        # --- OUR MODEL (Certificate Contract) ---
        logging.info(f"[Our Model] Issuing and revoking {size} certificates...")
        # Issue and revoke `size` certificates to populate the revocation data
        for i in tqdm(range(size), desc=f"[Our Model] Setup for size {size}"):
            # Issue
            tx_hash_issue = cert_contract.functions.issueCertificate(certificate_hashes[i]).transact()
            helper.w3.eth.wait_for_transaction_receipt(tx_hash_issue)
            # Revoke
            tx_hash_revoke = cert_contract.functions.revokeCertificate(certificate_hashes[i]).transact()
            helper.w3.eth.wait_for_transaction_receipt(tx_hash_revoke)

        # --- BASELINE MODEL (On-chain list) ---
        logging.info(f"[Baseline Model] Revoking {size} certificates...")
        for i in tqdm(range(size), desc=f"[Baseline Model] Setup for size {size}"):
            tx_hash = baseline_contract.functions.revoke(certificate_hashes[i]).transact()
            helper.w3.eth.wait_for_transaction_receipt(tx_hash)

        # --- Verification & Gas Measurement (after setup) ---
        our_verify_gas, our_verify_time = 0, 0
        baseline_verify_gas, baseline_verify_time = 0, 0

        logging.info(f"Measuring verification performance for size {size} ({num_verifications} queries)..." )
        for i in tqdm(range(num_verifications), desc="Verification Measurement"):
            # Alternate between revoked and non-revoked hashes for a fair test
            # A revoked hash (index < size) and a valid hash (index >= size)
            h = certificate_hashes[i] if i % 2 == 0 else certificate_hashes[size + i]

            # Our model verification
            start_time = time.time()
            our_verify_gas += cert_contract.functions.getCertificateStatus(h).estimate_gas()
            cert_contract.functions.getCertificateStatus(h).call()
            our_verify_time += time.time() - start_time

            # Baseline model verification
            start_time = time.time()
            baseline_verify_gas += baseline_contract.functions.isRevoked(h).estimate_gas()
            baseline_contract.functions.isRevoked(h).call()
            baseline_verify_time += time.time() - start_time

        # --- Gas Cost for Adding a new item to Revocation List ---
        # Use a new hash that hasn't been used yet
        new_hash_to_revoke = certificate_hashes[size + num_verifications]
        # For our model, we must issue it first before revoking
        tx_hash = cert_contract.functions.issueCertificate(new_hash_to_revoke).transact()
        helper.w3.eth.wait_for_transaction_receipt(tx_hash)
        our_revoke_gas = cert_contract.functions.revokeCertificate(new_hash_to_revoke).estimate_gas()
        baseline_revoke_gas = baseline_contract.functions.revoke(new_hash_to_revoke).estimate_gas()

        results.append({
            'revocation_size': size,
            'our_revoke_gas': our_revoke_gas,
            'baseline_revoke_gas': baseline_revoke_gas,
            'our_avg_verify_gas': our_verify_gas / num_verifications,
            'baseline_avg_verify_gas': baseline_verify_gas / num_verifications,
            'our_avg_verify_time': our_verify_time / num_verifications,
            'baseline_avg_verify_time': baseline_verify_time / num_verifications,
        })
        logging.info(f"Size {size}: Verification stats collected.")

    df_results = pd.DataFrame(results)
    results_path = os.path.join(DATA_DIR, "exp5_revocation_scalability.csv")
    df_results.to_csv(results_path, index=False)
    logging.info(f"Revocation mechanism efficiency results saved to {results_path}")
    logging.info("--- Experiment 5 Finished ---")

# --- Main Execution Logic ---
def main():
    """Main function to run the entire simulation suite."""
    logging.info("====== STARTING SIMULATION ======")

    if not DEPLOYER_PRIVATE_KEY:
        logging.error("FATAL: PRIVATE_KEY not found in .env file. Please set it up.")
        return

    try:
        helper = BlockchainHelper(HARDHAT_RPC_URL, DEPLOYER_PRIVATE_KEY)

        logging.info(f"Loading dataset from {DATASET_PATH}...")
        if not os.path.exists(DATASET_PATH):
            logging.error(f"Dataset not found. Please run generate_dataset.py first.")
            return
        dataset = pd.read_csv(DATASET_PATH)
        logging.info(f"Dataset loaded with {len(dataset)} records.")

        # --- Get Contract Factories ---
        cert_factory = helper.get_contract_factory(CERTIFICATE_ARTIFACT_PATH)
        cert_onchain_factory = helper.get_contract_factory(CERTIFICATE_ONCHAIN_ARTIFACT_PATH)
        baseline_revocation_factory = helper.get_contract_factory(BASELINE_REVOCATION_ARTIFACT_PATH)

        # --- Deploy Contracts for All Experiments ---
        logging.info("--- Deploying all contracts for experiments ---")
        cert_contract_exp1, deploy_gas_hybrid = helper.deploy_contract("Certificate (Exp1-3)", cert_factory, helper.account.address)
        helper.authorize_institution(cert_contract_exp1)
        
        cert_onchain_contract_exp4, deploy_gas_onchain = helper.deploy_contract("CertOnChain (Exp4)", cert_onchain_factory, helper.account.address)
        helper.authorize_institution(cert_onchain_contract_exp4, is_onchain=True)

        # --- State tracking for experiments ---
        total_issued_certificates = 0

        # Run experiments
        newly_issued = run_experiment_1_baseline(helper, cert_contract_exp1, dataset)
        total_issued_certificates += newly_issued
        logging.info(f"Total certificates issued after Exp 1: {total_issued_certificates}")

        # For Exp2, we use the same contract as Exp1 to measure throughput on a contract with existing state.
        asyncio.run(run_experiment_2_throughput(helper, cert_contract_exp1, dataset))

        newly_issued = run_experiment_3_scalability(helper, cert_contract_exp1, dataset, initial_records=total_issued_certificates)
        total_issued_certificates += newly_issued
        logging.info(f"Total certificates issued after Exp 3: {total_issued_certificates}")

        run_experiment_4_storage(helper, cert_contract_exp1, cert_onchain_contract_exp4, dataset, deploy_gas_hybrid, deploy_gas_onchain)
        
        run_experiment_5_revocation(helper, cert_factory, baseline_revocation_factory)
        
        logging.info("\n--- Note on Experiment 6: Node Fault Recovery Test ---")
        logging.info("This experiment is designed to be run separately as it requires managing multiple Hardhat nodes.")
        logging.info("To run this experiment, please execute the dedicated script: python scripts/fault_tolerance_test.py")

    except Exception as e:
        logging.critical(f"An unrecoverable error occurred: {e}", exc_info=True)
    finally:
        logging.info("====== SIMULATION FINISHED ======")

if __name__ == '__main__':
    main()
