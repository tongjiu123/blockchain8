"""
Node Manager for Fault Tolerance Testing

This module provides functionality to manage multiple Hardhat nodes for fault tolerance testing.
It allows starting, stopping, and monitoring the status of nodes.
"""

import os
import time
import signal
import logging
import subprocess
import socket
import json
import requests
from web3 import Web3

class NodeManager:
    """Manages multiple Hardhat nodes for fault tolerance testing."""
    
    def __init__(self, base_port=8545, node_count=4):
        """
        Initialize the NodeManager.
        
        Args:
            base_port (int): The starting port number for the first node
            node_count (int): The number of nodes to manage
        """
        self.base_port = base_port
        self.node_count = node_count
        self.nodes = {}  # Dictionary to store node processes
        self.node_urls = {}  # Dictionary to store node URLs
        self.log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'log')
        os.makedirs(self.log_dir, exist_ok=True)
        
    def start_node(self, node_id):
        """
        Start a Hardhat node with the given ID.
        
        Args:
            node_id (int): The ID of the node to start
            
        Returns:
            bool: True if the node was started successfully, False otherwise
        """
        if node_id in self.nodes and self.is_node_running(node_id):
            logging.info(f"Node {node_id} is already running")
            return True
            
        port = self.base_port + node_id
        logging.info(f"Starting node {node_id} on port {port}...")
        
        # Check if the port is already in use
        if self._is_port_in_use(port):
            logging.error(f"Port {port} is already in use. Cannot start node {node_id}.")
            return False
            
        # Create log file for this node
        log_file = open(os.path.join(self.log_dir, f'node_{node_id}.log'), 'w')
        
        # Start the Hardhat node with the specified port
        try:
            process = subprocess.Popen(
                ['npx', 'hardhat', 'node', '--hostname', '127.0.0.1', '--port', str(port)],
                stdout=log_file,
                stderr=log_file,
                cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            )
            
            self.nodes[node_id] = process
            self.node_urls[node_id] = f"http://127.0.0.1:{port}"
            
            # Wait for the node to start
            time.sleep(2)
            
            # Check if the node is running
            if not self.is_node_running(node_id):
                logging.error(f"Failed to start node {node_id}")
                return False
                
            logging.info(f"Node {node_id} started successfully on port {port}")
            return True
            
        except Exception as e:
            logging.error(f"Error starting node {node_id}: {e}")
            return False
    
    def stop_node(self, node_id):
        """
        Stop a running Hardhat node.
        
        Args:
            node_id (int): The ID of the node to stop
            
        Returns:
            bool: True if the node was stopped successfully, False otherwise
        """
        if node_id not in self.nodes:
            logging.warning(f"Node {node_id} is not managed by this NodeManager")
            return False
            
        if not self.is_node_running(node_id):
            logging.info(f"Node {node_id} is not running")
            return True
            
        logging.info(f"Stopping node {node_id}...")
        
        try:
            # Send SIGTERM to the process
            self.nodes[node_id].terminate()
            
            # Wait for the process to terminate
            for _ in range(5):  # Wait up to 5 seconds
                if not self.is_node_running(node_id):
                    break
                time.sleep(1)
                
            # If the process is still running, kill it
            if self.is_node_running(node_id):
                self.nodes[node_id].kill()
                time.sleep(1)
                
            if not self.is_node_running(node_id):
                logging.info(f"Node {node_id} stopped successfully")
                return True
            else:
                logging.error(f"Failed to stop node {node_id}")
                return False
                
        except Exception as e:
            logging.error(f"Error stopping node {node_id}: {e}")
            return False
    
    def is_node_running(self, node_id):
        """
        Check if a node is running.
        
        Args:
            node_id (int): The ID of the node to check
            
        Returns:
            bool: True if the node is running, False otherwise
        """
        if node_id not in self.nodes:
            return False
            
        # First check if the process is running
        if self.nodes[node_id].poll() is not None:
            return False
            
        # Then check if the node is responding to RPC calls
        try:
            url = self.node_urls[node_id]
            response = requests.post(
                url,
                json={"jsonrpc": "2.0", "method": "eth_blockNumber", "params": [], "id": 1},
                timeout=2
            )
            return response.status_code == 200
        except:
            return False
    
    def start_all_nodes(self):
        """
        Start all nodes.
        
        Returns:
            list: List of node IDs that were started successfully
        """
        successful_nodes = []
        for node_id in range(self.node_count):
            if self.start_node(node_id):
                successful_nodes.append(node_id)
        return successful_nodes
    
    def stop_all_nodes(self):
        """
        Stop all running nodes.
        
        Returns:
            list: List of node IDs that were stopped successfully
        """
        successful_stops = []
        for node_id in self.nodes.keys():
            if self.stop_node(node_id):
                successful_stops.append(node_id)
        return successful_stops
    
    def get_running_nodes(self):
        """
        Get a list of currently running nodes.
        
        Returns:
            list: List of node IDs that are currently running
        """
        return [node_id for node_id in self.nodes.keys() if self.is_node_running(node_id)]
    
    def get_node_url(self, node_id):
        """
        Get the URL for a node.
        
        Args:
            node_id (int): The ID of the node
            
        Returns:
            str: The URL of the node, or None if the node is not managed by this NodeManager
        """
        return self.node_urls.get(node_id)
    
    def _is_port_in_use(self, port):
        """
        Check if a port is in use.
        
        Args:
            port (int): The port to check
            
        Returns:
            bool: True if the port is in use, False otherwise
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            return s.connect_ex(('127.0.0.1', port)) == 0
