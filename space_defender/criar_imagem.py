import pygame
import os
import math

def criar_imagens_placeholder():
    """Cria imagens placeholder para o jogo"""
    
    print("🎨 Criando imagens placeholder...")
    
    # Garante que as pastas existem
    pastas = [
        "assets/sprites",
        "assets/sprites/enemies",
        "assets/sprites/bullets",
        "assets/sprites/powerups",
        "assets/sprites/effects",
        "assets/sounds",
        "assets/fonts"
    ]
    
    for pasta in pastas:
        os.makedirs(pasta, exist_ok=True)
    
    # 1. Player
    surf = pygame.Surface((40, 40), pygame.SRCALPHA)
    pygame.draw.polygon(surf, (0, 200, 255), [
        (20, 0),    # Topo
        (5, 35),    # Inferior esquerdo
        (35, 35)    # Inferior direito
    ])
    pygame.draw.polygon(surf, (100, 255, 255), [
        (20, 0), (5, 35), (35, 35)
    ], 2)
    pygame.draw.line(surf, (255, 100, 0), (20, 35), (20, 40), 3)
    pygame.image.save(surf, "assets/sprites/player.png")
    print("✅ assets/sprites/player.png criado")
    
    # 2. Inimigos
    # Scout
    surf = pygame.Surface((30, 30), pygame.SRCALPHA)
    pygame.draw.polygon(surf, (255, 100, 100), [
        (15, 5),
        (25, 15),
        (15, 25),
        (5, 15)
    ])
    pygame.image.save(surf, "assets/sprites/enemies/scout.png")
    
    # Soldier
    surf = pygame.Surface((40, 40), pygame.SRCALPHA)
    points = []
    for i in range(6):
        angle = math.radians(i * 60)
        px = 20 + math.cos(angle) * 15
        py = 20 + math.sin(angle) * 15
        points.append((px, py))
    pygame.draw.polygon(surf, (255, 150, 50), points)
    pygame.image.save(surf, "assets/sprites/enemies/soldier.png")
    
    # Tank
    surf = pygame.Surface((50, 50), pygame.SRCALPHA)
    pygame.draw.rect(surf, (255, 50, 50), (5, 5, 40, 40))
    pygame.draw.rect(surf, (100, 100, 100), (20, 0, 10, 25))
    pygame.image.save(surf, "assets/sprites/enemies/tank.png")
    
    # Boss
    surf = pygame.Surface((100, 100), pygame.SRCALPHA)
    pygame.draw.circle(surf, (255, 0, 255), (50, 50), 40)
    pygame.draw.circle(surf, (255, 100, 255), (50, 50), 40, 3)
    pygame.draw.circle(surf, (255, 255, 0), (35, 40), 10)
    pygame.draw.circle(surf, (255, 255, 0), (65, 40), 10)
    pygame.draw.circle(surf, (0, 0, 0), (35, 40), 4)
    pygame.draw.circle(surf, (0, 0, 0), (65, 40), 4)
    pygame.draw.arc(surf, (255, 0, 0), (30, 60, 40, 30), 0, math.pi, 3)
    pygame.image.save(surf, "assets/sprites/enemies/boss.png")
    print("✅ Inimigos criados")
    
    # 3. Balas
    # Player bullet
    surf = pygame.Surface((10, 20), pygame.SRCALPHA)
    pygame.draw.polygon(surf, (0, 200, 255), [
        (5, 0),
        (2, 15),
        (8, 15)
    ])
    pygame.image.save(surf, "assets/sprites/bullets/player_bullet.png")
    
    # Enemy bullet
    surf = pygame.Surface((10, 10), pygame.SRCALPHA)
    pygame.draw.circle(surf, (255, 50, 50), (5, 5), 5)
    pygame.draw.circle(surf, (255, 150, 150), (5, 5), 2)
    pygame.image.save(surf, "assets/sprites/bullets/enemy_bullet.png")
    
    # Special bullet
    surf = pygame.Surface((15, 15), pygame.SRCALPHA)
    pygame.draw.circle(surf, (255, 255, 0), (7, 7), 7)
    pygame.draw.circle(surf, (255, 100, 0), (7, 7), 3)
    pygame.image.save(surf, "assets/sprites/bullets/special_bullet.png")
    print("✅ Balas criadas")
    
    # 4. Power-ups
    # Shield
    surf = pygame.Surface((40, 40), pygame.SRCALPHA)
    pygame.draw.circle(surf, (0, 200, 255), (20, 20), 15)
    pygame.draw.circle(surf, (255, 255, 255), (20, 20), 15, 2)
    pygame.draw.circle(surf, (255, 255, 255), (20, 20), 8, 2)
    pygame.draw.circle(surf, (255, 255, 255), (20, 20), 4, 2)
    pygame.image.save(surf, "assets/sprites/powerups/shield.png")
    
    # Triple shot
    surf = pygame.Surface((40, 40), pygame.SRCALPHA)
    pygame.draw.circle(surf, (255, 200, 0), (20, 20), 15)
    for i in range(3):
        angle = math.radians(i * 120)
        px = 20 + math.cos(angle) * 10
        py = 20 + math.sin(angle) * 10
        pygame.draw.circle(surf, (255, 255, 255), (int(px), int(py)), 5)
    pygame.image.save(surf, "assets/sprites/powerups/triple.png")
    
    # Rapid fire
    surf = pygame.Surface((40, 40), pygame.SRCALPHA)
    pygame.draw.circle(surf, (0, 255, 100), (20, 20), 15)
    points = [
        (20, 5),
        (30, 20),
        (20, 35),
        (10, 20)
    ]
    pygame.draw.polygon(surf, (255, 255, 255), points)
    pygame.image.save(surf, "assets/sprites/powerups/rapid.png")
    
    # Life
    surf = pygame.Surface((40, 40), pygame.SRCALPHA)
    pygame.draw.circle(surf, (255, 50, 50), (20, 20), 15)
    pygame.draw.circle(surf, (255, 255, 255), (16, 18), 7)
    pygame.draw.circle(surf, (255, 255, 255), (24, 18), 7)
    points = [
        (11, 19),
        (20, 32),
        (29, 19)
    ]
    pygame.draw.polygon(surf, (255, 255, 255), points)
    pygame.image.save(surf, "assets/sprites/powerups/life.png")
    print("✅ Power-ups criados")
    
    # 5. Explosão
    surf = pygame.Surface((64, 64), pygame.SRCALPHA)
    for i in range(8):
        angle = math.radians(i * 45)
        length = 25 + (i % 3) * 5
        px1 = 32 + math.cos(angle) * 10
        py1 = 32 + math.sin(angle) * 10
        px2 = 32 + math.cos(angle) * length
        py2 = 32 + math.sin(angle) * length
        
        # Gradiente de cor
        color = (
            255,
            200 - i * 10,
            50 + i * 5
        )
        
        pygame.draw.line(surf, color, (px1, py1), (px2, py2), 4)
    
    pygame.draw.circle(surf, (255, 255, 200, 180), (32, 32), 15)
    pygame.image.save(surf, "assets/sprites/effects/explosion.png")
    print("✅ Efeitos criados")
    
    # 6. Sons placeholder (arquivos vazios)
    for som in ["shoot", "explosion", "powerup", "hit", "music"]:
        with open(f"assets/sounds/{som}.wav", "wb") as f:
            f.write(b"")  # Arquivo vazio
    
    print("✅ Sons placeholder criados (arquivos vazios)")
    
    # 7. Instruções de fonte
    with open("assets/fonts/INSTRUCOES.txt", "w") as f:
        f.write("Para usar uma fonte personalizada:\n")
        f.write("1. Baixe uma fonte .ttf (ex: PressStart2P.ttf)\n")
        f.write("2. Renomeie para 'pixel_font.ttf'\n")
        f.write("3. Coloque nesta pasta\n")
        f.write("\nO jogo funcionará com fonte padrão se não encontrar este arquivo.")
    
    print("\n✨ TODAS AS IMAGENS PLACEHOLDER CRIADAS!")
    print("📁 Estrutura completa em 'assets/'")
    print("🎮 Execute 'python main.py' para jogar!")

if __name__ == "__main__":
    pygame.init()
    criar_imagens_placeholder()
    pygame.quit()