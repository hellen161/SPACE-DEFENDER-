import pygame

class Bullet:
    def __init__(self, x, y, dx, dy, damage=1):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy
        self.damage = damage
        self.width = 4
        self.height = 8
    
    def update(self):
        self.x += self.dx
        self.y += self.dy
    
    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 0), 
                        (self.x - 2, self.y - 4, 4, 8))

class PlayerBullet(Bullet):
    def __init__(self, x, y, dx, dy):
        super().__init__(x, y, dx, dy, 1)
        self.width = 6
        self.height = 12
    
    def draw(self, screen):
        # Balas do player (laser azul)
        points = [
            (self.x - 3, self.y + 6),
            (self.x, self.y - 6),
            (self.x + 3, self.y + 6)
        ]
        pygame.draw.polygon(screen, (0, 200, 255), points)

class SpecialBullet(Bullet):
    def __init__(self, x, y, dx, dy):
        super().__init__(x, y, dx, dy, 3)
        self.width = 8
        self.height = 8
    
    def draw(self, screen):
        # Balas especiais (estrelas)
        pygame.draw.circle(screen, (255, 255, 0), (int(self.x), int(self.y)), 4)
        pygame.draw.circle(screen, (255, 100, 0), (int(self.x), int(self.y)), 2)

class EnemyBullet(Bullet):
    def __init__(self, x, y, dx, dy, damage=1):
        super().__init__(x, y, dx, dy, damage)
        self.width = 6
        self.height = 6
    
    def draw(self, screen):
        # Balas inimigas (laser vermelho)
        pygame.draw.circle(screen, (255, 50, 50), (int(self.x), int(self.y)), 3)
        pygame.draw.circle(screen, (255, 150, 150), (int(self.x), int(self.y)), 1)