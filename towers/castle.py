import levels
import towers.tower as tower
import game
from interface import pictures, ui


class Castle(tower.Tower):
    def __init__(self, tile, max_health):
        super().__init__(tile, 0, 0)
        self._max_health = max_health
        self._health = float(max_health)
        
    def shoot(self):
        pass
    
    @property
    def max_health(self):
        return self._max_health

    @property
    def health(self):
        return self._health
    
    def damage(self, amount: float, source):
        self._health -= amount
        
        if self._health <= 0:
            ui.INTERFACE_INSTANCE.popup_text = ["Vous avez perdu ...", "", "Cliquez sur OK", "pour recommencer"]
            
            def popup_button_action():
                game.GAME_INSTANCE = game.Game(levels.ALL_LEVELS[game.GAME_INSTANCE.level.id])
                
            ui.INTERFACE_INSTANCE.popup_button_action = popup_button_action
    
    def get_render(self, time):
        img = pictures.get("castle", hash(self.tile.position))
        return img
