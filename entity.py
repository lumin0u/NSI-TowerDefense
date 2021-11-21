from abc import ABC, abstractmethod


class Entity(ABC):
    """
        Classe abstraite représentant une entité, c'est à dire soit un mob soit un projectile
        Une entité possède quelques attributs: un id unique et une position
    """
    def __init__(self, game_, position):
        """
        :param game_: Game - l'instance du jeu
        :param position: Position - la position d'apparition de l'entité
        """
        self._id = game_.next_id()
        
        self._position = position
        self._last_position = self._position
        self._ticks_lived = 0
        self._tiles_travelled = 0
    
    def tick(self, current_tick, game_):
        """
        :param current_tick: int - non utilisé ici
        :param game_: Game - non utilisé ici
        """
        # la distance parcourue depuis l'apparition est sauvegardée et permet notamment le choix de cible des tours
        self._tiles_travelled += self._last_position.distance(self._position)
        
        # la sauvegarde de la dernière position permet à l'étape du dessin de faire un mouvement fluide entre sa
        # dernière position et la prochaine
        self._last_position = self._position
        
        self._ticks_lived += 1
    
    @abstractmethod
    def is_dead(self):
        """
            Indique si l'entité vit encore ou non. Une entité morte n'est plus référencée dans l'instance du jeu
        :return: bool - si l'entité est morte ou non
        """
        pass
    
    @property
    def tiles_travelled(self) -> float:
        return self._tiles_travelled
    
    @property
    def id_(self):
        return self._id
    
    @property
    def position(self):
        return self._position
    
    @property
    def last_position(self):
        return self._last_position
    
    @property
    def ticks_lived(self):
        return self._ticks_lived
        
    @abstractmethod
    def get_render(self, relative_time):
        """
            Construit et retourne le rendu de l'entité à la date time
        :param relative_time: nombre - le temps relatif au tick
        :return: MyImage - le rendu de l'entité
        """
        pass
