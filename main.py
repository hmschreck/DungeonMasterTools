#!/usr/bin/python3
import town_generator
from PC import PC
from os import linesep

"""
@TODO:
1: UNIT TESTS!
2: Try sorting items in stores based on rarity.
3: Character creator with actual classes
4: Add Beasts to Beast list
5: Just treasure printing
"""


def make_sample():
    with open('generate.txt', 'w') as outf:
        # Write Weapon Shop
        # [# of Stores, Rarity Low, Rarity High, Quantity Low, Quantity High, Inflation]
        outf.write("2 0 4 15 20 1.0" + linesep)
        # Write Armor Shop
        # [# of Stores, Rarity Low, Rarity High, Quantity Low, Quantity High, Inflation]
        outf.write("2 0 2 15 20 1.0" + linesep)
        # Write Potion Shop
        # [# of Stores, Rarity Low, Rarity High, Quantity Low, Quantity High, Inflation]
        outf.write("1 0 9 10 15 1.0" + linesep)
        # Write Enchant Shop
        # [# of Stores, Rarity Low, Rarity High, Quantity Low, Quantity High, Inflation]
        outf.write("1 0 9 10 15 1.0" + linesep)
        # Write Enchanter Shop
        # [# of Stores, Rarity Low, Rarity High, Quantity Low, Quantity High, Inflation]
        outf.write("1 0 9 15 25 1.0" + linesep)
        # Write Book Shop
        # [# of Stores, Quantity High, Quantity Low, Inflation]
        outf.write("1 15 25 1.0" + linesep)
        # Write Tavern Shop
        # [# of Stores, Rarity Low, Rarity High, Quantity Low, Quantity High, Inflation]
        outf.write("1 0 3 10 15 1.0" + linesep)
        # Write Jewel Shop
        # [# of Stores, Rarity Low, Rarity High, Quantity Low, Quantity High, Inflation]
        outf.write("1 0 5 15 30 1.0" + linesep)
        # Write Food Shop
        # [# of Stores, Rarity, Quantity Low, Quantity High, Inflation]
        outf.write("1 0 15 30 1.0" + linesep)
        # Write General Shop
        # [# of Stores, Rarity Low, Rarity High, Quantity Low, Quantity High, Trinkets, Inflation]
        outf.write("1 0 1 20 30 1 1.0" + linesep)
        # Write Brothel
        # [# of Stores, Rarity Low, Rarity High, Quantity Low, Quantity High, Inflation]
        outf.write("1 0 9 5 10 1" + linesep)
        # Write Gunsmith
        # [# of Stores, Rarity Low, Rarity High, Quantity Low, Quantity High, Inflation]
        outf.write("1 0 5 50 100 1" + linesep)
        # Write Quest board
        # [# of Stores, Level Low, Level High, Quantity]
        outf.write("1 0 5 20")


if __name__ == '__main__':
    # Weapons = Armor = Potion = Enchant = Enchanter = Books = Tavern = Jewel = Food = General = []
    with open('generate.txt', 'r') as inf:
        """ Ordering
        Weapons|Armor|Potion|Enchant|Enchanter|Books|Tavern|Jewel|Food|General|Brothel
        See above for explanation and creation of the settings
        """
        content = inf.readlines()
        val = content[0].split()
        Weapons = [eval(thing) for thing in val]

        val = content[1].split()
        Armor = [eval(thing) for thing in val]

        val = content[2].split()
        Potion = [eval(thing) for thing in val]

        val = content[3].split()
        Enchant = [eval(thing) for thing in val]

        val = content[4].split()
        Enchanter = [eval(thing) for thing in val]

        val = content[5].split()
        Books = [eval(thing) for thing in val]

        val = content[6].split()
        Tavern = [eval(thing) for thing in val]

        val = content[7].split()
        Jewel = [eval(thing) for thing in val]

        val = content[8].split()
        Food = [eval(thing) for thing in val]

        val = content[9].split()
        General = [eval(thing) for thing in val]

        val = content[10].split()
        Brothel = [eval(thing) for thing in val]

        val = content[11].split()
        Gunsmith = [eval(thing) for thing in val]

        val = content[12].split()
        Quests = [eval(thing) for thing in val]

        Positions = []
        NPC = []
        for thing in range(13, len(content)):
            title = content[thing].strip()
            if title[0] == '!':
                NPC.append(title[1:])
            else:
                Positions.append(title)

    town_name = town_generator.generate(Weapons, Armor, Potion, Enchant, Enchanter, Books, Tavern, Jewel, Food, General,
                                        Brothel, Gunsmith, Quests)
    for p in Positions:
        town_generator.write_people(town_generator.create_person(town_generator.create_variance()), p)
    for npc in NPC:
        town_generator.write_npc(PC(), npc)
    print("Writing the town ", town_name)
    town_generator.write_html(town_name)
