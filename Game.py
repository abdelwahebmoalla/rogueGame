import copy
import random
import tkinter as tk

import theGame
from Coord import Coord
from Equipment import Equipment, Gold
from Hero import Hero
from Map import Map
from Monster import Monster
from Stairs import Stairs
from Weapon import Weapon, Sword, Armor, Amulette
from handler import heal, feed


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
                      Equipment("food", "f", usage=lambda self, hero: feed(hero)),
                      Sword("Sword level 2", "s2", usage=None, extraStrength=100),
                      Sword("Sword level 1", "s1", usage=None, extraStrength=100),
                      Armor("Armure level 1", "a1", usage=None, extraDefense=2),
                      Armor("Armure level 2", "a2", usage=None, extraDefense=4),
                      Amulette("Amulette", "am", usage=None, extraHp=2),
                      Gold("gold", "g")],

                  1: [Equipment("potion", "!", usage=lambda self, hero: heal(hero)),
                      Equipment("food", "f", usage=lambda self, hero: feed(hero)),
                      Weapon("Sword level 2", "s2", usage=None, weapon_type="sword", extraStrength=100),
                      Weapon("Sword level 1", "s1", usage=None, weapon_type="sword", extraStrength=100),
                      Gold("gold", "g")
                      ],
                  2: [Equipment("potion", "!", usage=lambda self, hero: heal(hero)),
                      Equipment("food", "f", usage=lambda self, hero: feed(hero)),
                      Weapon("Sword level 2", "s2", usage=None, weapon_type="sword", extraStrength=100),
                      Weapon("Sword level 1", "s1", usage=None, weapon_type="sword", extraStrength=100),
                      Gold("gold", "g")
                      ],
                  3: [Equipment("potion", "!", usage=lambda self, hero: heal(hero)),
                      Equipment("food", "f", usage=lambda self, hero: feed(hero)),
                      Gold("gold", "g")],
                  4: [Equipment("potion", "!", usage=lambda self, hero: heal(hero)),
                      Equipment("food", "f", usage=lambda self, hero: feed(hero)),
                      Gold("gold", "g")]
                  }
    """ available monsters """
    # monsters = {0: [Creature("Goblin", 4), Creature("Bat", 2, "W")],
    #             1: [Creature("Ork", 6, strength=2), Creature("Blob", 10)], 5: [Creature("Dragon", 20, strength=3)]}

    monsters = {0: [Monster("Goblin", 4, "G", 2, 2), Monster("ORC", 2, "O", 4),
                    Monster("Goblin Fantome", 2, "GF", 1, showInMap=False)],
                1: [Monster("Goblin", 4, "G", 2, 2), Monster("ORC", 2, "O", 4),
                    Monster("Goblin Fantome", 2, "GF", 1, showInMap=False)],
                2: [Monster("Goblin", 4, "G", 2, 2), Monster("ORC", 2, "O", 4),
                    Monster("Goblin Fantome", 2, "GF", 1, showInMap=False)]}

    """ available actions """
    _actions = {'z': lambda h: theGame.theGame()._floor.move(h, Coord(0, -1)),
                'q': lambda h: theGame.theGame()._floor.move(h, Coord(-1, 0)),
                's': lambda h: theGame.theGame()._floor.move(h, Coord(0, 1)),
                'd': lambda h: theGame.theGame()._floor.move(h, Coord(1, 0)),
                'a': lambda h: theGame.theGame()._floor.move(h, Coord(-1, -1)),
                'e': lambda h: theGame.theGame()._floor.move(h, Coord(1, -1)),
                'x': lambda h: theGame.theGame()._floor.move(h, Coord(1, 1)),
                'w': lambda h: theGame.theGame()._floor.move(h, Coord(-1, 1)),
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
    _satietyConsumableActions = ['z', 'q', 's', 'd', 'u', 't', 'a', 'e', 'w', 'x']

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
        goblinFatome = tk.PhotoImage(file=basePath + "goblin_fantome.png")
        orc = tk.PhotoImage(file=basePath + "orc.png")
        sword_level1 = tk.PhotoImage(file=basePath + "sword.png")
        sword_level2 = tk.PhotoImage(file=basePath + "sword2.gif")
        stairs = tk.PhotoImage(file=basePath + "stairs.png")
        darkness = tk.PhotoImage(file=basePath + "darkness.png")
        armure_level1 = tk.PhotoImage(file=basePath + "armure.png")
        armure_level2 = tk.PhotoImage(file=basePath + "armure2.png")
        amulette = tk.PhotoImage(file=basePath + "amulette.png")
        gold = tk.PhotoImage(file=basePath + "gold.png")
        self.heroInterface = tk.PhotoImage(file=basePath + "hero_interface.png")
        self.imageMapping = {"@": hero, ".": brick, "!": potion, "f": food, "G": goblin, "O": orc, "E": stairs,
                             "darkness": darkness, "s1": sword_level1, "s2": sword_level2, "GF": goblinFatome,
                             "a1": armure_level1, "a2": armure_level2, "am": amulette, "g": gold}

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
        var = tk.StringVar()
        # bind any key to modify the variable
        self.root.bind("<Key>", lambda event: var.set(event.char))
        # wait for the variable to change
        self.root.wait_variable(var)
        # get the value of the variable
        value = var.get()
        # unbind the key
        self.root.unbind("<Key>")
        c = value
        if c.isdigit() and int(c) in range(len(l)):
            return l[int(c)]

    def updategraph(self) -> None:
        y = 160
        self.canvas.delete("all")
        for n in range(self.size):
            x = 32
            for m in range(self.size):
                if self._floor.showedCords[n][m]:
                # if True:
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
                        if type(current_position_object) == Monster:
                            # check if monster is shown in map or not
                            if current_position_object.showInMap:
                                self.canvas.create_image(x, y,
                                                         image=self.imageMapping.get(current_position_object.abbrv))
                            else:
                                self.canvas.create_image(x, y,
                                                         image=self.imageMapping.get("."))
                        else:
                            self.canvas.create_image(x, y,
                                                     image=self.imageMapping.get(current_position_object.abbrv))
                        # self.canvas.create_image(x, y,
                        #                          image=self.imageMapping.get(current_position_object.abbrv))
                x += 32
            y += 32
        self.canvas.create_text(32, 32, text="Game notifications", font="Arial 14 italic", fill="red", anchor="nw")
        self.canvas.create_text(32, 52, text=self.readMessages(), font="Arial 12 italic", fill="blue", anchor="nw")
        self.canvas.create_text(900, 32, text="Hero stats", font="Arial 14 italic", fill="red", anchor="nw")
        self.canvas.create_image(1050, 80, image=self.heroInterface)
        self.canvas.create_text(900, 54, text=f"Hp: {self._hero.hp}", font="Arial 12 italic", fill="red", anchor="nw")
        self.canvas.create_text(900, 74, text=f"Strength: {self._hero.strength}", font="Arial 12 italic", fill="red",
                                anchor="nw")
        self.canvas.create_text(900, 94, text=f"Defense: {self._hero.defense}", font="Arial 12 italic", fill="red",
                                anchor="nw")
        self.canvas.create_text(900, 114, text=f"Gold: {self._hero.gold}", font="Arial 12 italic", fill="red",
                                anchor="nw")
        self.canvas.create_text(900, 134, text=f"Satiety: {self._hero.satiety}", font="Arial 12 italic", fill="red",
                                anchor="nw")
        self.canvas.create_text(900, 154, text=f"Xp: {self._hero.xp}", font="Arial 12 italic", fill="red",
                                anchor="nw")
        self.canvas.create_text(900, 174, text=f"Level: {self._hero.level}", font="Arial 12 italic", fill="red",
                                anchor="nw")
        self.canvas.create_text(900, 200, text="Inventory", font="Arial 14 italic", fill="red", anchor="nw")
        initial_x = 900
        initial_y = 225
        for i in range(self._hero._inventorySize):
            if len(self._hero._inventory) > i:
                self.canvas.create_text(initial_x, initial_y, text=f"{i}: {self._hero._inventory[i].description()}",
                                        font="Arial 12 italic", fill="red", anchor="nw")
            else:
                self.canvas.create_text(initial_x, initial_y, text=f"{i}: empty",
                                        font="Arial 12 italic", fill="red", anchor="nw")
            initial_y += 20
        initial_y+=10
        self.canvas.create_text(900, initial_y, text="Active weapons", font="Arial 14 italic", fill="red", anchor="nw")
        for i in range(len(self._hero._activeWeapons)):
            initial_y+=20
            self.canvas.create_text(initial_x, initial_y, text=f"{i}: {self._hero._activeWeapons[i].description()}",
                                    font="Arial 12 italic", fill="red", anchor="nw")
        self.canvas.pack()
        if self._hero.hp < 1:
            self.endgame()

    def endgame(self) -> None:
        self.canvas.delete("all")
        self.canvas = tk.Canvas(self.root, width=1200, height=800, background="black")
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
            self._actions[event.char](self._hero)
            if event.char in Game._satietyConsumableActions:
                self._hero.consumeSatiety()
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
