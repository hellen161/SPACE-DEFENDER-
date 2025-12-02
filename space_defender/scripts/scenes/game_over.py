import pygame
from scripts.ui import Button, Text

class GameOverScene:
    def __init__(self, game):
        self.game = game
        self.title = Text("GAME OVER", 400, 150, 64, (255, 50, 50), game.font_large)
        self.score_text = Text(f"SCORE: {game.score}", 400, 220, 48, (255, 255, 255), game.font_medium)
        
        # Input para nome
        self.name = ""
        self.input_active = True
        
        # Botões
        self.buttons = [
            Button("SALVAR", 400, 350, 200, 50, (0, 200, 0), (0, 150, 0), game.font_medium),
            Button("MENU", 400, 420, 200, 50, (0, 150, 200), (0, 100, 150), game.font_medium),
            Button("SAIR", 400, 490, 200, 50, (200, 0, 0), (150, 0, 0), game.font_medium)
        ]
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if self.input_active:
                if event.key == pygame.K_RETURN:
                    if self.name.strip():
                        self.save_score()
                        return "menu"
                elif event.key == pygame.K_BACKSPACE:
                    self.name = self.name[:-1]
                elif len(self.name) < 10 and event.unicode.isalnum():
                    self.name += event.unicode.upper()
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                for button in self.buttons:
                    if button.is_hovered(mouse_pos):
                        result = button.click()
                        if result == "menu":
                            return "menu"
                        elif result == "quit":
                            return "quit"
        return None
    
    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        for button in self.buttons:
            button.update_hover(mouse_pos)
        return None
    
    def save_score(self):
        if self.name.strip():
            self.game.save_score(self.name, self.game.score)
    
    def render(self, screen):
        screen.fill((10, 10, 30))
        
        # Título e pontuação
        self.title.draw(screen)
        self.score_text.text = f"SCORE: {self.game.score}"
        self.score_text.draw(screen)
        
        # Input de nome
        input_rect = pygame.Rect(300, 280, 200, 40)
        pygame.draw.rect(screen, (50, 50, 80), input_rect)
        pygame.draw.rect(screen, (100, 100, 150), input_rect, 2)
        
        name_surface = self.game.font_medium.render(self.name, True, (255, 255, 255))
        screen.blit(name_surface, (310, 285))
        
        # Cursor piscando
        if pygame.time.get_ticks() % 1000 < 500 and self.input_active:
            cursor_x = 310 + name_surface.get_width()
            pygame.draw.line(screen, (255, 255, 255), 
                           (cursor_x, 285), 
                           (cursor_x, 315), 2)
        
        # Instrução
        instr = self.game.font_small.render("Digite seu nome e pressione ENTER", True, (150, 150, 200))
        screen.blit(instr, (400 - instr.get_width()//2, 330))
        
        # Botões
        for button in self.buttons:
            button.draw(screen)
        
        # High scores
        if self.game.high_scores:
            title = self.game.font_medium.render("TOP SCORES:", True, (255, 255, 0))
            screen.blit(title, (600, 50))
            
            for i, score_data in enumerate(self.game.high_scores[:5]):
                score_text = f"{i+1}. {score_data['name']}: {score_data['score']}"
                score_surf = self.game.font_small.render(score_text, True, (200, 200, 255))
                screen.blit(score_surf, (600, 100 + i * 30))