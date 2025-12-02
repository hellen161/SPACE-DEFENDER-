import pygame

class Text:
    def __init__(self, text, x, y, font_size, color, font=None):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        
        # Se a font for None ou inválida, usa fonte padrão
        if font is None:
            self.font = pygame.font.Font(None, font_size)
        else:
            try:
                # Tenta usar a fonte passada
                self.font = font
            except:
                # Se falhar, usa fonte padrão
                self.font = pygame.font.Font(None, font_size)
        
        self.update_surface()
    
    def update_surface(self):
        self.surface = self.font.render(self.text, True, self.color)
        self.rect = self.surface.get_rect(center=(self.x, self.y))
    
    def draw(self, screen):
        screen.blit(self.surface, self.rect)

class Button:
    def __init__(self, text, x, y, width, height, color, hover_color, font):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.hover_color = hover_color
        
        # Se a font for None ou inválida, usa fonte padrão
        if font is None:
            self.font = pygame.font.Font(None, 32)
        else:
            try:
                self.font = font
            except:
                self.font = pygame.font.Font(None, 32)
        
        self.is_hovering = False
        self.rect = pygame.Rect(x - width//2, y - height//2, width, height)
        self.text_surface = self.font.render(text, True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect(center=(x, y))
    
    def update_hover(self, mouse_pos):
        self.is_hovering = self.rect.collidepoint(mouse_pos)
        return self.is_hovering
    
    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)
    
    def click(self):
        return self.text.lower() if self.text != "SAIR" else "quit"
    
    def draw(self, screen):
        color = self.hover_color if self.is_hovering else self.color
        
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 3, border_radius=10)
        
        screen.blit(self.text_surface, self.text_rect)