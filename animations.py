import time
import pygame

class HeartbeatAnimation:
    def __init__(self, x, y, color=(0, 255, 0), duration=1.0):
        self.x = x
        self.y = y
        self.color = color
        self.start_time = time.time()
        self.duration = duration
        self.max_radius = 100  # Maximum radius of the wave
        
    def draw(self, screen):
        current_time = time.time()
        age = current_time - self.start_time
        
        if age > self.duration:
            return False  # Animation is complete
        
        # Calculate current radius and alpha
        progress = age / self.duration
        current_radius = self.max_radius * progress
        alpha = int(255 * (1 - progress))  # Fade out as circle expands
        
        # Create a surface for the circle with transparency
        surface = pygame.Surface((current_radius * 2, current_radius * 2), pygame.SRCALPHA)
        
        # Draw the circle with transparency
        pygame.draw.circle(surface, (*self.color, alpha), 
                         (current_radius, current_radius), 
                         current_radius, 2)  # Width of 2 pixels
        
        # Blit the surface onto the screen
        screen.blit(surface, 
                   (self.x - current_radius, 
                    self.y - current_radius))
        
        return True  # Animation still running


class TextAnimation:
    def __init__(self, x, y, color=(0, 0, 0), duration=1.0):
        self.x = x
        self.y = y
        self.color = color
        self.start_time = time.time()
        self.duration = duration
        self.start_size = 20
        self.max_size = 40
        self.text = "HB RECEIVED"
        
    def draw(self, screen):
        current_time = time.time()
        age = current_time - self.start_time
        
        if age > self.duration:
            return False  # Animation is complete
        
        # Calculate current size and alpha
        progress = age / self.duration
        current_size = self.start_size + (self.max_size - self.start_size) * progress
        alpha = int(255 * (1 - progress))  # Fade out
        
        # Create font with current size
        font = pygame.font.Font(None, int(current_size))
        
        # Render text with transparency
        text_surface = font.render(self.text, True, self.color)
        text_surface.set_alpha(alpha)
        
        # Get text rect for centered positioning
        text_rect = text_surface.get_rect(center=(self.x, self.y))
        # Draw the text
        screen.blit(text_surface, text_rect)

        return True  # Animation still running

class ResetAnimation:
    def __init__(self, x, y, color=(0, 0, 0), duration=1.0):
        self.x = x
        self.y = y
        self.color = color
        self.start_time = time.time()
        self.duration = duration
        self.start_size = 40
        self.max_size = 80
        self.text = "MAJORITY RAFT DOWN: RESETTING"
        
    def draw(self, screen):
        current_time = time.time()
        age = current_time - self.start_time
        
        if age > self.duration:
            return False  # Animation is complete
        
        # Calculate current size and alpha
        progress = age / self.duration
        current_size = self.start_size + (self.max_size - self.start_size) * progress
        alpha = int(255 * (1 - progress))  # Fade out
        
        # Create font with current size
        font = pygame.font.Font(None, int(current_size))
        
        # Render text with transparency
        text_surface = font.render(self.text, True, self.color)
        text_surface.set_alpha(alpha)
        
        # Get text rect for centered positioning
        text_rect = text_surface.get_rect(center=(self.x, self.y))
        
        # Draw the text
        screen.blit(text_surface, text_rect)
        
        return True  # Animation still running
