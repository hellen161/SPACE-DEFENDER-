import pygame
import random

class PowerUp:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = 20
        self.speed = 2
        
        types = ["shield", "triple", "rapid", "life"]
        self.type = random.choice(types)
        
        self.colors = {
            "shield": (0, 200, 255),
            "triple": (255, 200, 0),
            "rapid": (0, 255, 100),
            "life": (255, 50, 50)
        }
    
    def update(self):
        self.y += self.speed
    
    def draw(self, screen):
        color = self.colors[self.type]
        
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.size)
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), self.size, 2)
        
        if self.type == "shield":
            pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), 8, 2)
        
        elif self.type == "triple":
            pygame.draw.circle(screen, (255, 255, 255), (int(self.x - 6), int(self.y - 6)), 3)
            pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y + 6)), 3)
            pygame.draw.circle(screen, (255, 255, 255), (int(self.x + 6), int(self.y - 6)), 3)
        
        elif self.type == "rapid":
            pygame.draw.line(screen, (255, 255, 255), (self.x - 8, self.y), (self.x + 8, self.y), 3)
            pygame.draw.line(screen, (255, 255, 255), (self.x, self.y - 8), (self.x, self.y + 8), 3)
        
        elif self.type == "life":
            pygame.draw.polygon(screen, (255, 255, 255), [
                (self.x, self.y - 8),
                (self.x - 6, self.y + 4),
                (self.x + 6, self.y + 4)
            ])