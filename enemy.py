import pygame
import random
import time
import logging
from enum import Enum


class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 10
        self.speed = 0.5
        
    def move_towards(self, target):
        dx = target.x - self.x
        dy = target.y - self.y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        
        if distance != 0:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed
            
    def draw(self, screen):
        pygame.draw.rect(screen, (128, 128, 128), 
                        (self.x, self.y, self.size, self.size))
