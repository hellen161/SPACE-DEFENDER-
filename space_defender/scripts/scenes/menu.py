import pygame
from scripts.ui import Button, Text

class MenuScene:
    def __init__(self, game):
        self.game = game
        self.title = Text("SPACE DEFENDER", 400, 150, 64, (255, 255, 255), game.font_large)
        
        # Botões do menu
        button_y = 250
        button_spacing = 70
        self.buttons = [
            Button("JOGAR", 400, button_y, 200, 50, (0, 200, 0), (0, 150, 0), game.font_medium),
            Button("RANKING", 400, button_y + button_spacing, 200, 50, (0, 150, 200), (0, 100, 150), game.font_medium),
            Button("INSTRUÇÕES", 400, button_y + button_spacing*2, 200, 50, (200, 150, 0), (150, 100, 0), game.font_medium),
            Button("SAIR", 400, button_y + button_spacing*3, 200, 50, (200, 0, 0), (150, 0, 0), game.font_medium)
        ]
        
        # Efeitos de fundo (estrelas)
        self.stars = []
        for i in range(100):
            self.stars.append({
                "x": pygame.time.get_ticks() % 800 + i * 7,
                "y": i * 6 % 600,
                "speed": (i % 3) + 1,
                "size": (i % 3) + 1
            })
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Botão esquerdo
                mouse_pos = pygame.mouse.get_pos()
                for button in self.buttons:
                    if button.is_hovered(mouse_pos):
                        return button.click()
        return None
    
    def update(self):
        # Atualiza estrelas
        for star in self.stars:
            star["x"] -= star["speed"]
            if star["x"] < 0:
                star["x"] = 800
                star["y"] = pygame.time.get_ticks() % 600
        
        # Atualiza hover dos botões
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.update_hover(mouse_pos)
        return None
    
    def render(self, screen):
        # Desenha estrelas
        for star in self.stars:
            color = (200, 200, 255) if star["speed"] > 1 else (150, 150, 200)
            pygame.draw.circle(screen, color, (int(star["x"]), int(star["y"])), star["size"])
        
        self.title.draw(screen)
        for button in self.buttons:
            button.draw(screen)
        
        # Instruções rápidas
        controls = [
            "CONTROLES:",
            "WASD/SETAS - Movimentar",
            "ESPAÇO - Atirar",
            "SHIFT - Tiro Especial"
        ]
        
        y_pos = 500
        for line in controls:
            text = self.game.font_small.render(line, True, (150, 150, 200))
            text_rect = text.get_rect(center=(400, y_pos))
            screen.blit(text, text_rect)
            y_pos += 25