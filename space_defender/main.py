import pygame
import sys
import random
import math
import json

# ========== CLASSES BÁSICAS ==========

class Text:
    def __init__(self, text, x, y, size=36, color=(255,255,255)):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.font = pygame.font.Font(None, size)
        self.update()
    
    def update(self):
        self.surface = self.font.render(self.text, True, self.color)
        self.rect = self.surface.get_rect(center=(self.x, self.y))
    
    def draw(self, screen):
        screen.blit(self.surface, self.rect)

class Button:
    def __init__(self, text, x, y, w=200, h=50, color=(0,200,0), hover_color=(0,150,0)):
        self.text = text
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.hover_color = hover_color
        self.font = pygame.font.Font(None, 32)
        self.rect = pygame.Rect(x-w//2, y-h//2, w, h)
        self.is_hovering = False
    
    def update(self, mouse_pos):
        self.is_hovering = self.rect.collidepoint(mouse_pos)
    
    def draw(self, screen):
        color = self.hover_color if self.is_hovering else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, (255,255,255), self.rect, 3, border_radius=10)
        text_surf = self.font.render(self.text, True, (255,255,255))
        text_rect = text_surf.get_rect(center=(self.x, self.y))
        screen.blit(text_surf, text_rect)
    
    def is_clicked(self, mouse_pos, mouse_pressed):
        return self.rect.collidepoint(mouse_pos) and mouse_pressed[0]

# ========== CENAS DO JOGO ==========

class MenuScene:
    def __init__(self, game):
        self.game = game
        self.title = Text("SPACE DEFENDER", 400, 150, 64, (255, 255, 255))
        self.play_btn = Button("JOGAR", 400, 300, 200, 50, (0,200,0), (0,150,0))
        self.quit_btn = Button("SAIR", 400, 370, 200, 50, (200,0,0), (150,0,0))
        
        # Estrelas de fundo
        self.stars = []
        for _ in range(100):
            self.stars.append([random.randint(0, 800), random.randint(0, 600), 
                              random.uniform(0.5, 2), random.randint(1, 3)])
    
    def update(self):
        # Movimenta estrelas
        for star in self.stars:
            star[0] -= star[2]
            if star[0] < 0:
                star[0] = 800
                star[1] = random.randint(0, 600)
        
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        
        self.play_btn.update(mouse_pos)
        self.quit_btn.update(mouse_pos)
        
        if self.play_btn.is_clicked(mouse_pos, mouse_pressed):
            return "game"
        if self.quit_btn.is_clicked(mouse_pos, mouse_pressed):
            return "quit"
        
        return None
    
    def render(self, screen):
        # Fundo
        screen.fill((10, 10, 30))
        
        # Estrelas
        for x, y, speed, size in self.stars:
            brightness = 150 + int(speed * 50)
            pygame.draw.circle(screen, (brightness, brightness, 255), (int(x), int(y)), size)
        
        self.title.draw(screen)
        self.play_btn.draw(screen)
        self.quit_btn.draw(screen)
        
        # Instruções
        controls = [
            "CONTROLES:",
            "WASD ou SETAS - Movimentar",
            "ESPAÇO - Atirar",
            "SHIFT - Tiro Especial",
            "ESC - Voltar ao Menu"
        ]
        
        y_pos = 450
        for line in controls:
            text = pygame.font.Font(None, 24).render(line, True, (150, 150, 200))
            screen.blit(text, (400 - text.get_width()//2, y_pos))
            y_pos += 25

class GameScene:
    def __init__(self, game):
        self.game = game
        self.player_x = 400
        self.player_y = 500
        self.player_lives = 3
        self.player_speed = 5
        self.shoot_cooldown = 0
        self.special_cooldown = 0
        
        self.enemies = []
        self.bullets = []
        self.enemy_bullets = []
        self.powerups = []
        self.explosions = []
        
        self.wave = 1
        self.score = 0
        self.game_over = False
        
        self.spawn_timer = 0
        self.spawn_delay = 60
        self.enemies_to_spawn = 5
        self.enemies_spawned = 0
    
    def update(self):
        if self.game_over:
            self.game.score = self.score
            return "game_over"
        
        keys = pygame.key.get_pressed()
        
        # Movimento do player
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player_x -= self.player_speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player_x += self.player_speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.player_y -= self.player_speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.player_y += self.player_speed
        
        # Limites
        self.player_x = max(20, min(self.player_x, 780))
        self.player_y = max(20, min(self.player_y, 580))
        
        # Atirar
        if keys[pygame.K_SPACE] and self.shoot_cooldown <= 0:
            self.bullets.append([self.player_x, self.player_y - 20, 0, -10])
            self.shoot_cooldown = 10
        
        # Tiro especial
        if keys[pygame.K_LSHIFT] and self.special_cooldown <= 0:
            for angle in range(0, 360, 45):
                rad = math.radians(angle)
                self.bullets.append([self.player_x, self.player_y, 
                                   math.sin(rad)*8, -math.cos(rad)*8])
            self.special_cooldown = 180
        
        # Atualiza cooldowns
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
        if self.special_cooldown > 0:
            self.special_cooldown -= 1
        
        # Spawn inimigos
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_delay and self.enemies_spawned < self.enemies_to_spawn:
            x = random.randint(50, 750)
            self.enemies.append({
                'x': x, 'y': -30,
                'type': random.choice(['scout', 'soldier', 'tank']),
                'health': 1,
                'speed': random.uniform(1, 3)
            })
            self.enemies_spawned += 1
            self.spawn_timer = 0
        
        # Atualiza inimigos
        for enemy in self.enemies[:]:
            enemy['y'] += enemy['speed']
            
            # Colisão com balas
            for bullet in self.bullets[:]:
                bx, by = bullet[0], bullet[1]
                if (abs(bx - enemy['x']) < 20 and abs(by - enemy['y']) < 20):
                    enemy['health'] -= 1
                    if enemy['health'] <= 0:
                        self.score += 10
                        self.explosions.append([enemy['x'], enemy['y'], 0])
                        self.enemies.remove(enemy)
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    break
            
            # Se inimigo sair da tela
            if enemy['y'] > 650:
                self.enemies.remove(enemy)
                self.player_lives -= 1
                if self.player_lives <= 0:
                    self.game_over = True
        
        # Atualiza balas
        for bullet in self.bullets[:]:
            bullet[0] += bullet[2]
            bullet[1] += bullet[3]
            if bullet[1] < -20 or bullet[1] > 620:
                self.bullets.remove(bullet)
        
        # Atualiza explosões
        for explosion in self.explosions[:]:
            explosion[2] += 1
            if explosion[2] > 30:
                self.explosions.remove(explosion)
        
        # Verifica ESC para voltar ao menu
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return "menu"
        
        return None
    
    def render(self, screen):
        screen.fill((10, 10, 30))
        
        # Desenha player (triângulo)
        points = [(self.player_x, self.player_y-20), 
                 (self.player_x-15, self.player_y+10), 
                 (self.player_x+15, self.player_y+10)]
        pygame.draw.polygon(screen, (0, 200, 255), points)
        
        # Desenha inimigos
        for enemy in self.enemies:
            color = (255,100,100) if enemy['type'] == 'scout' else (255,150,50) if enemy['type'] == 'soldier' else (255,50,50)
            pygame.draw.circle(screen, color, (int(enemy['x']), int(enemy['y'])), 15)
        
        # Desenha balas
        for bullet in self.bullets:
            pygame.draw.circle(screen, (0, 200, 255), (int(bullet[0]), int(bullet[1])), 3)
        
        # Desenha explosões
        for x, y, timer in self.explosions:
            size = 10 + timer
            pygame.draw.circle(screen, (255, 200, 0), (int(x), int(y)), size, 2)
        
        # UI
        score_text = pygame.font.Font(None, 32).render(f"SCORE: {self.score}", True, (255,255,255))
        screen.blit(score_text, (10, 10))
        
        wave_text = pygame.font.Font(None, 32).render(f"WAVE: {self.wave}", True, (255,255,255))
        screen.blit(wave_text, (10, 50))
        
        lives_text = pygame.font.Font(None, 32).render(f"LIVES: {self.player_lives}", True, (255,255,255))
        screen.blit(lives_text, (10, 90))
        
        # Cooldown do special
        if self.special_cooldown > 0:
            width = 80 - (self.special_cooldown * 80 / 180)
            pygame.draw.rect(screen, (100,100,100), (700, 10, 80, 20))
            pygame.draw.rect(screen, (0,200,0), (700, 10, width, 20))
            special_text = pygame.font.Font(None, 16).render("SPECIAL", True, (255,255,255))
            screen.blit(special_text, (705, 12))

class GameOverScene:
    def __init__(self, game):
        self.game = game
        self.title = Text("GAME OVER", 400, 150, 64, (255, 50, 50))
        self.score_text = Text(f"SCORE: {game.score}", 400, 220, 48, (255,255,255))
        self.menu_btn = Button("MENU", 400, 350, 200, 50, (0,150,200), (0,100,150))
    
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()
        
        self.menu_btn.update(mouse_pos)
        
        if self.menu_btn.is_clicked(mouse_pos, mouse_pressed):
            return "menu"
        
        return None
    
    def render(self, screen):
        screen.fill((10, 10, 30))
        
        # Overlay escuro
        overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        self.title.draw(screen)
        self.score_text.draw(screen)
        self.menu_btn.draw(screen)

# ========== JOGO PRINCIPAL ==========

class Game:
    def __init__(self):
        pygame.init()
        self.WIDTH = 800
        self.HEIGHT = 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Space Defender")
        self.clock = pygame.time.Clock()
        
        self.score = 0
        self.current_scene = "menu"
    
    def run(self):
        scenes = {
            "menu": MenuScene(self),
            "game": GameScene(self),
            "game_over": GameOverScene(self)
        }
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            # Atualiza cena atual
            scene = scenes[self.current_scene]
            next_scene = scene.update()
            
            if next_scene == "quit":
                running = False
            elif next_scene:
                if next_scene == "game":
                    scenes["game"] = GameScene(self)
                self.current_scene = next_scene
            
            # Renderiza
            scene.render(self.screen)
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()