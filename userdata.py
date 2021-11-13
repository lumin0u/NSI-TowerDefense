import os

# chemin d'accès du fichier de données

DATA_PATH = "data"

DEFAULT_DATA = """
{
    "unlocked_levels": [0],
    "tuto_info": {
        "no_more_levels": True,
        "basic": True,
        "money": True,
        "controls": True,
        "damaged": True
    }
}
"""

# la liste des ids des niveaux débloqués
UNLOCKED_LEVELS = []
# informations pour le tutoriel, True indique que le message n'a pas encore été affiché
TUTO_INFO = {}


def reset():
    """
        Supprime les données sauvegardées
    """
    open(DATA_PATH, mode="w+").write(DEFAULT_DATA)
    update()


def update():
    """
        Met à jour les données à partir du fichier de données
    """
    global UNLOCKED_LEVELS, TUTO_INFO
    
    # le json est parfaitement interprétable en python
    data = eval(open(DATA_PATH, mode="r").read())
    UNLOCKED_LEVELS = data["unlocked_levels"]
    TUTO_INFO = data["tuto_info"]


def save():
    """
        Sauvegarde les données dans le fichier de données
    """
    data = {"unlocked_levels": UNLOCKED_LEVELS, "tuto_info": TUTO_INFO}
    open(DATA_PATH, mode="w").write(str(data))


if not os.path.exists(DATA_PATH):
    reset()
else:
    try:
        update()
    except KeyError:
        print("Une erreur a eu lieu lors du chargement du fichier de données")
        open(DATA_PATH + ".save", mode="w+").write(open(DATA_PATH, mode="r").read())
        reset()
