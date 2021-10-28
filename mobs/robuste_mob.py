from interface import pictures, graphics
import mobs.mob as mob
from position import Position
import main
import game


class RobusteMob(mob.Mob):
    def __init__(self, game_, position: Position, health):
        attributes = {
            
            # la vie maximum
            "health_mul": 2,
            
            # la vitesse, en tuiles/ticks
            # TICK_REAL_TIME devrait toujours etre 0.1 (secondes) mais il faut toujours utiliser la variable
            # mettre TICK_REAL_TIME comme speed revient a dire que le mob avancera d'une tuile par seconde
            "speed": main.TICK_REAL_TIME / 4,
            
            # les resistances du mob, pour chaque type d'attaque
            "resistances": {
                game.DAMAGE_TYPE_FIRE: 2,
                game.DAMAGE_TYPE_ICE: 2,
                game.DAMAGE_TYPE_RAW: 2,
                game.DAMAGE_TYPE_MAGIC: 0.7,
                
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
        return pictures.PICTURES["robuste"].get_img().final_scaled(0.3)
