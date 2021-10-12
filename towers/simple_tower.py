import towers.tower
import pictures

pictures.load_picture("simple_tower", "towers/")


class SimpleTower(towers.tower.Tower):
    def __init__(self, tile):
        super().__init__(tile, 10)
        
    def shoot(self):
        pass
    
    def get_render(self, time):
        return pictures.PICTURES["simple_tower"].get_img(time)
