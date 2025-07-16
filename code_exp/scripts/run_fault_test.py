"""
Script to run the fault tolerance test with a custom base port
"""

import os
import sys
from fault_tolerance_test import main as run_fault_test

# Set a different base port to avoid conflict with the running Hardhat node
os.environ['BASE_PORT'] = '9545'  # Use a different port range starting from 9545

if __name__ == '__main__':
    print("Starting fault tolerance test with base port 9545...")
    run_fault_test()
