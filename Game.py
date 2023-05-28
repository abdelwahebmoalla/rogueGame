from Equipment import Equipment
from Creature import Creature
from Coord import Coord
from Hero import Hero
from Map import Map
from Stairs import Stairs
from handler import heal, teleport, throw
from utils import getch
import theGame

import random, copy

class Game(object):
    """ Class representing game state """

    """ available equipments """
    equipments = {0: [Equipment("potion", "!", usage=lambda self, hero: heal(hero)), \
                      Equipment("gold", "o")], \
                  1: [Equipment("potion", "!", usage=lambda self, hero: teleport(hero, True))], \
                  2: [Equipment("bow", usage=lambda self, hero: throw(1, True))], \
                  3: [Equipment("portoloin", "w", usage=lambda self, hero: teleport(hero, False))], \
                  }
    """ available monsters """
    monsters = {0: [Creature("Goblin", 4), Creature("Bat", 2, "W")],
                1: [Creature("Ork", 6, strength=2), Creature("Blob", 10)], 5: [Creature("Dragon", 20, strength=3)]}

    """ available actions """
    _actions = {'z': lambda h: theGame.theGame()._floor.move(h, Coord(0, -1)), \
                'q': lambda h: theGame.theGame()._floor.move(h, Coord(-1, 0)), \
                's': lambda h: theGame.theGame()._floor.move(h, Coord(0, 1)), \
                'd': lambda h: theGame.theGame()._floor.move(h, Coord(1, 0)), \
                'i': lambda h: theGame.theGame().addMessage(h.fullDescription()), \
                'k': lambda h: h.__setattr__('hp', 0), \
                'u': lambda h: h.use(theGame.theGame().select(h._inventory)), \
                ' ': lambda h: None, \
                'h': lambda hero: theGame.theGame().addMessage("Actions disponibles : " + str(list(Game._actions.keys()))), \
                'b': lambda hero: theGame.theGame().addMessage("I am " + hero.name), \
                }

    def __init__(self, level=1, hero=None):
        self._level = level
        self._messages = []
        if hero == None:
            hero = Hero()
        self._hero = hero
        self._floor = None

    def buildFloor(self):
        """Creates a map for the current floor."""
        self._floor = Map(hero=self._hero)
        self._floor.put(self._floor._rooms[-1].center(), Stairs())
        self._level += 1

    def addMessage(self, msg):
        """Adds a message in the message list."""
        self._messages.append(msg)

    def readMessages(self):
        """Returns the message list and clears it."""
        s = ''
        for m in self._messages:
            s += m + '. '
        self._messages.clear()
        return s

    def randElement(self, collect):
        """Returns a clone of random element from a collection using exponential random law."""
        x = random.expovariate(1 / self._level)
        for k in collect.keys():
            if k <= x:
                l = collect[k]
        return copy.copy(random.choice(l))

    def randEquipment(self):
        """Returns a random equipment."""
        return self.randElement(Game.equipments)

    def randMonster(self):
        """Returns a random monster."""
        return self.randElement(Game.monsters)

    def select(self, l):
        print("Choose item> " + str([str(l.index(e)) + ": " + e.name for e in l]))
        c = getch()
        if c.isdigit() and int(c) in range(len(l)):
            return l[int(c)]

    def play(self):
        """Main game loop"""
        self.buildFloor()
        print("--- Welcome Hero! ---")
        while self._hero.hp > 0:
            print()
            print(self._floor)
            print(self._hero.description())
            print(self.readMessages())
            c = getch()
            if c in Game._actions:
                Game._actions[c](self._hero)
            self._floor.moveAllMonsters()
        print("--- Game Over ---")
