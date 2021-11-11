import levels
from mobs import simple_mob, robuste_mob, boss_mob, quick_mob
from towers import simple_tower, explosive_tower, sniper_tower

tower_prices: dict[type, list[int]] = None
mobs_rewards: dict[type, int] = None


def load():
    prices_json = eval(open("resources/prices.json", mode="r").read())
    
    global tower_prices, mobs_rewards
    
    towers_names = {
        "simple": simple_tower.SimpleTower,
        "explosive": explosive_tower.ExplosiveTower,
        "sniper": sniper_tower.SniperTower
    }
    mobs_names = {
        "simple": simple_mob.SimpleMob,
        "robuste": robuste_mob.RobusteMob,
        "boss": boss_mob.BossMob,
        "rapide": quick_mob.QuickMob
    }
    
    tower_prices = {towers_names[k]: v for k, v in prices_json["towers"].items()}
    mobs_rewards = {mobs_names[k]: v for k, v in prices_json["mobs_rewards"].items()}



def get_tower_price(tower_type):
    return tower_prices[tower_type][0]


def get_tower_level_prices(tower_type):
    return tower_prices[tower_type][1:]
