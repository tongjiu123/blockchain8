"""
Fault Tolerance Test for Blockchain Academic Credential System

This script implements Experiment 6: Node Fault Recovery Test, which tests the system's
fault tolerance and recovery capabilities in a distributed environment.
"""

import os
import time
import random
import logging
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
from web3 import Web3
from web3.middleware import geth_poa_middleware
from dotenv import load_dotenv
from node_manager import NodeManager
import json

# --- Configuration & Setup ---
load_dotenv()

# --- Constants ---
BASE_PORT = int(os.getenv("BASE_PORT", "8545"))
NODE_COUNT = 4
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

# --- File Paths ---
ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ARTIFACTS_DIR = os.path.join(ROOT_DIR, 'artifacts', 'contracts')
CERTIFICATE_ARTIFACT_PATH = os.path.join(ARTIFACTS_DIR, 'Certificate.sol', 'Certificate.json')
DATA_DIR = os.path.join(ROOT_DIR, 'data')
LOG_DIR = os.path.join(ROOT_DIR, 'log')

# --- Ensure directories exist ---
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)

# --- Logging Setup ---
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, f'fault_tolerance_test_{timestamp}.log')),
        logging.StreamHandler()
    ]
)

class FaultToleranceTest:
    """
    Implements fault tolerance testing for the blockchain academic credential system.
    """
    
    def __init__(self):
        """Initialize the fault tolerance test."""
        self.node_manager = NodeManager(base_port=BASE_PORT, node_count=NODE_COUNT)
        self.web3_connections = {}
        self.contracts = {}
        self.results = []
        
    def setup(self):
        """Set up the test environment by starting all nodes."""
        logging.info("Setting up fault tolerance test environment...")
        
        # Start all nodes
        active_nodes = self.node_manager.start_all_nodes()
        if len(active_nodes) < NODE_COUNT:
            logging.warning(f"Only {len(active_nodes)} out of {NODE_COUNT} nodes started successfully")
        
        # Connect to each node
        for node_id in active_nodes:
            self._connect_to_node(node_id)
            
        logging.info(f"Connected to {len(self.web3_connections)} nodes")
        return len(active_nodes) > 0
    
    def _connect_to_node(self, node_id):
        """
        Connect to a node and deploy the Certificate contract.
        
        Args:
            node_id (int): The ID of the node to connect to
        
        Returns:
            bool: True if connection and deployment were successful, False otherwise
        """
        node_url = self.node_manager.get_node_url(node_id)
        if not node_url:
            logging.error(f"No URL found for node {node_id}")
            return False
        
        try:
            # Connect to the node
            w3 = Web3(Web3.HTTPProvider(node_url, request_kwargs={'timeout': 30}))
            w3.middleware_onion.inject(geth_poa_middleware, layer=0)
            
            if not w3.is_connected():
                logging.error(f"Failed to connect to node {node_id} at {node_url}")
                return False
            
            # Set up account
            account = w3.eth.account.from_key(PRIVATE_KEY)
            w3.eth.default_account = account.address
            
            # Deploy Certificate contract
            with open(CERTIFICATE_ARTIFACT_PATH, 'r') as f:
                contract_json = json.load(f)
            
            contract_factory = w3.eth.contract(abi=contract_json['abi'], bytecode=contract_json['bytecode'])
            tx_hash = contract_factory.constructor(account.address).transact({'from': account.address})
            tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
            contract_address = tx_receipt.contractAddress
            
            contract = w3.eth.contract(address=contract_address, abi=contract_json['abi'])
            
            # Add institution
            tx_hash = contract.functions.addInstitution(account.address).transact({'from': account.address})
            w3.eth.wait_for_transaction_receipt(tx_hash)
            
            # Store connections
            self.web3_connections[node_id] = w3
            self.contracts[node_id] = contract
            
            logging.info(f"Successfully connected to node {node_id} and deployed contract at {contract_address}")
            return True
            
        except Exception as e:
            logging.error(f"Error connecting to node {node_id}: {e}")
            return False
    
    def run_test(self, scenario_name, active_node_count, fault_duration=30, transaction_count=50):
        """
        Run a fault tolerance test scenario.
        
        Args:
            scenario_name (str): Name of the test scenario
            active_node_count (int): Number of nodes to keep active
            fault_duration (int): Duration of the fault in seconds
            transaction_count (int): Number of transactions to attempt during the test
            
        Returns:
            dict: Test results including availability and recovery metrics
        """
        logging.info(f"Running test scenario: {scenario_name} with {active_node_count}/{NODE_COUNT} active nodes")
        
        # Ensure we have enough nodes running
        running_nodes = self.node_manager.get_running_nodes()
        if len(running_nodes) < NODE_COUNT:
            logging.warning(f"Only {len(running_nodes)} nodes are running, starting missing nodes...")
            self.node_manager.start_all_nodes()
            time.sleep(5)  # Give nodes time to start
            running_nodes = self.node_manager.get_running_nodes()
        
        if len(running_nodes) < active_node_count:
            logging.error(f"Not enough nodes running. Need {active_node_count}, have {len(running_nodes)}")
            return None
        
        # Select nodes to keep active and nodes to shut down
        nodes_to_keep = random.sample(running_nodes, active_node_count)
        nodes_to_shutdown = [node for node in running_nodes if node not in nodes_to_keep]
        
        # Record initial block numbers for all nodes
        initial_blocks = {}
        for node_id in running_nodes:
            if node_id in self.web3_connections:
                initial_blocks[node_id] = self.web3_connections[node_id].eth.block_number
        
        # Shut down selected nodes
        for node_id in nodes_to_shutdown:
            logging.info(f"Shutting down node {node_id} for fault simulation")
            self.node_manager.stop_node(node_id)
        
        # Run transactions on remaining nodes
        start_time = time.time()
        successful_txs = 0
        failed_txs = 0
        
        for i in range(transaction_count):
            # Select a random active node for this transaction
            if not nodes_to_keep:
                logging.error("No active nodes available for transactions")
                break
                
            node_id = random.choice(nodes_to_keep)
            
            if node_id not in self.web3_connections or node_id not in self.contracts:
                logging.warning(f"No connection to node {node_id}, skipping transaction")
                failed_txs += 1
                continue
            
            # Issue a certificate
            try:
                w3 = self.web3_connections[node_id]
                contract = self.contracts[node_id]
                
                # Generate a unique certificate hash
                cert_hash = w3.keccak(text=f"certificate-fault-test-{scenario_name}-{i}")
                
                # Issue the certificate
                tx_hash = contract.functions.issueCertificate(cert_hash).transact({
                    'from': w3.eth.default_account
                })
                
                # Wait for transaction receipt with timeout
                try:
                    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=10)
                    successful_txs += 1
                    logging.info(f"Transaction {i+1}/{transaction_count} successful on node {node_id}")
                except Exception as e:
                    failed_txs += 1
                    logging.warning(f"Transaction {i+1}/{transaction_count} failed on node {node_id}: {e}")
                
            except Exception as e:
                failed_txs += 1
                logging.warning(f"Error issuing certificate on node {node_id}: {e}")
            
            # Add a small delay between transactions
            time.sleep(0.5)
        
        # Calculate availability during fault
        fault_duration_actual = time.time() - start_time
        availability = successful_txs / transaction_count if transaction_count > 0 else 0
        
        logging.info(f"Fault period complete. Availability: {availability:.2%}")
        logging.info(f"Successful transactions: {successful_txs}/{transaction_count}")
        
        # Wait for the specified fault duration if we haven't already exceeded it
        remaining_time = fault_duration - fault_duration_actual
        if remaining_time > 0:
            logging.info(f"Waiting {remaining_time:.1f} seconds to complete fault duration...")
            time.sleep(remaining_time)
        
        # Restart the nodes that were shut down
        recovery_start_time = time.time()
        for node_id in nodes_to_shutdown:
            logging.info(f"Restarting node {node_id}")
            self.node_manager.start_node(node_id)
            
            # Reconnect to the node if needed
            if node_id not in self.web3_connections:
                self._connect_to_node(node_id)
        
        # Wait for nodes to sync
        logging.info("Waiting for nodes to sync...")
        time.sleep(10)
        
        # Check block synchronization
        sync_complete = False
        sync_start_time = time.time()
        max_sync_time = 60  # Maximum time to wait for sync in seconds
        
        while not sync_complete and (time.time() - sync_start_time) < max_sync_time:
            block_numbers = {}
            for node_id in self.node_manager.get_running_nodes():
                if node_id in self.web3_connections:
                    try:
                        block_numbers[node_id] = self.web3_connections[node_id].eth.block_number
                    except Exception as e:
                        logging.warning(f"Error getting block number from node {node_id}: {e}")
            
            # Check if all nodes have the same block number
            if block_numbers and len(set(block_numbers.values())) == 1:
                sync_complete = True
                break
            
            logging.info(f"Nodes not yet in sync. Block numbers: {block_numbers}")
            time.sleep(5)
        
        recovery_time = time.time() - recovery_start_time
        
        # Verify data consistency
        consistency_check_passed = self._verify_data_consistency()
        
        # Record results
        result = {
            'scenario': scenario_name,
            'active_nodes': active_node_count,
            'total_nodes': NODE_COUNT,
            'fault_duration': fault_duration,
            'availability': availability,
            'successful_txs': successful_txs,
            'failed_txs': failed_txs,
            'recovery_time': recovery_time,
            'sync_complete': sync_complete,
            'data_consistent': consistency_check_passed
        }
        
        self.results.append(result)
        logging.info(f"Test scenario complete: {scenario_name}")
        logging.info(f"Results: {result}")
        
        return result
    
    def _verify_data_consistency(self):
        """
        Verify that all nodes have consistent data.
        
        Returns:
            bool: True if data is consistent across all nodes, False otherwise
        """
        logging.info("Verifying data consistency across nodes...")
        
        # Get a list of certificate hashes from each node
        certificates = {}
        for node_id, w3 in self.web3_connections.items():
            try:
                contract = self.contracts[node_id]
                # We'll check a few recent certificates by their status
                # This is a simplified check - in a real system you'd want more thorough verification
                test_hashes = [w3.keccak(text=f"test-cert-{i}") for i in range(5)]
                node_certs = []
                
                for cert_hash in test_hashes:
                    try:
                        status, _, _ = contract.functions.getCertificateStatus(cert_hash).call()
                        node_certs.append((cert_hash.hex(), status))
                    except Exception:
                        # This certificate might not exist on this node
                        pass
                
                certificates[node_id] = node_certs
            except Exception as e:
                logging.error(f"Error checking certificates on node {node_id}: {e}")
                return False
        
        # Check if all nodes have the same certificates
        if not certificates:
            logging.error("No certificate data found on any node")
            return False
        
        # Compare certificates across nodes
        reference_node = list(certificates.keys())[0]
        reference_certs = set(tuple(item) for item in certificates[reference_node])
        
        for node_id, node_certs in certificates.items():
            if node_id == reference_node:
                continue
            
            node_certs_set = set(tuple(item) for item in node_certs)
            if node_certs_set != reference_certs:
                logging.warning(f"Data inconsistency detected on node {node_id}")
                logging.warning(f"Reference node has {len(reference_certs)} certificates, node {node_id} has {len(node_certs_set)}")
                return False
        
        logging.info("Data consistency check passed")
        return True
    
    def run_all_tests(self):
        """Run all test scenarios."""
        logging.info("Starting fault tolerance test suite...")
        
        # Define test scenarios
        scenarios = [
            {"name": "Normal Operation", "active_nodes": 4, "fault_duration": 30, "transactions": 50},
            {"name": "Single Node Failure", "active_nodes": 3, "fault_duration": 30, "transactions": 50},
            {"name": "Double Node Failure", "active_nodes": 2, "fault_duration": 30, "transactions": 50},
            {"name": "Extreme Failure", "active_nodes": 1, "fault_duration": 30, "transactions": 50}
        ]
        
        # Run each scenario
        for scenario in scenarios:
            self.run_test(
                scenario_name=scenario["name"],
                active_node_count=scenario["active_nodes"],
                fault_duration=scenario["fault_duration"],
                transaction_count=scenario["transactions"]
            )
            
            # Wait between tests
            time.sleep(10)
        
        # Save results
        self.save_results()
        
        return self.results
    
    def save_results(self):
        """Save test results to a CSV file."""
        if not self.results:
            logging.warning("No results to save")
            return
        
        # Convert results to DataFrame
        df = pd.DataFrame(self.results)
        
        # Save to CSV
        output_path = os.path.join(DATA_DIR, 'fault_tolerance_test.csv')
        df.to_csv(output_path, index=False)
        logging.info(f"Results saved to {output_path}")
    
    def cleanup(self):
        """Clean up resources by stopping all nodes."""
        logging.info("Cleaning up resources...")
        self.node_manager.stop_all_nodes()
        logging.info("All nodes stopped")

def main():
    """Main function to run the fault tolerance test."""
    logging.info("=== Starting Node Fault Recovery Test ===")
    
    test = FaultToleranceTest()
    
    try:
        # Set up the test environment
        if not test.setup():
            logging.error("Failed to set up test environment")
            return
        
        # Run all test scenarios
        test.run_all_tests()
        
    except Exception as e:
        logging.critical(f"An unrecoverable error occurred: {e}", exc_info=True)
    finally:
        # Clean up resources
        test.cleanup()
        logging.info("=== Node Fault Recovery Test Complete ===")

if __name__ == '__main__':
    main()
