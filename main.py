#!/usr/bin/python3
import town_generator
from PC import PC
from os import linesep
from re import match
import simplejson as json

if __name__ == '__main__':
    generator = json.loads(open('generate.json', 'r').read())
    Weapons = [
        generator['Weapon Shops']["# of Stores"],
        generator['Weapon Shops']["Rarity Low"],
        generator['Weapon Shops']["Rarity High"],
        generator['Weapon Shops']["Quantity Low"],
        generator['Weapon Shops']["Quantity High"],
        generator['Weapon Shops']["Inflation"]
    ]
    Armor = [
        generator['Armor Shops']["# of Stores"],
        generator['Armor Shops']["Rarity Low"],
        generator['Armor Shops']["Rarity High"],
        generator['Armor Shops']["Quantity Low"],
        generator['Armor Shops']["Quantity High"],
        generator['Armor Shops']["Inflation"]
    ]
    Potion = [
        generator["Potion Shops"]["# of Stores"],
        generator["Potion Shops"]["Rarity Low"],
        generator["Potion Shops"]["Rarity High"],
        generator["Potion Shops"]["Quantity Low"],
        generator["Potion Shops"]["Quantity High"],
        generator["Potion Shops"]["Inflation"]
    ]
    Enchant = [
        generator['Enchant Shops']["# of Stores"],
        generator['Enchant Shops']["Rarity Low"],
        generator['Enchant Shops']["Rarity High"],
        generator['Enchant Shops']["Quantity Low"],
        generator['Enchant Shops']["Quantity High"],
        generator['Enchant Shops']["Inflation"]
    ]
    Enchanter = [
        generator["Enchanter Shops"]["# of Stores"],
        generator["Enchanter Shops"]["Rarity Low"],
        generator["Enchanter Shops"]["Rarity High"],
        generator["Enchanter Shops"]["Quantity Low"],
        generator["Enchanter Shops"]["Quantity High"],
        generator["Enchanter Shops"]["Inflation"]
    ]
    Books = [
        generator["Book Shops"]["# of Stores"],
        generator["Book Shops"]["Quantity Low"],
        generator["Book Shops"]["Quantity High"],
        generator["Book Shops"]["Inflation"]
    ]
    Tavern = [
        generator["Tavern Shops"]["# of Stores"],
        generator["Tavern Shops"]["Rooms"],
        generator["Tavern Shops"]["Quantity Low"],
        generator["Tavern Shops"]["Quantity High"],
        generator["Tavern Shops"]["Inflation"]
    ]
    Jewel = [
        generator["Jewel Shops"]["# of Stores"],
        generator["Jewel Shops"]["Rarity Low"],
        generator["Jewel Shops"]["Rarity High"],
        generator["Jewel Shops"]["Quantity Low"],
        generator["Jewel Shops"]["Quantity High"],
        generator["Jewel Shops"]["Inflation"]
    ]
    Food = [
        generator["Food Shops"]["# of Stores"],
        generator["Food Shops"]["Quantity Low"],
        generator["Food Shops"]["Quantity High"],
        generator["Food Shops"]["Inflation"]
    ]
    General = [
        generator["General Shops"]["# of Stores"],
        generator["General Shops"]["Rarity Low"],
        generator["General Shops"]["Rarity High"],
        generator["General Shops"]["Quantity Low"],
        generator["General Shops"]["Quantity High"],
        generator["General Shops"]["Trinkets"],
        generator["General Shops"]["Inflation"]
    ]
    Brothel = [
        generator["Brothels"]["# of Stores"],
        generator["Brothels"]["Quantity Low"],
        generator["Brothels"]["Quantity High"],
        generator["Brothels"]["Inflation"]
    ]
    Gunsmith = [
        generator["Gunsmiths"]["# of Stores"],
        generator["Gunsmiths"]["Rarity Low"],
        generator["Gunsmiths"]["Rarity High"],
        generator["Gunsmiths"]["Quantity Low"],
        generator["Gunsmiths"]["Quantity High"],
        generator["Gunsmiths"]["Inflation"]
    ]
    Quests = [
        generator["Quest Boards"]["# of Stores"],
        generator["Quest Boards"]["Level Low"],
        generator["Quest Boards"]["Level High"],
        generator["Quest Boards"]["Quantity"]
    ]

    town_name = town_generator.generate(Weapons, Armor, Potion, Enchant,
                                        Enchanter, Books, Tavern, Jewel, Food,
                                        General, Brothel, Gunsmith, Quests)

    for p in generator['Occupations']:
        town_generator.write_people(
            town_generator.create_person(town_generator.create_variance()), p)
    for npc in generator['NPCs']:
        town_generator.write_npc(PC(), npc)

    print("Writing the town ", town_name)
    town_generator.write_html(town_name)
