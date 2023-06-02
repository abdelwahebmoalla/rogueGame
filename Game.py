import copy
import random
import tkinter as tk

import theGame
from Coord import Coord
from Creature import Creature
from Equipment import Equipment
from Hero import Hero
from Map import Map
from Stairs import Stairs
from handler import heal, feed
from utils import getch


# should I add gold Equipment("gold", "g")
class Game(object):
    """ Class representing game state """

    """ available equipments """
    # equipments = {0: [Equipment("potion", "!", usage=lambda self, hero: heal(hero)),
    #                   Equipment("food", "f", usage=lambda self, hero: feed(hero)),
    #                   Weapon("Sword level 1", "s1", usage=None, weapon_type="sword", extraStrength=50),
    #                   Weapon("Sword level 2", "s2", usage=None, weapon_type="sword", extraStrength=100)],
    #
    #               1: [Equipment("potion", "!", usage=lambda self, hero: teleport(hero, True)),
    #                   Equipment("food", "f", usage=lambda self, hero: feed(hero)),
    #                   Weapon("Sword level 1", "s1", usage=None, weapon_type="sword", extraStrength=50),
    #                   Weapon("Sword level 2", "s2", usage=None, weapon_type="sword", extraStrength=100)
    #                   ],
    #               2: [Equipment("bow", usage=lambda self, hero: shoot(1, True)),
    #                   Equipment("food", "f", usage=lambda self, hero: feed(hero)),
    #                   Weapon("Sword level 1", "s1", usage=None, weapon_type="sword", extraStrength=50),
    #                   Weapon("Sword level 2", "s2", usage=None, weapon_type="sword", extraStrength=100)
    #                   ],
    #               3: [Equipment("portoloin", "w", usage=lambda self, hero: teleport(hero, False)),
    #                   Equipment("food", "f", usage=lambda self, hero: feed(hero)),
    #                   Weapon("Sword level 2", "s2", usage=None, weapon_type="sword", extraStrength=100)],
    #               4: [Equipment("portoloin", "w", usage=lambda self, hero: teleport(hero, False)),
    #                   Equipment("food", "f", usage=lambda self, hero: feed(hero)),
    #                   Weapon("Sword level 2", "s2", usage=None, weapon_type="sword", extraStrength=100)]
    #               }

    equipments = {0: [Equipment("potion", "!", usage=lambda self, hero: heal(hero)),
                      Equipment("food", "f", usage=lambda self, hero: feed(hero))],

                  1: [Equipment("potion", "!", usage=lambda self, hero: heal(hero)),
                      Equipment("food", "f", usage=lambda self, hero: feed(hero))],
                  2: [Equipment("potion", "!", usage=lambda self, hero: heal(hero)),
                      Equipment("food", "f", usage=lambda self, hero: feed(hero))],
                  3: [Equipment("potion", "!", usage=lambda self, hero: heal(hero)),
                      Equipment("food", "f", usage=lambda self, hero: feed(hero))],
                  4: [Equipment("potion", "!", usage=lambda self, hero: heal(hero)),
                      Equipment("food", "f", usage=lambda self, hero: feed(hero))]
                  }
    """ available monsters """
    # monsters = {0: [Creature("Goblin", 4), Creature("Bat", 2, "W")],
    #             1: [Creature("Ork", 6, strength=2), Creature("Blob", 10)], 5: [Creature("Dragon", 20, strength=3)]}

    monsters = {0: [Creature("Goblin", 4, "G"), Creature("ORC", 2, "O")],
                1: [Creature("Goblin", 4, "G"), Creature("ORC", 2, "O")],
                2: [Creature("Goblin", 4, "G"), Creature("ORC", 2, "O")]}

    """ available actions """
    _actions = {'z': lambda h: theGame.theGame()._floor.move(h, Coord(0, -1)),
                'q': lambda h: theGame.theGame()._floor.move(h, Coord(-1, 0)),
                's': lambda h: theGame.theGame()._floor.move(h, Coord(0, 1)),
                'd': lambda h: theGame.theGame()._floor.move(h, Coord(1, 0)),
                'i': lambda h: theGame.theGame().addMessage(h.fullDescription()),
                'k': lambda h: h.__setattr__('hp', 0),
                'u': lambda h: h.use(theGame.theGame().select(h._inventory)),
                't': lambda h: h.throw(theGame.theGame().select(h._inventory)),
                'r': lambda h: h.rest(),
                # ' ': lambda h: None,
                'h': lambda hero: theGame.theGame().addMessage(
                    "Actions disponibles : " + str(list(Game._actions.keys()))),
                'b': lambda hero: theGame.theGame().addMessage("I am " + hero.name),
                }
    _satietyConsumableActions = ['z', 'q', 's', 'd', 'u', 't']

    def __init__(self, level=1, hero=None, size=20):
        self._level = level
        self._messages = []
        if hero == None:
            hero = Hero()
        self._hero = hero
        self._floor = None
        self.size = size
        self.root = tk.Tk()
        basePath = "assets/"
        hero = tk.PhotoImage(file=basePath + "hero.png")
        brick = tk.PhotoImage(file=basePath + "brick.png")
        potion = tk.PhotoImage(file=basePath + "potion.png")
        food = tk.PhotoImage(file=basePath + "food.png")
        goblin = tk.PhotoImage(file=basePath + "goblin.png")
        orc = tk.PhotoImage(file=basePath + "orc.png")
        stairs = tk.PhotoImage(file=basePath + "stairs.png")
        darkness = tk.PhotoImage(file=basePath + "darkness.png")
        self.imageMapping = {"@": hero, ".": brick, "!": potion, "f": food, "G": goblin, "O": orc, "E": stairs,
                             "darkness": darkness}

    def buildFloor(self):
        """Creates a map for the current floor."""
        self._floor = Map(size=20, hero=self._hero)
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

    def updategraph(self) -> None:
        x = 128
        self.canvas.delete("all")
        for n in range(self.size):
            y = 128
            for m in range(self.size):
                # if self._floor.showedCords[n][m]:
                if True:
                    # prepare floor if object not floor
                    current_position_object = self._floor._mat[n][m]
                    if current_position_object == " ":  # empty
                        self.canvas.create_image(x, y,
                                                 image=self.imageMapping.get("darkness"))
                    elif current_position_object == ".":
                        self.canvas.create_image(x, y,
                                                 image=self.imageMapping.get("."))
                    else:
                        # prepare floor then create second object
                        self.canvas.create_image(x, y,
                                                 image=self.imageMapping.get("."))
                        self.canvas.create_image(x, y,
                                                 image=self.imageMapping.get(current_position_object.abbrv))
                y += 32
            x += 32
        self.canvas.create_text(85, 120, text=self.readMessages(), font="Arial 16 italic", fill="blue")
        self.canvas.create_text(85, 60, text=self._hero.description(), font="Arial 16 italic", fill="blue")
        self.canvas.pack()
        print(self._floor)
        if self._hero.hp < 1:
            self.endgame()

    def endgame(self) -> None:
        self.canvas.delete("all")
        self.canvas = tk.Canvas(self.fenetre, width=1200, height=800, background="black")
        self.canvas.place(x=0, y=0)
        self.canvas.create_text(85, 120, text="GAME OVER", font="Arial 16 italic", fill="blue")

    def generateGameInterface(self):
        self.canvas = tk.Canvas(self.root, width=1200, height=800, background="black")
        self.updategraph()
        [self.root.bind(i, self.action) for i in self._actions]
        self.canvas.pack()
        self.root.mainloop()

    def action(self, event):
        if event.char in self._actions:
            print("event.char",event.char)
            self._actions[event.char](self._hero)
        self._floor.moveAllMonsters()
        self.updategraph()

    def play(self):
        """Main game loop"""
        self.buildFloor()
        self.root.title('rogue Game')
        self.root.resizable(False, False)
        self.root.configure(background="black")
        # print("--- Welcome Hero! ---")
        # while self._hero.hp > 0:
        #     print(self._floor)
        #     print(self._hero.description())
        #     print(self.readMessages())
        #     c = getch()
        #     if c in Game._actions:
        #         Game._actions[c](self._hero)
        #     if c in Game._satietyConsumableActions:
        #         self._hero.consumeSatiety()
        #     self._floor.moveAllMonsters()
        self.generateGameInterface()
        print("--- Game Over ---")
        # self.root.mainloop()
