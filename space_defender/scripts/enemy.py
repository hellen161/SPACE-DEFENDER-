import pygame
import random
import math
from scripts.bullet import EnemyBullet

class Enemy:
    def __init__(self, x, y, width, height, speed, health, points, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.health = health
        self.max_health = health
        self.points = points
        self.color = color
        
        self.shoot_chance = 0.01
        self.bullet_speed = 4
        self.damage = 1
        self.powerup_chance = 0.1
        
        self.wobble = random.random() * math.pi * 2
    
    def update(self):
        self.y += self.speed
        self.x += math.sin(self.wobble) * 2
        self.wobble += 0.1
    
    def shoot(self):
        return EnemyBullet(self.x, self.y + 10, 0, self.bullet_speed, self.damage)
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, 
                        (self.x - self.width//2, self.y - self.height//2,
                         self.width, self.height))
        
        if self.health < self.max_health:
            health_width = (self.health / self.max_health) * self.width
            pygame.draw.rect(screen, (255, 0, 0),
                           (self.x - self.width//2, self.y - self.height//2 - 10,
                            self.width, 5))
            pygame.draw.rect(screen, (0, 255, 0),
                           (self.x - self.width//2, self.y - self.height//2 - 10,
                            health_width, 5))

class Scout(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, 20, 20, 2, 1, 10, (255, 100, 100))
        self.shoot_chance = 0.005
        self.speed = random.uniform(1.5, 2.5)
    
    def draw(self, screen):
        points = [
            (self.x, self.y - 10),
            (self.x + 10, self.y),
            (self.x, self.y + 10),
            (self.x - 10, self.y)
        ]
        pygame.draw.polygon(screen, self.color, points)

class Soldier(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, 30, 30, 1.5, 3, 25, (255, 150, 50))
        self.shoot_chance = 0.01
        self.bullet_speed = 5
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x - 15, self.y - 15, 30, 30))

class Tank(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 40, 1, 10, 50, (255, 50, 50))
        self.shoot_chance = 0.02
        self.bullet_speed = 3
        self.damage = 2
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x - 20, self.y - 20, 40, 40))
        pygame.draw.rect(screen, (100, 100, 100), (self.x - 5, self.y - 30, 10, 20))

class Boss(Enemy):
    def __init__(self, x, y):
        super().__init__(x, y, 80, 80, 0.5, 50, 200, (255, 0, 255))
        self.shoot_chance = 0.1
        self.bullet_speed = 4
        self.damage = 3
        self.powerup_chance = 1.0
        
        self.phase = 1
        self.phase_timer = 0
        self.move_x = 0
        self.move_speed = 2
    
    def update(self):
        self.x += self.move_x
        self.y += self.speed * 0.5
        
        if self.x < 100 or self.x > 700:
            self.move_x *= -1
        
        if self.move_x == 0:
            self.move_x = self.move_speed
        
        self.phase_timer += 1
        if self.phase_timer > 300:
            self.phase = 3 - self.phase
            self.phase_timer = 0
            self.move_x *= -1
    
    def shoot(self):
        bullets = []
        
        if self.phase == 1:
            for angle in [-30, 0, 30]:
                rad = math.radians(angle)
                dx = math.sin(rad) * 2
                dy = math.cos(rad) * self.bullet_speed
                bullets.append(EnemyBullet(self.x, self.y + 40, dx, dy, self.damage))
        else:
            for angle in range(0, 360, 45):
                rad = math.radians(angle)
                dx = math.sin(rad) * 3
                dy = math.cos(rad) * 3
                bullets.append(EnemyBullet(self.x, self.y + 40, dx, dy, self.damage))
        
        return bullets
    
    def check_collision(self, x, y):
        return (abs(x - self.x) < self.width//2 and 
                abs(y - self.y) < self.height//2)
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 40)
        pygame.draw.circle(screen, (255, 100, 255), (int(self.x), int(self.y)), 40, 3)
        
        pygame.draw.circle(screen, (255, 255, 0), (int(self.x - 15), int(self.y - 10)), 8)
        pygame.draw.circle(screen, (255, 255, 0), (int(self.x + 15), int(self.y - 10)), 8)
        pygame.draw.circle(screen, (0, 0, 0), (int(self.x - 15), int(self.y - 10)), 3)
        pygame.draw.circle(screen, (0, 0, 0), (int(self.x + 15), int(self.y - 10)), 3)
        
        pygame.draw.arc(screen, (255, 0, 0), 
                       (self.x - 20, self.y + 5, 40, 20),
                       0, math.pi, 3)
        
        # Barra de vida do boss
        health_width = (self.health / self.max_health) * 200
        pygame.draw.rect(screen, (255, 0, 0), (300, 20, 200, 20))
        pygame.draw.rect(screen, (0, 255, 0), (300, 20, health_width, 20))
        pygame.draw.rect(screen, (255, 255, 255), (300, 20, 200, 20), 2)