import random

class WaveManager:
    def __init__(self):
        self.wave = 1
        self.enemies_spawned = 0
        self.enemies_to_spawn = 5
        self.spawn_timer = 0
        self.spawn_delay = 60
        self.boss_wave = 5  # Boss a cada 5 waves
        
    def start_wave(self, wave_number):
        """Inicia uma nova wave"""
        self.wave = wave_number
        self.enemies_spawned = 0
        self.enemies_to_spawn = 5 + (wave_number * 2)
        self.spawn_delay = max(20, 60 - (wave_number * 2))  # Spawn mais rápido
        
        # Retorna informações da wave
        return {
            "wave": wave_number,
            "total_enemies": self.enemies_to_spawn,
            "boss": wave_number % self.boss_wave == 0
        }
    
    def should_spawn_enemy(self, current_enemies, boss_active=False):
        """Verifica se deve spawnar um novo inimigo"""
        if boss_active:
            return False
            
        if (self.spawn_timer >= self.spawn_delay and 
            self.enemies_spawned < self.enemies_to_spawn):
            
            self.spawn_timer = 0
            self.enemies_spawned += 1
            return True
        
        self.spawn_timer += 1
        return False
    
    def get_enemy_types_for_wave(self, wave):
        """Retorna quais tipos de inimigos podem spawnar na wave atual"""
        enemy_types = []
        
        if wave >= 1:
            enemy_types.append("scout")  # Sempre disponível
        
        if wave >= 2:
            enemy_types.append("soldier")  # Disponível a partir da wave 2
        
        if wave >= 3:
            enemy_types.append("tank")  # Disponível a partir da wave 3
        
        # Chance de spawn baseado na wave
        weights = []
        for enemy_type in enemy_types:
            if enemy_type == "scout":
                weight = max(0.5, 1.0 - (wave * 0.1))  # Diminui com waves
            elif enemy_type == "soldier":
                weight = min(0.7, 0.3 + (wave * 0.05))  # Aumenta com waves
            elif enemy_type == "tank":
                weight = min(0.5, 0.1 + (wave * 0.03))  # Aumenta lentamente
            weights.append(weight)
        
        # Normaliza os pesos
        total = sum(weights)
        if total > 0:
            weights = [w/total for w in weights]
        
        return random.choices(enemy_types, weights=weights, k=1)[0]
    
    def is_wave_complete(self, current_enemies_count):
        """Verifica se a wave atual foi completada"""
        return (self.enemies_spawned >= self.enemies_to_spawn and 
                current_enemies_count == 0)
    
    def get_wave_info(self):
        """Retorna informações da wave atual"""
        return {
            "number": self.wave,
            "enemies_spawned": self.enemies_spawned,
            "total_enemies": self.enemies_to_spawn,
            "progress": f"{self.enemies_spawned}/{self.enemies_to_spawn}",
            "next_boss_in": max(0, self.boss_wave - (self.wave % self.boss_wave))
        }