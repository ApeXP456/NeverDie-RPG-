# Written by Jarod L. Cunningham
# Python
# Imports and Character & Dragon Class

import json
import random
import time

class Character:
    def __init__(self, name=None, char_class=None, strength=0, intelligence=0, agility=0, max_health=100, current_health=100, inventory=None, gold=0):
        self.name = name or "Unknown"
        self.char_class = char_class or "None"
        self.strength = strength
        self.intelligence = intelligence
        self.agility = agility
        self.max_health = max_health
        self.current_health = current_health if current_health else max_health
        self.inventory = inventory if inventory else ["health potion", "health potion", "sword", "map"]
        self.gold = gold

    def __str__(self):
        return (f"{self.name}, the {self.char_class} - Strength: {self.strength}, "
                f"Intelligence: {self.intelligence}, Agility: {self.agility}, "
                f"Health: {self.current_health}/{self.max_health}, Gold: {self.gold}")

    def take_damage(self, damage):
        self.current_health -= damage
        if self.current_health < 0:
            self.current_health = 0
        print(f"{self.name} takes {damage} damage! Current health: {self.current_health}/{self.max_health}")

    def heal(self, amount):
        self.current_health += amount
        if self.current_health > self.max_health:
            self.current_health = self.max_health
        print(f"{self.name} heals for {amount}! Current health: {self.current_health}/{self.max_health}")

    def use_potion(self):
        if "health potion" in self.inventory:
            self.heal(30)
            self.inventory.remove("health potion")
            print(f"{self.name} drinks a potion and restores 30 health!")
        else:
            print("You don't have any potions.")

class Dragon:
    def __init__(self, max_health=100):
        self.max_health = max_health
        self.current_health = max_health

    def take_damage(self, damage):
        self.current_health -= damage
        if self.current_health < 0:
            self.current_health = 0
        print(f"The dragon takes {damage} damage! Current health: {self.current_health}/{self.max_health}")

    def is_alive(self):
        return self.current_health > 0

def roll_d20():
    return random.randint(1, 20)

def player_attack(character, dragon):
    roll = roll_d20()
    attack_modifier = character.strength
    dragon_ac = 18
    total = roll + attack_modifier
    if total >= dragon_ac:
        damage = 20
        dragon.take_damage(damage)
        return True
    else:
        return False

def dragon_attack(character):
    roll = roll_d20()
    dragon_attack_modifier = 7
    player_ac = 15
    total = roll + dragon_attack_modifier
    if total >= player_ac:
        character.take_damage(15)
        return True
    else:
        return False
    
# encounter function
def encounter_dragon(character):
    dragon = Dragon()
    while dragon.is_alive() and character.current_health > 0:
        player_choice = input("Do you want to 'attack' the dragon or 'use potion'? ")
        if player_choice.lower() == 'attack':
            hit = player_attack(character, dragon)
            if hit:
                print(f"You hit the dragon!")
                if not dragon.is_alive():
                    print("You defeated the dragon and take its treasure!")
                    character.gold += 1000
                    character.inventory.append("health potion")
                    print(f"You receive 1000 gold and a health potion. Total gold: {character.gold}")
                    return True
            else:
                print("You missed the dragon.")
        elif player_choice.lower() == 'use potion':
            character.use_potion()

        if dragon.is_alive():
            hit = dragon_attack(character)
            if hit:
                print("The dragon hits you!")
                if character.current_health <= 0:
                    print("You were defeated by the dragon!")
                    return False
            else:
                print("The dragon missed its attack.")
    return True

# save and load function
def save_game(character):
    with open('game_save.json', 'w') as file:
        json.dump(character.__dict__, file)
    print("Game saved successfully.")

def load_game():
    try:
        with open('game_save.json', 'r') as file:
            data = json.load(file)
            character = Character(**data)
            print("Game loaded successfully.")
            return character
    except FileNotFoundError:
        print("No saved game found.")
        return None
    
#  character creattion and storyline
def display_intro():
    print('''Welcome to NeverDie, a mystical land of dragons and adventure...''')

def choose_class():
    classes = ["Warrior", "Mage", "Rogue"]
    print("Choose a class:")
    for i, char_class in enumerate(classes, 1):
        print(f"{i}. {char_class}")
    class_choice = 0
    while class_choice < 1 or class_choice > len(classes):
        class_choice = int(input("Enter the number of your class: "))
    return classes[class_choice - 1]

def distribute_attributes():
    total_points = 15
    attributes = {"Strength": 0, "Intelligence": 0, "Agility": 0}
    print("Distribute your attribute points (total: 15): ")
    for attribute in attributes:
        points = -1
        while points < 0 or points > total_points:
            points = int(input(f"Enter points for {attribute} (0-15): "))
            if points > total_points:
                print(f"Not enough points. You have {total_points} points left.")
        attributes[attribute] = points
        total_points -= points
    return attributes["Strength"], attributes["Intelligence"], attributes["Agility"]

def create_character():
    print("Character Creation")
    name = input("Enter your character's name: ")
    char_class = choose_class()
    strength, intelligence, agility = distribute_attributes()
    return Character(name, char_class, strength, intelligence, agility, max_health=100)

def move_forward(character):
    print("You cautiously move forward into the darkness...")
    if random.choice([True, False]):  # 50% chance of encountering a dragon
        print("Suddenly, a dragon appears before you!")
        outcome = encounter_dragon(character)
        if not outcome:
            print("Game over. You have been defeated.")
            exit(0)
    else:
        print("It's quiet... perhaps too quiet. You continue on your journey.")

# main loop
def main_game_loop(character):
    print(character)
    while True:
        print("What would you like to do?")
        print("1. Move forward")
        print("2. Check your inventory")
        print("3. Consult your map")
        print("4. Drink Potion")
        print("5. Exit game")
        print("6. Save game")
        print("7. Load game")
        choice = input("Enter your choice (1-7): ")

        if choice == "1":
            move_forward(character)

        elif choice == "2":
            print("You check your inventory:")
            for item in character.inventory:
                print(f" - {item}")
            print(f"Gold: {character.gold}")
            print(f"Current Health: {character.current_health}/{character.max_health}")

        elif choice == "3":
            if "map" in character.inventory:
                print("You consult your map and see that you are currently in the middle of a cave.")
            else:
                print("You don't have a map to consult.")

        elif choice == "4":
            character.use_potion()

        elif choice == "5":
            print("Thanks for playing! Exiting game...")
            exit(0)

        elif choice == "6":
            save_game(character)

        elif choice == "7":
            loaded_character = load_game()
            if loaded_character:
                character = loaded_character
                print(character)

        else:
            print("Invalid input. Please try again.")

def start_game():
    display_intro()
    load_choice = input("Do you want to load a saved game? (yes/no): ")
    if load_choice.lower() == 'yes':
        character = load_game()
        if character:
            main_game_loop(character)
            return
    character = create_character()
    main_game_loop(character)

if __name__ == "__main__":
    start_game()
