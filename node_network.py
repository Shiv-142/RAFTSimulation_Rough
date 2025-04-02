import pygame
import random
import logging
from events import *
from node import NodeState, Node
import threading
import time

class NodeNetwork(threading.Thread):
    def __init__(self, nodes):
        # Existing initialization
        self.nodes = nodes
        self.leader = None
        self.heartbeat_interval = 500
        self.last_heartbeat = pygame.time.get_ticks()
        
        # New log-related attributes
        self.current_log_index = 0
        self.log_timeout = 2000  # Time to wait for acks before retry
        self.last_log_attempt = 0
        self.running = True

    

    def send_heartbeat(self):
        self.leader.sendHeartbeat()

    def receive_heartbeat(self, from_id, term):
        """Receive a heartbeat from a node"""
        for node in self.nodes:
            if node.id != self.leader.id:
                node.heartbeat_received()
    
    
    def run(self):
        """Main thread loop"""
        while self.running:
            current_time = time.time()
            
            # Send heartbeats
            if self.leader and current_time - self.last_heartbeat >= self.heartbeat_interval:
                self.send_heartbeat()
            
            """# Check for log timeouts
            if self.leader and self.leader.waiting_for_acks:
                if current_time - self.last_log_attempt >= self.log_timeout:
                    # Retry log replication
                    self.leader.waiting_for_acks = False
                    self.replicate_log(self.leader.pending_log.data)
            """
            # Sleep to prevent high CPU usage
            time.sleep(0.01)

