import pygame
import math

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.speed = 5
        self.lives = 3
        
        # Disparo
        self.shoot_cooldown = 0
        self.shoot_delay = 10
        self.bullet_speed = 10
        
        # Special attack
        self.special_cooldown = 0
        self.special_delay = 180  # 3 segundos
        
        # Power-ups
        self.has_shield = False
        self.shield_time = 0
        self.triple_shot = False
        self.triple_time = 0
        self.rapid_fire = False
        self.rapid_time = 0
        
        # Hitbox
        self.rect = pygame.Rect(self.x - self.width//2, self.y - self.height//2, 
                               self.width, self.height)
    
    def update(self, keys):
        # Movimento
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.x += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.y -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.y += self.speed
        
        # Limites da tela
        self.x = max(self.width//2, min(self.x, 800 - self.width//2))
        self.y = max(self.height//2, min(self.y, 600 - self.height//2))
        
        # Atualiza cooldowns
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        
        if self.special_cooldown > 0:
            self.special_cooldown -= 1
        
        # Atualiza power-ups
        if self.has_shield:
            self.shield_time -= 1
            if self.shield_time <= 0:
                self.has_shield = False
        
        if self.triple_shot:
            self.triple_time -= 1
            if self.triple_time <= 0:
                self.triple_shot = False
        
        if self.rapid_fire:
            self.rapid_time -= 1
            if self.rapid_time <= 0:
                self.rapid_fire = False
                self.shoot_delay = 10
        
        # Atualiza hitbox
        self.rect.center = (self.x, self.y)
    
    def shoot(self):
        from scripts.bullet import PlayerBullet
        bullets = []
        
        if self.shoot_cooldown <= 0:
            # Disparo normal
            bullets.append(PlayerBullet(self.x, self.y - 20, 0, -self.bullet_speed))
            
            # Tiro triplo
            if self.triple_shot:
                bullets.append(PlayerBullet(self.x - 15, self.y - 10, -1, -self.bullet_speed))
                bullets.append(PlayerBullet(self.x + 15, self.y - 10, 1, -self.bullet_speed))
            
            # Configura cooldown
            if self.rapid_fire:
                self.shoot_cooldown = 5
            else:
                self.shoot_cooldown = self.shoot_delay
        
        return bullets
    
    def special_attack(self):
        from scripts.bullet import SpecialBullet
        bullets = []
        
        if self.special_cooldown <= 0:
            # Cria 8 balas em todas as direções
            for angle in range(0, 360, 45):
                rad = math.radians(angle)
                dx = math.sin(rad) * 8
                dy = math.cos(rad) * 8
                bullets.append(SpecialBullet(self.x, self.y, dx, -dy))
            
            self.special_cooldown = self.special_delay
        
        return bullets
    
    def take_damage(self):
        if not self.has_shield:
            self.lives -= 1
            return self.lives <= 0
        return False
    
    def add_powerup(self, powerup_type):
        if powerup_type == "shield":
            self.has_shield = True
            self.shield_time = 300  # 5 segundos
        
        elif powerup_type == "triple":
            self.triple_shot = True
            self.triple_time = 600  # 10 segundos
        
        elif powerup_type == "rapid":
            self.rapid_fire = True
            self.rapid_time = 450  # 7.5 segundos
            self.shoot_delay = 5
        
        elif powerup_type == "life":
            self.lives += 1
    
    def draw(self, screen):
        # Desenha nave (triângulo)
        points = [
            (self.x, self.y - 20),           # Topo
            (self.x - 15, self.y + 10),      # Inferior esquerdo
            (self.x + 15, self.y + 10)       # Inferior direito
        ]
        pygame.draw.polygon(screen, (0, 200, 255), points)
        
        # Detalhes da nave
        pygame.draw.polygon(screen, (100, 255, 255), points, 2)
        pygame.draw.line(screen, (255, 100, 0), (self.x, self.y + 10), 
                        (self.x, self.y + 20), 3)
        
        # Escudo
        if self.has_shield:
            pygame.draw.circle(screen, (0, 255, 255, 100), 
                             (self.x, self.y), 25, 2)