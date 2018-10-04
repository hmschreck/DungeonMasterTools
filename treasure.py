#!/usr/bin/python3
import re
from numpy.random import randint, choice
from stores import Jewel, Art, Scroll, Ring, Wondrous, Weapon, Armor, Potion, determine_cost

Monster_Types = {
    "aberration": ['Coins', 'Coins and Gems', 'Coins & Small Objects', 'Armor and weapons', ],
    "animal": ['Coins', 'Coins and Gems', 'Coins & Small Objects', 'Armor and weapons', ],
    "construct": ['Coins and Gems', 'Art Objects', 'Armor and weapons', 'Combatant Gear', 'Lair Treasure', ],
    "dragon": ['Coins', 'Coins and Gems', 'Art Objects', 'Lair Treasure', 'Treasure Horde', ],
    "fey": ['Coins and Gems', 'Art Objects', 'Coins & Small Objects', 'Spellcaster Gear', ],
    "humanoid": ['Coins', 'Coins and Gems', 'Coins & Small Objects', 'Armor and weapons', 'Combatant Gear',
                 'Spellcaster Gear', 'Lair Treasure', ],
    "magical beast": ['Coins', 'Coins and Gems', 'Coins & Small Objects', 'Armor and weapons', ],
    "monstrous humanoid": ['Coins', 'Coins and Gems', 'Art Objects', 'Coins & Small Objects', 'Armor and weapons',
                           'Lair Treasure', ],
    "ooze": ['Coins', 'Coins and Gems', 'Coins & Small Objects', ],
    "outsider": ['Coins', 'Coins and Gems', 'Art Objects', 'Coins & Small Objects', 'Armor and weapons',
                 'Combatant Gear', 'Spellcaster Gear', 'Lair Treasure', 'Treasure Horde', ],
    "plant": ['Coins', 'Coins and Gems', 'Coins & Small Objects', 'Armor and weapons', ],
    "undead": ['Coins', 'Coins and Gems', 'Coins & Small Objects', 'Armor and weapons', 'Combatant Gear',
               'Spellcaster Gear', ],
    "vermin": ['Coins', 'Coins and Gems', 'Coins & Small Objects', ],
}
Coins = {
    1: ["5d10 cp", "3d4 sp"],
    5: ["2d6 *10 cp", "4d8 sp", "1d4 gp"],
    10: ["5d10 *10 cp", "5d10 sp", "1d8 gp"],
    25: ["2d4 *100 cp", "3d6 *10 sp", "4d4 gp"],
    50: ["4d4 *100 cp", "4d6 *10 sp", "8d6 gp"],
    100: ["6d8 *10 sp", "3d4 *10 gp"],
    200: ["2d4 *100 sp", "4d4 *10 gp", "2d4 pp"],
    500: ["6d6 *10 gp", "8d6 pp"],
    1000: ["2d4 *100 gp", "10d10 pp"],
    5000: ["4d8 *100 gp", "6d10 *10 pp"],
    10000: ["2d4 *1000 gp", "12d8 *10 pp"],
    50000: ["2d6 *1000 gp", "8d10 *100 pp"],
}
Coins_and_Gems = {
    10: ["grade 1 gemstone"],
    15: ["2d6 *10 cp", "4d8 sp", "1d4 gp", "grade 1 gemstone"],
    25: ["5d10 sp", "1d4 gp", "2 grade 1 gemstones"],
    50: ["grade 2 gemstone"],
    75: ["1d4 *10 sp", "1d4 gp", "2 grade 1 gemstones", "grade 2 gemstone"],
    100: ["grade 3 gemstone"],
    150: ["grade 2 gemstone", "grade 3 gemstone"],
    200: ["3d6 *10 sp", "2d4 *10 gp", "4 grade 1 gemstones", "grade 3 gemstone"],
    250: ["2d4 *10 gp", "2 grade 2 gemstones", "grade 3 gemstone"],
    500: ["grade 4 gemstone"],
    750: ["2d4 *10 gp", "2 grade 2 gemstones", "grade 3 gemstone", "grade 4 gemstone"],
    1000: ["grade 5 gemstone"],
    2500: ["2d4 *100 gp", "2 grade 4 gemstones", "grade 5 gemstone"],
    5000: ["grade 6 gemstone"],
    10000: ["5 grade 5 gemstones", "grade 6 gemstone"],
    20000: ["4d8 *100 gp", "6d10 *10 pp", "3 grade 6 gemstones"],
    50000: ["4d4 *10 pp", "10 grade 3 gemstones", "4 grade 4 gemstones", "6 grade 5 gemstones", "8 grade 6 gemstones"],
}
Art_Objects = {
    50: ["grade 1 art object"],
    100: ["grade 2 art object"],
    150: ["grade 1 art object", "grade 2 art object"],
    200: ["2 grade 2 art objects"],
    250: ["3 grade 1 art objects", "grade 2 art object"],
    500: ["grade 3 art object"],
    750: ["3 grade 1 art objects", "2 grade 2 art objects", "grade 3 art object"],
    1000: ["grade 4 art object"],
    1500: ["grade 3 art object", "grade 4 art object"],
    2000: ["2 grade 4 art objects"],
    2500: ["5 grade 2 art objects", "2 grade 3 art objects", "grade 4 art object"],
    5000: ["grade 5 art object"],
    7500: ["grade 3 art object", "2 grade 4 art objects", "grade 5 art object"],
    10000: ["grade 6 art object"],
    15000: ["grade 5 art object", "grade 6 art object"],
    20000: ["2 grade 5 art objects", "grade 6 art object"],
    50000: ["10 grade 3 art objects", "5 grade 4 art objects", "4 grade 5 art objects", "2 grade 6 art objects"],

}
Coins_and_Objects = {
    40: ["3d6 *10 sp", "4d4 gp", "lesser minor scroll"],
    50: ["2d4 *10 sp", "2d4 gp", "lesser minor potion"],
    100: ["4d6 *10 sp", "3d10 gp", "lesser minor potion", "lesser minor scroll"],
    150: ["2d4 *10 sp", "6d6 gp", "greater minor scroll"],
    200: ["2d4 *10 sp", "4d6 gp", "greater minor potion", "lesser minor scroll"],
    250: ["3d6 *10 sp", "3d6 gp", "1d4 pp", "2 lesser minor potions", "greater minor scroll"],
    300: ["2d4 *10 sp", "6d6 gp", "greater minor potion", "greater minor scroll"],
    400: ["greater minor potion", "2 greater minor scrolls"],
    450: ["2d4 *10 gp", "1d4 pp", "lesser medium potion", "greater minor scroll"],
    500: ["2d4 *10 gp", "1d4 pp", "2 greater minor potions", "greater minor scroll"],
    750: ["7d6 gp", "greater minor scroll", "lesser minor wand"],
    1000: ["4d4 *10 gp", "3d6 pp", "lesser medium potion", "lesser medium scroll"],
    1250: ["2d6 *10 gp", "2d4 pp", "lesser medium potion", "lesser minor wand"],
    1500: ["greater minor wand"],
    1750: ["4d6 *10 gp", "3d6 pp", "greater medium potion", "greater medium scroll"],
    2000: ["greater medium potion", "greater minor wand"],
    2500: ["2d6 *10 gp", "2d4 pp", "lesser medium potion", "2 greater medium scrolls"],
    3000: ["3d6 *10 gp", "4d4 pp", "greater medium potion", "greater medium scroll", "greater minor wand"],
    4000: ["3d6 *10 gp", "4d4 pp", "greater medium scroll", "2 greater minor wands"],
    5000: ["2d4 *10 gp", "2d4 pp", "3 lesser major potions", "2 greater medium scrolls", "greater minor wand"],
    7500: ["2d6 pp", "lesser major scroll", "lesser medium wand"],
    8000: ["5d8 pp", "2 greater major potions", "2 greater major scrolls"],
    10000: ["greater medium wand"],
    12500: ["4d6 pp", "greater major potion", "greater major scroll", "lesser medium wand"],
    15000: ["lesser major wand"],
    17500: ["10d10 pp", "3 greater major potions", "2 lesser major scrolls", "greater medium wand"],
    20000: ["4d4 *10 gp", "2d4 *10 pp", "2 greater major potions", "greater major scroll", "lesser major wand"],
    22500: ["6d8 *10 gp", "3 lesser major potions", "greater major wand"],
    25000: ["5 greater major scrolls", "greater medium wand"],
    30000: ["6d6 pp", "4 greater major potions", "3 greater major scrolls", "greater major wand"],
    50000: ["8d4 *10 pp", "4 greater major scrolls", "2 greater major wands"],
}
Armor_and_Weapons = {
    200: ["masterwork light armor"],
    300: ["masterwork medium armor"],
    350: ["masterwork weapon"],
    1000: ["masterwork heavy armor"],
    1500: ["lesser minor armor"],
    2500: ["lesser minor weapon"],
    3000: ["greater minor armor"],
    3500: ["masterwork medium armor", "masterwork light armor", "lesser medium weapon"],
    4000: ["lesser minor armor", "lesser minor weapon"],
    5500: ["greater minor armor", "lesser minor weapon"],
    6000: ["greater minor weapon"],
    7500: ["lesser minor armor", "greater minor weapon"],
    8000: ["greater minor armor", "2 lesser minor weapons"],
    9000: ["greater minor armor", "greater minor weapon"],
    10000: ["lesser medium armor", "lesser minor weapon"],
    13000: ["lesser medium weapon"],
    13500: ["lesser medium armor", "greater medium weapon"],
    15000: ["greater medium armor", "lesser minor weapon"],
    20000: ["lesser medium armor", "lesser medium weapon"],
    25000: ["greater minor armor", "greater medium weapon"],
    30000: ["lesser major armor", "lesser minor weapon", "greater minor weapon"],
    32500: ["lesser medium armor", "greater medium weapon"],
    35000: ["lesser major armor", "lesser medium weapon"],
    37500: ["lesser medium armor", "lesser major weapon"],
    40000: ["greater major armor", "greater minor weapon"],
    50000: ["greater major armor", "lesser medium weapon"],
    75000: ["greater minor armor", "greater major weapon"],
    100000: ["greater major armor", "greater major weapon"],
}
Combatant_Gear = {
    50: ["2d4 *10 sp", "2d4 gp", "lesser minor potion"],
    250: ["2d4 *10 sp", "2d4 gp", "masterwork light armor", "lesser minor potion"],
    350: ["2d4 *10 sp", "2d4 gp", "masterwork medium armor", "lesser minor potion"],
    400: ["2d4 *10 sp", "2d4 gp", "masterwork weapon", "lesser minor potion"],
    500: ["masterwork weapon", "greater minor potion"],
    750: ["6d6 gp", "masterwork medium armor", "masterwork weapon", "2 lesser minor potions "],
    1000: ["masterwork heavy armor"],
    1500: ["masterwork heavy armor", "masterwork weapon", "greater minor potion"],
    2000: ["lesser minor armor", "masterwork weapon", "2 greater minor potions "],
    3000: ["masterwork medium armor", "lesser minor weapon", "greater minor potion"],
    4000: ["lesser minor armor", "masterwork weapon", "lesser minor wondrous item", "greater minor potion"],
    5000: ["masterwork medium armor", "lesser minor weapon", "lesser minor wondrous item", "greater minor potion"],
    6000: ["lesser minor armor", "lesser minor weapon", "lesser minor wondrous item"],
    7500: ["greater minor armor", "lesser minor weapon", "lesser minor ring"],
    10000: ["greater minor armor", "lesser minor weapon", "lesser minor ring", "lesser minor wondrous item", "3 greater minor potions "],
    11000: ["greater minor armor", "greater medium weapon", "2 greater medium potions "],
    12500: ["greater minor armor", "lesser minor weapon", "greater minor wondrous item", "2 greater medium potions "],
    15000: ["greater minor armor", "greater minor weapon", "greater minor ring"],
    20000: ["lesser medium armor", "greater minor weapon", "greater minor wondrous item", "2 greater medium potions "],
    25000: ["lesser medium armor", "lesser medium weapon", "lesser minor ring", "lesser minor wondrous item", "2 greater medium potions"],
    30000: ["lesser medium armor", "lesser medium weapon", "2 lesser minor rings", "greater minor wondrous items"],
    40000: ["lesser medium armor", "lesser medium weapon", "lesser medium ring", "greater minor wondrous item", "2 greater medium potions "],
    50000: ["greater medium armor", "greater medium weapon", "lesser medium wondrous item", "2 lesser major potions "],
    60000: ["greater medium armor", "greater medium weapon", "2 greater minor rings", "2 greater minor wondrous items"],
    75000: ["lesser major armor", "greater medium weapon", "greater minor ring", "greater medium wondrous item", "3 greater major potions "],
    100000: ["lesser major armor", "lesser major weapon", "lesser medium ring", "greater minor ring", "2 lesser medium wondrous items"],
}
Spellcaster_Gear = {
    50: ["2d4 *10 sp", "2d4 gp", "lesser minor potion"],
    75: ["2d4 gp", "lesser minor potion", "lesser minor scroll"],
    100: ["lesser minor potion", "2 lesser minor scrolls"],
    150: ["lesser minor scroll", "greater minor scroll"],
    200: ["2 lesser minor potions", "greater minor scroll"],
    250: ["2 greater minor scrolls"],
    500: ["3 lesser minor potions", "3 greater minor scrolls"],
    750: ["greater minor potion", "lesser minor wand"],
    1000: ["7d6 gp", "3 greater minor scrolls", "lesser minor wand"],
    1500: ["3d6 *10 gp", "lesser medium potion", "lesser medium scroll", "lesser minor wand"],
    2000: ["2d4 *10 gp", "masterwork weapon", "2 lesser medium scrolls", "lesser minor wand"],
    2500: ["2 greater medium potions", "greater minor wand"],
    3000: ["greater medium potion", "2 lesser medium scrolls", "greater minor wand"],
    4000: ["lesser minor wondrous item", "greater medium potion", "greater minor wand"],
    5000: ["lesser minor ring", "lesser minor wondrous item", "2 lesser medium scrolls"],
    6000: ["lesser minor ring", "lesser minor wondrous item", "greater medium potion", "greater minor wand"],
    7500: ["2 greater medium potions", "lesser minor scroll", "lesser medium wand"],
    10000: ["lesser minor ring", "lesser minor wondrous item", "lesser medium wand"],
    12500: ["lesser minor ring", "greater minor wondrous item", "2 greater medium scrolls", "2 greater minor wands"],
    15000: ["lesser minor ring", "lesser medium rod", "lesser medium wand"],
    20000: ["greater minor ring", "greater minor wondrous item", "greater medium potion", "2 greater medium scrolls", "lesser medium wand"],
    25000: ["lesser minor ring", "lesser medium wand", "greater medium wand", "greater minor wondrous item"],
    30000: ["greater minor ring", "lesser medium wondrous item", "lesser major scroll", "greater medium wand"],
    40000: ["lesser minor weapon", "lesser medium staff", "greater medium rod", "2 lesser minor wondrous items", "lesser medium wand"],
    50000: ["greater minor ring", "2 lesser medium wondrous items", "lesser major potion", "3 greater medium scrolls", "lesser major wand"],
    60000: ["lesser medium staff", "greater medium rod", "greater medium wondrous item", "greater medium potion", "2 lesser major scrolls", "lesser medium wand"],
    75000: ["lesser minor weapon", "greater medium staff", "greater medium wondrous item", "3 greater major scrolls", "greater major wand"],
    100000: ["lesser major ring", "greater medium rod", "lesser major staff", "lesser major scroll", "greater medium wand"],
}
Lair_Treasure = {
    500: ["4d4 *100 cp", "3d6 *10 sp", "2d4 *10 gp", "masterwork weapon", "lesser minor potion", "lesser minor scroll", "grade 2 gemstone"],
    1000: ["2d4 *100 cp", "2d6 *100 sp", "6d6 gp", "greater minor potion", "greater minor scroll", "lesser minor wand", "3 grade 1 gemstones"],
    2500: ["3d6 *10 sp", "2d4 gp", "masterwork heavy armor", "masterwork weapon", "2 lesser medium potions", "2 greater minor scrolls"],
    5000: ["2d4 *10 gp", "4d6 pp", "masterwork weapon", "lesser minor ring", "greater medium potion", "lesser medium scroll", "greater minor wand"],
    7500: ["4d4 *10 gp", "6d6 pp", "lesser minor weapon", "lesser minor wondrous item", "2 greater medium potions", "greater minor wand", "2 grade 3 gemstones"],
    10000: ["4d8 *10 gp", "6d10 pp", "greater minor armor", "lesser minor ring", "lesser minor wondrous item", "lesser medium scroll", "greater minor wand", "grade 4 gemstone"],
    15000: ["4d4 *10 gp", "4d4 *10 pp", "greater minor armor", "lesser minor wondrous item", "2 greater medium potions", "2 greater medium scrolls", "lesser medium wand", "1 grade 3 gemstone"],
    20000: ["2d4 *10 pp", "greater minor ring", "2 lesser minor wondrous items", "2 greater medium potions", "2 lesser major scrolls", "lesser medium wand"],
    25000: ["6d10 *10 gp", "6d6 pp", "lesser medium armor", "lesser minor weapon", "greater minor wondrous item", "2 lesser major scrolls", "lesser medium wand", "grade 4 gemstone"],
    30000: ["6d6 *10 gp", "2d4 *10 pp", "greater minor weapon", "lesser medium wondrous item", "greater medium wand", "3 grade 3 gemstones"],
    40000: ["4d4 *10 gp", "4d4 *10 pp", "lesser medium ring", "lesser medium rod", "2 greater major potions", "2 lesser major scrolls", "lesser major wand"],
    50000: ["4d4 *10 pp", "greater medium armor", "lesser medium staff", "lesser medium wondrous item", "greater major scroll", "lesser medium wand", "grade 5 gemstone"],
    75000: ["2d8 *100 gp", "4d4 *10 pp", "greater minor weapon", "greater medium ring", "greater medium staff", "3 greater major potions", "greater major scroll", "lesser major wand", "grade 5 gemstone"],
    100000: ["8d6 *100 gp", "4d4 *10 pp", "lesser major ring", "lesser major wondrous item", "3 greater major potions", "greater major scroll", "lesser medium wand", "2 grade 5 gemstones", "grade 6 gemstone"],
}
Treasure_Horde = {
    5000: ["4d4 *1000 cp", "6d6 *100 sp", "2d4 *100 gp", "6d6 pp", "lesser minor armor", "greater minor wand", "5 grade 3 gemstones", "grade 3 art object"],
    10000: ["4d4 *1000 cp", "6d6 *100 sp", "2d4 *100 gp", "6d6 pp", "greater minor armor", "lesser minor weapon", "lesser minor wondrous item", "greater medium scroll", "grade 4 gemstone", "grade 3 art object"],
    15000: ["2d4 *1000 cp", "6d4 *100 sp", "3d6 *10 gp", "6d6 pp", "greater minor ring", "2 lesser minor wondrous items", "2 greater medium potions", "greater minor wand", "grade 4 gemstone", "grade 3 art object"],
    20000: ["2d4 *1000 cp", "6d4 *100 sp", "3d6 *10 gp", "6d6 pp", "greater minor armor", "lesser medium rod", "greater minor wondrous item", "2 lesser major potions", "greater medium scroll", "3 grade 3 art objects"],
    25000: ["2d4 *1000 cp", "6d4 *100 sp", "3d6 *10 gp", "6d6 pp", "lesser medium staff", "2 lesser minor wondrous items", "greater medium potion", "lesser medium wand", "2 grade 2 gemstones", "2 grade 3 gemstones", "grade 4 gemstone"],
    30000: ["2d4 *1000 cp", "6d4 *100 sp", "3d6 *10 gp", "6d6 pp", "lesser medium armor", "greater minor weapon", "lesser medium wondrous item", "2 lesser major scrolls", "grade 4 art object"],
    40000: ["4d4 *1000 cp", "6d6 *100 sp", "2d4 *100 gp", "6d6 pp", "lesser medium weapon", "greater medium rod", "greater major potion", "greater medium scroll", "lesser medium wand", "3 grade 3 art objects", "2 grade 4 art objects"],
    50000: ["4d4 *10000 cp", "6d6 *1000 sp", "4d4 *100 gp", "2d4 *10 pp", "greater minor armor", "2 greater minor weapons", "greater medium staff", "greater minor wondrous item", "grade 5 gemstone"],
    60000: ["2d4 *10000 cp", "2d4 *1000 sp", "2d4 *100 gp", "2d4 *10 pp", "greater medium weapon", "greater medium rod", "lesser medium wondrous item", "greater major scroll", "2 greater minor wands", "grade 4 gemstone", "5 grade 2 art objects"],
    75000: ["2d4 *10000 cp", "2d4 *1000 sp", "2d4 *100 gp", "2d4 *10 pp", "lesser major armor", "greater medium ring", "lesser medium staff", "greater medium wand", "grade 6 gemstone", "grade 4 art object"],
    100000: ["2d4 *10000 cp", "2d4 *1000 sp", "2d4 *100 gp", "2d4 *10 pp", "lesser medium weapon", "greater medium ring", "lesser major rod", "greater medium wondrous item", "2 greater major potions", "lesser medium scroll", "2 grade 4 art objects"],
    125000: ["4d4 *10000 cp", "6d6 *1000 sp", "4d4 *100 gp", "2d8 *10 pp", "greater major armor", "lesser medium weapon", "lesser major staff", "2 greater major scrolls", "greater major wand", "grade 6 gemstone", "3 grade 4 art objects"],
    150000: ["4d4 *10000 cp", "6d6 *1000 sp", "4d4 *100 gp", "2d8 *10 pp", "greater medium armor", "lesser major ring", "greater major wondrous item", "greater major wand"],
    200000: ["4d4 *10000 cp", "6d6 *1000 sp", "4d4 *100 gp", "2d8 *10 pp", "greater major weapon", "2 lesser medium rings", "lesser major staff", "lesser major wondrous item", "lesser major wand", "3 grade 5 gemstones", "grade 4 gemstone"],
    300000: ["8d4 *10000 cp", "12d6 *1000 sp", "8d4 *100 gp", "2d8 *10 pp", "greater major weapon", "lesser major ring", "greater major staff", "greater major wondrous item", "greater medium wand", "grade 6 gemstone", "grade 6 art object"],
}

# 1/8, 1/6, 1/4, 1/3, 1/2, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
# 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30,
Campaign_Speed_Slow = \
    [20, 30, 40, 55, 85, 170, 350, 550, 750, 1000, 1350, 1750, 2200, 2850, 3650, 4650, 6000, 7750, 10000, 13000, 16500,
     22000, 28000, 35000, 44000, 55000, 69000, 85000, 102000, 125000, 150000, 175000, 205000, 240000, 280000, 320000,
     360000, 400000, 440000, 480000, 520000, 560000, 600000, 640000, 680000, 720000, 760000, 800000, 840000, 880000,
     920000, 960000, 1000000, 1040000, 1080000, 1120000, ]
Campaign_Speed_Medium = \
    [35, 45, 65, 85, 130, 260, 550, 800, 1150, 1550, 2000, 2600, 3350, 4250, 5450, 7000, 9000, 11600, 15000, 19500,
     25000, 32000, 41000, 53000, 67000, 84000, 104000, 127000, 155000, 185000, 220000, 260000, 305000, 360000, 420000,
     480000, 540000, 600000, 660000, 720000, 780000, 840000, 900000, 960000, 1020000, 1080000, 1140000, 1200000,
     1260000, 1320000, 1380000, 1440000, 1500000, 1560000, 1620000, 1680000, ]
Campaign_Speed_Fast = \
    [50, 65, 100, 135, 200, 400, 800, 1200, 1700, 2300, 3000, 3900, 5000, 6400, 8200, 10500, 13500, 17500, 22000, 29000,
     38000, 48000, 62000, 79000, 100000, 125000, 155000, 190000, 230000, 275000, 330000, 390000, 460000, 540000, 630000,
     720000, 810000, 900000, 990000, 1080000, 1170000, 1260000, 1350000, 1440000, 1530000, 1620000, 1710000, 1800000,
     1890000, 1980000, 2070000, 2160000, 2250000, 2340000, 2430000, 2520000, ]

Campaign_Speed = Campaign_Speed_Medium


def treasure_calculator(treasure, species, cr):
    if species not in list(Monster_Types.keys()):
        return None
    all_items = []
    additional = ''
    mult = 0
    match = re.match(r'NPG gear \((.*)\)', treasure)
    if match is not None:
        # Add some gold with whatever is in group 1
        additional = match.group(1)
    else:
        match = re.match(r'([ \w])+ \((.*)\)', treasure)
        if match is not None:
            additional = match.group(2)
            treasure = match.group(1)

    # Basic Cases
    if treasure == 'standard':
        mult = 1
    elif treasure == 'half standard':
        mult = 0.5
    elif treasure == 'double standard':
        mult = 2
    elif treasure == 'triple standard':
        mult = 3

    if float(cr) == .13:
        budget = Campaign_Speed[0]
    elif float(cr) == .17:
        budget = Campaign_Speed[1]
    elif float(cr) == .25:
        budget = Campaign_Speed[2]
    elif float(cr) == .33:
        budget = Campaign_Speed[3]
    elif float(cr) == .5:
        budget = Campaign_Speed[4]
    else:
        budget = Campaign_Speed[int(float(cr))+4]

    all_items += treasure_samples(mult, Monster_Types[species], budget)

    totalMoney = 0
    i = 0
    while i < len(all_items):
        if isinstance(all_items[i], int) or isinstance(all_items[i], float):
            totalMoney += all_items[i]
            all_items.pop(i)
        else:
            # all_items[i] = all_items[i].to_string()
            i += 1

    if additional != '':
        for item in additional.split(','):
            s = '<tr><td style="width:50%;"><span class="text-md">' + item.strip() + '</span></td><td> --- ' + \
                '</td><td>Common</td></tr>'
            all_items.append(s)
    s = '<tr><td style="width:50%;"><span class="text-md">Spare Change</span></td><td>' + determine_cost(totalMoney) + \
        '</td><td>Common</td></tr>'
    all_items.append(s)
    return all_items


def treasure_samples(quantity, item_groups, budget):
    all_items = []
    while budget > 0:
        category = choose_treause(choice(item_groups))
        available = []
        for item in list(category.keys()):
            if item <= budget:
                available.append(item)
        if not available:
            continue
        item_key = choice(available)
        budget -= item_key
        for items in category[item_key]:
            func = determine_treasure(items)
            if func is not None:
                ret = func(items)
                if isinstance(ret, float) or isinstance(ret, int):
                    all_items.append(ret)
                else:
                    all_items += ret
    return all_items


def choose_treause(item):
    if item == 'Coins':
        return Coins
    elif item == 'Coins and Gems':
        return Coins_and_Gems
    elif item == 'Art Objects':
        return Art_Objects
    elif item == 'Coins & Small Objects':
        return Coins_and_Objects
    elif item == 'Armor and weapons':
        return Armor_and_Weapons
    elif item == 'Combatant Gear':
        return Combatant_Gear
    elif item == 'Spellcaster Gear':
        return Spellcaster_Gear
    elif item == 'Lair Treasure':
        return Lair_Treasure
    elif item == 'Treasure Horde':
        return Treasure_Horde
    else:
        return None


def determine_treasure(s):
    if s.strip().split(' ')[-1] == 'scroll' or s.strip().split(' ')[-1] == 'scrolls':
        return scroll
    elif s.strip().split(' ')[-1] == 'ring' or s.strip().split(' ')[-1] == 'rings':
        return ring
    elif s.strip().split(' ')[-1] == 'pp' or s.strip().split(' ')[-1] == 'gp' or \
            s.strip().split(' ')[-1] == 'sp' or s.strip().split(' ')[-1] == 'cp':
        return money
    elif s.strip().split(' ')[-1] == 'gemstone' or s.strip().split(' ')[-1] == 'gemstones':
        return gemstone
    elif s.strip().split(' ')[-1] == 'weapon' or s.strip().split(' ')[-1] == 'weapons':
        return weapon
    elif s.strip().split(' ')[-1] == 'armor' or s.strip().split(' ')[-1] == 'armors':
        return armor
    elif s.strip().split(' ')[-1] == 'scroll' or s.strip().split(' ')[-1] == 'scrolls':
        return scroll
    elif s.strip().split(' ')[-1] == 'wand' or s.strip().split(' ')[-1] == 'wands' or \
            s.strip().split(' ')[-1] == 'rod' or s.strip().split(' ')[-1] == 'rods' or \
            s.strip().split(' ')[-1] == 'staff' or s.strip().split(' ')[-1] == 'staffs':
        return wand
    elif s.strip().split(' ')[-1] == 'potion' or s.strip().split(' ')[-1] == 'potions':
        return potion
    elif s.strip().split(' ')[-1] == 'object' or s.strip().split(' ')[-1] == 'objects':
        return art
    elif s.strip().split(' ')[-1] == 'item' or s.strip().split(' ')[-1] == 'items':
        return wondrous
    else:
        print(s)


def potion(g):
    l = []
    primary = ['lesser', 'greater']
    secondary = ['minor', 'medium', 'major']
    category = ''
    quantity = 0
    for p in primary:
        if category != '':
            break
        for s in secondary:
            match = re.match(re.compile('([\d ]*)' + p + ' ' + s + ' potion[s]?'), g)
            if match is not None:
                if match.group(1) == '' or match.group(1) is None:
                    quantity = 1
                else:
                    quantity = int(match.group(1))
                category = (p, s)
                break

    for _ in range(quantity):
        if category[1] == 'minor':
            l.append(Potion(randint(0, 3)))
        elif category[1] == 'medium':
            l.append(Potion(randint(2, 5)))
        elif category[1] == 'major':
            l.append(Potion(randint(4, 9)))
    return l


def armor(g):
    l = []
    primary = ['lesser', 'greater']
    secondary = ['minor', 'medium', 'major']
    category = ''
    quantity = 0
    for p in primary:
        if category != '':
            break
        for s in secondary:
            match = re.match(re.compile('([\d ]*)' + p + ' ' + s + ' armor[s]?'), g)
            if match is not None:
                if match.group(1) == '' or match.group(1) is None:
                    quantity = 1
                else:
                    quantity = int(match.group(1))
                category = (p, s)
                break

    for _ in range(quantity):
        if category[1] == 'minor':
            l.append(Armor(randint(0, 1)))
        elif category[1] == 'medium':
            l.append(Armor(randint(1, 2)))
        elif category[1] == 'major':
            l.append(Armor(randint(3, 4)))
    return l


def weapon(g):
    l = []
    primary = ['lesser', 'greater']
    secondary = ['minor', 'medium', 'major']
    category = ''
    quantity = 0
    for p in primary:
        if category != '':
            break
        for s in secondary:
            match = re.match(re.compile('([\d ]*)' + p + ' ' + s + ' weapon[s]?'), g)
            if match is not None:
                if match.group(1) == '' or match.group(1) is None:
                    quantity = 1
                else:
                    quantity = int(match.group(1))
                category = (p, s)
                break

    for _ in range(quantity):
        if category[1] == 'minor':
            l.append(Weapon(randint(0, 1)))
        elif category[1] == 'medium':
            l.append(Weapon(randint(1, 2)))
        elif category[1] == 'major':
            l.append(Weapon(randint(3, 4)))
    return l


def wondrous(g):
    l = []
    primary = ['lesser', 'greater']
    secondary = ['minor', 'medium', 'major']
    quantity = 0
    category = ''
    for p in primary:
        if category != '':
            break
        for s in secondary:
            match = re.match(re.compile('([\d ]*)' + p + ' ' + s + ' wondrous item[s]?'), g)
            if match is not None:
                if match.group(1) == '' or match.group(1) == None:
                    quantity = 1
                else:
                    quantity = int(match.group(1).strip())
                category = (p, s)
                break

    for _ in range(quantity):
        if category[0] == 'lesser' and category[1] == 'minor':
            l.append(Wondrous(randint(1, 3)))
        elif category[0] == 'lesser' and category[1] == 'medium':
            l.append(Wondrous(randint(2, 6)))
        elif category[0] == 'lesser' and category[1] == 'major':
            l.append(Wondrous(randint(4, 9)))
        if category[0] == 'greater' and category[1] == 'minor':
            l.append(Wondrous(randint(8, 13)))
        elif category[0] == 'greater' and category[1] == 'medium':
            l.append(Wondrous(randint(12, 16)))
        elif category[0] == 'greater' and category[1] == 'major':
            l.append(Wondrous(choice([16, 17, 18, 19, 20, 22])))
    return l


def art(s):
    l = []
    match = re.match(r'([\d ]*)grade (\d) art object[s]?', s)
    if match.group(1) is None or match.group(1) == '':
        l.append(Art(int(match.group(2)) - 1))
    else:
        for _ in range(int(match.group(1))):
            l.append(Art(int(match.group(2)) - 1))
    return l


def ring(g):
    l = []
    primary = ['lesser', 'greater']
    secondary = ['minor', 'medium', 'major']
    category = ''
    quantity = 0
    for p in primary:
        if category != '':
            break
        for s in secondary:
            match = re.match(re.compile('([\d ]*)' + p + ' ' + s + ' ring[s]?'), g)
            if match is not None:
                if match.group(1) == '' or match.group(1) == None:
                    quantity = 1
                else:
                    quantity = int(match.group(1))
                category = (p, s)
                break

    for _ in range(quantity):
        if category[1] == 'minor':
            l.append(Ring(randint(0, 3)))
        elif category[1] == 'medium':
            l.append(Ring(randint(2, 5)))
        elif category[1] == 'major':
            l.append(Ring(randint(4, 9)))
    return l


def wand(g):
    l = []
    primary = ['lesser', 'greater']
    secondary = ['minor', 'medium', 'major']
    category = ''
    quantity = 0
    for p in primary:
        if category != '':
            break
        for s in secondary:
            match = re.match(re.compile('([\d ]*)' + p + ' ' + s + ' wand[s]?'), g)
            if match is not None:
                if match.group(1) == '' or match.group(1) == None:
                    quantity = 1
                else:
                    quantity = int(match.group(1))
                category = (p, s)
                break

    for _ in range(quantity):
        if category[1] == 'minor':
            l.append(Scroll(randint(0, 3)))
        elif category[1] == 'medium':
            l.append(Scroll(randint(2, 5)))
        elif category[1] == 'major':
            l.append(Scroll(randint(4, 9)))
    return l


def gemstone(g):
    l = []
    match = re.match(r'([\d ]*)grade (\d) gemstone[s]?', g)
    if match.group(1) is '':
        l.append(Jewel(int(match.group(2)) - 1))
    else:
        for _ in range(int(match.group(1).strip())):
            l.append(Jewel(int(match.group(2)) - 1))
    return l


def money(s):
    match = re.match(r'(\d+)d(\d+) ([csgp]p)', s)
    if match is not None:
        # No need to multiply
        m = sum(randint(1, int(match.group(2)) + 1, size=int(match.group(1))))
        if not isinstance(m, int):
            m = int(m)
        if match.group(3) == 'cp':
            m *= .01
        elif match.group(3) == 'sp':
            m *= .1
        elif match.group(3) == 'pp':
            m *= 10

    match = re.match(r'(\d+)d(\d+) \*(\d+) ([csgp]p)', s)
    if match is not None:
        # Multiply
        m = sum(randint(1, int(match.group(2)) + 1, size=int(match.group(1)))) * int(match.group(3))
        if not isinstance(m, int):
            m = int(m)
        if match.group(4) == 'cp':
            m *= .01
        elif match.group(4) == 'sp':
            m *= .1
        elif match.group(4) == 'pp':
            m *= 10
        m *= int(match.group(3))
    return round(m, 2)


def scroll(g):
    l = []
    primary = ['lesser', 'greater']
    secondary = ['minor', 'medium', 'major']
    category = ''
    quantity = 0
    for p in primary:
        for s in secondary:
            match = re.match(re.compile('([\d ])*' + p + ' ' + s + ' [\d]+'), g)
            if match is not None:
                quantity = int(match.group(1).strip())
                category = (p, s)
                break
    for _ in range(quantity):
        if category[1] == 'minor':
            l.append(Scroll(randint(0, 1)))
        elif category[1] == 'medium':
            l.append(Scroll(randint(1, 2)))
        elif category[1] == 'major':
            l.append(Scroll(randint(3, 4)))
    return l


if __name__ == '__main__':
    for category in [Coins, Coins_and_Gems, Art_Objects, Coins_and_Objects, Armor_and_Weapons, Combatant_Gear, Spellcaster_Gear, Lair_Treasure, Treasure_Horde]:
        for items in category:
            for item in category[items]:
                func = determine_treasure(item)
                result = func(item)
                if result is None:
                    print(func)