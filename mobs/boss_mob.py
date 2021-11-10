from interface import pictures
import mobs.mob as mob
from position import Position
import main
import game


class BossMob(mob.Mob):
    def __init__(self, game_, position: Position, health):
        attributes = {
    
            # les dégats maximums que le mob pourra infliger
            "damage": 1000000,
            
            # la vie maximum
            "health_mul": 1,
            
            # la vitesse, en tuiles/ticks
            "speed": 0.01,
            
            # les resistances du mob, pour chaque type d'attaque
            "resistances": {
                game.DAMAGE_TYPE_FIRE: 0.75,
                game.DAMAGE_TYPE_ICE: 0.75,
                game.DAMAGE_TYPE_RAW: 0.75,
                game.DAMAGE_TYPE_MAGIC: 0.75,
                
                # le type DAMAGE_TYPE_ABSOLUTE est renseigné par défaut dans mob.py
            },
        }
        super().__init__(game_, position, attributes, health)
    
    def tick(self, current_tick, game_):
        super().tick(current_tick, game_)
        # a chaque tick
        
        # le mob avance
        self.advance()
    
    def get_render(self, time):
        return pictures.get("boss").final_scaled(0.5)
