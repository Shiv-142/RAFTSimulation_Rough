import pygame
import random
import time
import logging
from enum import Enum
from events import *
import threading


class NodeState(Enum):
    FOLLOWER = 1
    CANDIDATE = 2
    LEADER = 3
    DEAD = 4

class Node(threading.Thread):
    def __init__(self, id, x, y, size, total_nodes):
        threading.Thread.__init__(self)
        self.id = id
        self.x = x
        self.y = y
        self.size = size
        self.state = NodeState.FOLLOWER
        self.health = 100
        self.term = 0
        self.votes_received = 0
        self.election_timeout = random.uniform(7, 25)
        self.last_heartbeat = time.time()
        self.total_nodes = total_nodes
        self.voted_for = {}
        self.vote_request_timeout = 8
        self.last_vote_request = time.time()
        self.leader_id = None

        # Log-related attributes
        self.commit_log = []
        self.pending_log = None
        self.last_committed_index = -1
        self.is_active = True
        self.running = True
        
        # Thread-safe locks
        self.state_lock = threading.Lock()
        self.log_lock = threading.Lock()
        
    def run(self):
        """Main thread loop for node"""
        while self.running:
            current_time = time.time()
            
            with self.state_lock:
                if self.is_active:
                    # Leader sends heartbeats
                    if self.state == NodeState.LEADER:
                        if current_time - self.last_heartbeat >= 5:  # Heartbeat interval
                            self.send_heartbeat()
                            self.last_heartbeat = current_time
                    
                    # Followers check for election timeout
                    elif self.state == NodeState.FOLLOWER:
                        if current_time - self.last_heartbeat >= self.election_timeout:
                            print(f"Node {self.id} starting election")
                            self.start_election()

                    elif self.state == NodeState.CANDIDATE:
                        if current_time - self.last_vote_request >= self.vote_request_timeout:
                            self.send_vote_request()
            time.sleep(0.01)


    def stop(self):
        """Stop the node thread"""
        self.running = False

    def handle_heartbeat(self, from_id, term):
        if(self.state == NodeState.DEAD):
            return
        """Handle heartbeat from another node"""
        with self.state_lock:
            if self.state == NodeState.FOLLOWER:
                self.last_heartbeat = time.time()
                self.is_active = True
                self.term = term
                self
                event = pygame.event.Event(HEARTBEAT_RECEIVED, {
                    'from_id': from_id,
                    'term': term,
                    'from_x': self.x,
                    'from_y': self.y
                })
                
                pygame.event.post(event)
            elif self.state == NodeState.CANDIDATE:
                if term > self.term:
                    self.state = NodeState.FOLLOWER
                    self.last_heartbeat = time.time()
                    self.is_active = True
                    self.term = term
            elif self.state == NodeState.LEADER:
                self.last_heartbeat = time.time()

            """if term > self.term:
                self.term = term
                self.state = NodeState.FOLLOWER
                self.voted_for = None
            """
            # Log the heartbeat
        
    def handle_vote_request(self, candidate_id, term):
        if(self.state == NodeState.DEAD):
            return
        """Handle vote request from another node"""
        print(f"Node {self.id} received vote request from {candidate_id}")
        with self.state_lock:
            if term >= self.term and (self.voted_for.get(term) is None):
                self.voted_for[term] = candidate_id
                self.state = NodeState.FOLLOWER
                self.is_active = True
                event = pygame.event.Event(VOTE_RESPONSE, {
                    'voter_id': self.id,
                    'candidate_id': candidate_id,
                    'term': term
                })
                pygame.event.post(event)
    def send_heartbeat(self):
        if(self.state == NodeState.DEAD):
            return
        """Send heartbeat to all nodes"""
        event = pygame.event.Event(HEARTBEAT_SENT, {
            'from_id': self.id,
            'term': self.term,
            'from_x': self.x + self.size/2,
            'from_y': self.y + self.size/2
        })
        pygame.event.post(event)
    
    def handle_vote_response(self, voter_id, candidate_id, term):
        if(self.state == NodeState.DEAD):
            return
        """Handle vote response from another node"""
        with self.state_lock:
            if self.state == NodeState.CANDIDATE and term == self.term and candidate_id == self.id:
                self.votes_received += 1
                print(f"Votes recieved {self.votes_received}")
                if self.votes_received > (self.total_nodes // 2):
                    self.state = NodeState.LEADER
                    self.is_active = True
                    votes_received = 0
                    event = pygame.event.Event(ELECTION_COMPLETE, {
                        'leader_id': self.id,
                        'term': self.term
                    })
                    eventHB = pygame.event.Event(HEARTBEAT_SENT, {
                        'from_id': self.id,
                        'term': self.term,
                        'from_x': self.x + self.size/2,
                        'from_y': self.y + self.size/2
                    })
                    self.last_heartbeat = time.time()
                    pygame.event.post(event)
                    pygame.event.post(eventHB)


    def send_vote_request(self):
        if(self.state == NodeState.DEAD):
            return
        print(f"Node {self.id} sending vote request send_vote_request")
        self.last_vote_request = time.time()
        """Send vote request to all nodes"""
        event = pygame.event.Event(VOTE_REQUEST, {
            'candidate_id': self.id,
            'term': self.term
        })
        pygame.event.post(event)
    

    def start_election(self):
        if(self.state == NodeState.DEAD):
            return
        """Start an election"""
        print(f"Node {self.id} starting election start_election")
        
        self.state = NodeState.CANDIDATE
        self.term += 1
        self.votes_received = 1  # Vote for self
        self.voted_for[self.term] = self.id
        print(f"Node {self.id} starting election start_election with LOCK")
        self.send_vote_request()
            

    def handle_click(self):
        if(self.state == NodeState.DEAD):
            self.health+=10
            if(self.health > 100):
                self.state = NodeState.FOLLOWER
                self.election_timeout = random.uniform(7, 25)
                self.last_heartbeat = time.time()
                self.is_active = True
                self.health = 100
        
    def draw(self, screen):
        """Draw node on screen"""
        with self.state_lock:
            base_color = (0, 255, 0) if self.state == NodeState.LEADER else \
                        (255, 165, 0) if self.state == NodeState.CANDIDATE else \
                        (0, 0, 255) if self.state == NodeState.FOLLOWER else \
                        (255, 0, 0)
            color = base_color if self.is_active else tuple(c // 2 for c in base_color)
            pygame.draw.rect(screen, color, (self.x, self.y, self.size, self.size))
