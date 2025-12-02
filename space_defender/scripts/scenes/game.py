import pygame
import random
from scripts.player import Player
from scripts.enemy import Scout, Soldier, Tank
from scripts.powerup import PowerUp

class GameScene:
    def __init__(self, game):
        self.game = game
        self.player = Player(400, 500)
        
        # Grupos de sprites
        self.enemies = []
        self.bullets = []
        self.enemy_bullets = []
        self.powerups = []
        self.explosions = []
        
        # Wave management
        self.wave = 1
        self.enemies_spawned = 0
        self.enemies_to_spawn = 5
        self.spawn_timer = 0
        self.spawn_delay = 60  # Frames entre spawns
        
        # Game state
        self.score = 0
        self.game_over = False
        self.game_over_timer = 0
        
        # Power-up spawn
        self.powerup_timer = 0
        self.powerup_chance = 0.01  # 1% chance por frame
        
        # Boss
        self.boss_active = False
        self.boss = None
        
        # UI
        self.score_text = f"SCORE: {self.score}"
        self.wave_text = f"WAVE: {self.wave}"
        self.lives_text = f"LIVES: {self.player.lives}"
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return "menu"
            if event.key == pygame.K_SPACE:
                if not self.game_over:
                    new_bullets = self.player.shoot()
                    self.bullets.extend(new_bullets)
            if event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT:
                if not self.game_over and self.player.special_cooldown <= 0:
                    self.bullets.extend(self.player.special_attack())
        return None
    
    def update(self):
        if self.game_over:
            self.game_over_timer += 1
            if self.game_over_timer > 180:  # 3 segundos
                self.game.score = self.score
                return "game_over"
            return None
        
        # Atualiza player
        keys = pygame.key.get_pressed()
        self.player.update(keys)
        
        # Spawn de inimigos
        self.spawn_timer += 1
        if (self.spawn_timer >= self.spawn_delay and 
            self.enemies_spawned < self.enemies_to_spawn and 
            not self.boss_active):
            
            # Escolhe tipo de inimigo baseado na wave
            enemy_types = []
            if self.wave >= 1:
                enemy_types.append(Scout)
            if self.wave >= 2:
                enemy_types.append(Soldier)
            if self.wave >= 3:
                enemy_types.append(Tank)
            
            enemy_type = random.choice(enemy_types)
            
            # Spawn em posição aleatória no topo
            x = random.randint(50, self.game.WIDTH - 50)
            enemy = enemy_type(x, -50)
            self.enemies.append(enemy)
            
            self.enemies_spawned += 1
            self.spawn_timer = 0
        
        # Check se wave acabou
        if (self.enemies_spawned >= self.enemies_to_spawn and 
            len(self.enemies) == 0 and 
            not self.boss_active):
            
            # A cada 5 waves, spawn boss
            if self.wave % 5 == 0:
                self.spawn_boss()
            else:
                self.next_wave()
        
        # Atualiza inimigos
        for enemy in self.enemies[:]:
            enemy.update()
            
            # Inimigos atiram
            if random.random() < enemy.shoot_chance:
                bullet = enemy.shoot()
                if bullet:
                    self.enemy_bullets.append(bullet)
            
            # Check se inimigo saiu da tela
            if enemy.y > self.game.HEIGHT + 50:
                self.enemies.remove(enemy)
                self.player.lives -= 1
                if self.player.lives <= 0:
                    self.game_over = True
            
            # Colisão com balas do player
            for bullet in self.bullets[:]:
                if (bullet.x > enemy.x - enemy.width//2 and 
                    bullet.x < enemy.x + enemy.width//2 and
                    bullet.y > enemy.y - enemy.height//2 and
                    bullet.y < enemy.y + enemy.height//2):
                    
                    enemy.health -= bullet.damage
                    if enemy.health <= 0:
                        self.score += enemy.points
                        self.create_explosion(enemy.x, enemy.y)
                        self.enemies.remove(enemy)
                        
                        # Chance de drop de power-up
                        if random.random() < enemy.powerup_chance:
                            self.powerups.append(PowerUp(enemy.x, enemy.y))
                    
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    break
        
        # Atualiza boss
        if self.boss_active and self.boss:
            self.boss.update()
            if random.random() < 0.05:  # 5% chance por frame
                bullets = self.boss.shoot()
                self.enemy_bullets.extend(bullets)
            
            # Colisão com balas do player
            for bullet in self.bullets[:]:
                if self.boss.check_collision(bullet.x, bullet.y):
                    self.boss.health -= bullet.damage
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    
                    if self.boss.health <= 0:
                        self.score += self.boss.points
                        self.create_explosion(self.boss.x, self.boss.y, large=True)
                        self.boss_active = False
                        self.boss = None
                        self.next_wave()
                    break
        
        # Atualiza balas do player
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.y < -20 or bullet.y > self.game.HEIGHT + 20:
                self.bullets.remove(bullet)
        
        # Atualiza balas inimigas
        for bullet in self.enemy_bullets[:]:
            bullet.update()
            if bullet.y < -20 or bullet.y > self.game.HEIGHT + 20:
                self.enemy_bullets.remove(bullet)
            
            # Colisão com player
            if (bullet.x > self.player.x - self.player.width//2 and
                bullet.x < self.player.x + self.player.width//2 and
                bullet.y > self.player.y - self.player.height//2 and
                bullet.y < self.player.y + self.player.height//2):
                
                if self.player.take_damage():
                    self.game_over = True
                if bullet in self.enemy_bullets:
                    self.enemy_bullets.remove(bullet)
        
        # Atualiza power-ups
        for powerup in self.powerups[:]:
            powerup.update()
            if powerup.y > self.game.HEIGHT + 50:
                self.powerups.remove(powerup)
            
            # Colisão com player
            if (powerup.x > self.player.x - 20 and
                powerup.x < self.player.x + 20 and
                powerup.y > self.player.y - 20 and
                powerup.y < self.player.y + 20):
                
                self.player.add_powerup(powerup.type)
                self.powerups.remove(powerup)
        
        # Atualiza explosões
        for explosion in self.explosions[:]:
            explosion["timer"] += 1
            if explosion["timer"] > explosion["duration"]:
                self.explosions.remove(explosion)
        
        # Chance de spawn de power-up
        self.powerup_timer += 1
        if (random.random() < self.powerup_chance and 
            self.powerup_timer > 180):  # No mínimo 3 segundos entre power-ups
            
            x = random.randint(50, self.game.WIDTH - 50)
            y = -30
            self.powerups.append(PowerUp(x, y))
            self.powerup_timer = 0
        
        # Atualiza textos UI
        self.score_text = f"SCORE: {self.score}"
        self.wave_text = f"WAVE: {self.wave}"
        self.lives_text = f"LIVES: {self.player.lives}"
        
        return None
    
    def spawn_boss(self):
        from scripts.enemy import Boss
        self.boss_active = True
        self.boss = Boss(self.game.WIDTH // 2, 100)
    
    def next_wave(self):
        self.wave += 1
        self.enemies_spawned = 0
        self.enemies_to_spawn = 5 + (self.wave * 2)
        self.spawn_delay = max(20, 60 - (self.wave * 2))  # Spawn mais rápido a cada wave
    
    def create_explosion(self, x, y, large=False):
        self.explosions.append({
            "x": x,
            "y": y,
            "timer": 0,
            "duration": 30,
            "size": 30 if large else 15,
            "max_size": 60 if large else 30
        })
    
    def render(self, screen):
        # Desenha elementos do jogo
        for bullet in self.bullets:
            bullet.draw(screen)
        
        for bullet in self.enemy_bullets:
            bullet.draw(screen)
        
        for enemy in self.enemies:
            enemy.draw(screen)
        
        if self.boss_active and self.boss:
            self.boss.draw(screen)
        
        for powerup in self.powerups:
            powerup.draw(screen)
        
        for explosion in self.explosions:
            size = explosion["size"] + (explosion["timer"] * 2)
            if size > explosion["max_size"]:
                size = explosion["max_size"] - (explosion["timer"] - 15)
            
            alpha = 255 - (explosion["timer"] * 8)
            if alpha < 0:
                alpha = 0
            
            # Cria superfície para explosão
            surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(surf, (255, 100, 0, alpha), (size, size), size)
            pygame.draw.circle(surf, (255, 200, 0, alpha), (size, size), size // 2)
            screen.blit(surf, (explosion["x"] - size, explosion["y"] - size))
        
        self.player.draw(screen)
        
        # UI
        score_surf = self.game.font_medium.render(self.score_text, True, (255, 255, 255))
        screen.blit(score_surf, (10, 10))
        
        wave_surf = self.game.font_medium.render(self.wave_text, True, (255, 255, 255))
        screen.blit(wave_surf, (10, 50))
        
        lives_surf = self.game.font_medium.render(self.lives_text, True, (255, 255, 255))
        screen.blit(lives_surf, (10, 90))
        
        # Barra de cooldown do special
        if self.player.special_cooldown > 0:
            pygame.draw.rect(screen, (100, 100, 100), (700, 10, 80, 20))
            width = 80 - (self.player.special_cooldown * 80 / 180)
            pygame.draw.rect(screen, (0, 200, 0), (700, 10, width, 20))
            special_text = self.game.font_small.render("SPECIAL", True, (255, 255, 255))
            screen.blit(special_text, (705, 12))
        
        # Power-ups ativos
        y_offset = 130
        if self.player.has_shield:
            shield_text = self.game.font_small.render(f"SHIELD: {self.player.shield_time//60}s", True, (0, 200, 255))
            screen.blit(shield_text, (10, y_offset))
            y_offset += 30
        
        if self.player.triple_shot:
            triple_text = self.game.font_small.render(f"TRIPLE: {self.player.triple_time//60}s", True, (255, 200, 0))
            screen.blit(triple_text, (10, y_offset))
            y_offset += 30
        
        # Game over screen
        if self.game_over:
            overlay = pygame.Surface((self.game.WIDTH, self.game.HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            
            game_over_text = self.game.font_large.render("GAME OVER", True, (255, 50, 50))
            screen.blit(game_over_text, (self.game.WIDTH//2 - game_over_text.get_width()//2, 200))
            
            final_score = self.game.font_medium.render(f"SCORE: {self.score}", True, (255, 255, 255))
            screen.blit(final_score, (self.game.WIDTH//2 - final_score.get_width()//2, 280))