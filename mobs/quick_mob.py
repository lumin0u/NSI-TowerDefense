from interface import pictures, graphics
import mobs.mob as mob
from position import Position
import main
import game


class QuickMob(mob.Mob):
    def __init__(self, game_, position: Position, health):
        attributes = {
            
            # les dégats maximums que le mob pourra infliger
            "damage": 0.5,
            
            # la vie maximum
            "health_mul": 0.75,
            
            # la vitesse, en tuiles/ticks
            "speed": 0.15 / 3,
            
            # les resistances du mob, pour chaque type d'attaque
            "resistances": {
                game.DAMAGE_TYPE_FIRE: 1,
                game.DAMAGE_TYPE_ICE: 1,
                game.DAMAGE_TYPE_RAW: 1,
                game.DAMAGE_TYPE_MAGIC: 1,
                
                # le type DAMAGE_TYPE_ABSOLUTE est renseigné par défaut dans mob.py
            },
        }
        super().__init__(game_, position, attributes, health, "rapide_break")
    
    def tick(self, current_tick, game_):
        super().tick(current_tick, game_)
        # a chaque tick
        
        # le mob avance
        self.advance()
    
    def get_render(self, time):
        return pictures.get("triangle").final_scaled(0.25)