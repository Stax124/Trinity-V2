import json

names = open("./test/names.txt", "r").readlines()
d = dict()

base_money = 15000
base_army = 2000
level_multiplier = 1.2
time_multiplier = 1.02
rarity_drop = {
    "legendary": 0.01,
    "epic": 0.05,
    "rare": 0.1,
    "uncommon": 0.2,
}
level = 1


for name in names:
    base_time = 2
    drop = 1

    name = name.replace("\n", "").replace(" ", "-")

    legendary = rarity_drop["legendary"]*level
    if legendary > 1:
        legendary = 1
    drop -= legendary

    if drop > 0:
        epic = rarity_drop["epic"]*level
        if epic > drop:
            epic = drop
        drop -= epic

        if drop > 0:
            rare = rarity_drop["rare"]*level
            if rare > drop:
                rare = drop
            drop -= rare

            if drop > 0:
                uncommon = rarity_drop["uncommon"]*level
                if uncommon > drop:
                    uncommon = drop
                drop -= uncommon
            else:
                uncommon = 0
        else:
            rare = 0
    else:
        epic = 0
        rare = 0
        uncommon = 0
    common = drop

    for _ in range(level):
        base_time *= time_multiplier

    hours = base_time

    d[name] = {
        "level": level,
        "common": common,
        "uncommon": uncommon,
        "rare": rare,
        "epic": epic,
        "legendary": legendary,
        "hours": int(hours),
        "description": None
    }

    level += 1

json.dump(d, open("./test/test.json", "w"), indent=4)
