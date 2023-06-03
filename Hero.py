import theGame
from Creature import Creature
from Equipment import Equipment, Gold
from Weapon import Weapon

XP_PER_LEVEL = 10


class Hero(Creature):
    """The hero of the game.
        Is a creature. Has an inventory of elements. """

    def __init__(self, name="Hero", hp=50, abbrv="@", strength=2, defense=0, satiety=50, inventorySize=10):
        Creature.__init__(self, name, hp, abbrv, strength)
        self.xp = 0
        self.max_hp = hp
        self.level = 1
        self.defense = defense
        self.max_satiety = satiety
        self.satiety = satiety
        self._inventory = []
        self._inventorySize = inventorySize
        self._activeWeapons = []
        self.gold = 0

    def description(self):
        """Description of the hero"""
        return Creature.description(self)

    def fullDescription(self):
        """Complete description of the hero"""
        res = ''
        for e in self.__dict__:
            if e[0] != '_':
                res += '> ' + e + ' : ' + str(self.__dict__[e]) + '\n'
        res += '> INVENTORY : ' + str([x.name for x in self._inventory])
        return res

    def checkEquipment(self, o):
        """Check if o is an Equipment."""
        if not isinstance(o, Equipment):
            raise TypeError('Not a Equipment')

    def checkWeapon(self, weapon):
        if not isinstance(weapon, Weapon):
            raise TypeError('Not a Weapon')

    def unequipWeapon(self, weapon):
        self._activeWeapons.remove(weapon)
        self.strength -= weapon.extraStrength
        self.defense -= weapon.extraDefense
        self.hp -= weapon.extraHp

    def equipWeapon(self, weapon: Weapon):
        self.checkWeapon(weapon)
        self.strength += weapon.extraStrength
        self.defense += weapon.extraDefense
        self.hp += weapon.extraHp
        self._activeWeapons.append(weapon)

    def take(self, elem):
        """The hero takes adds the equipment to its inventory"""
        self.checkEquipment(elem)
        if type(elem) == Gold:
            self.gold += 1
        else:
            if len(self._inventory) >= self._inventorySize:
                theGame.theGame().addMessage(f"you reached maxmimum inventory size {self._inventorySize}")
            else:
                theGame.theGame().addMessage(f"element {elem.name} was added to inventory")
                self._inventory.append(elem)

    def use(self, elem: Equipment):
        """Use a piece of equipment"""
        if elem is None:
            return
        self.checkEquipment(elem)
        if elem not in self._inventory:
            raise ValueError('Equipment ' + elem.name + 'not in inventory')
        if elem.use(self):
            self._inventory.remove(elem)

    def throw(self, elem):
        if elem is None:
            return
        self.checkEquipment(elem)
        if elem not in self._inventory:
            raise ValueError('Equipment ' + elem.name + 'not in inventory')
        self._inventory.remove(elem)

    def gainXP(self, xp):
        self.xp = self.xp + xp
        if self.xp >= XP_PER_LEVEL * self.level:
            # If yes, call the level up method
            self.levelUp()

    def levelUp(self):
        self.level += 1
        self.max_hp += self.level
        self.hp = self.max_hp
        self.strength += self.level
        self.defense += self.level
        self.max_satiety += self.level
        self.satiety = self.max_satiety

    def rest(self):
        self.hp = self.hp + 5
        for i in range(10):
            theGame.theGame()._floor.moveAllMonsters()

    def consumeSatiety(self, statietyConsumed=3):
        if self.satiety > 0:
            self.satiety -= statietyConsumed
        else:
            # satiety=0 we remove 1 hp
            self.hp -= 1

    def equipedWeaponsUsed(self):
        for weapon in self._activeWeapons:
            weapon.usageCount -= 1
            if weapon.usageCount <= 0:
                self.unequipWeapon(weapon)

    def meet(self, monster):
        """The hero is encountered by another creature(Monster).
            The other one hits the creature. Return True if the creature is dead."""
        theGame.theGame().addMessage(f"hero HP:{self.hp} meeting monster")
        self.hp -= 0 if monster.strength - self.defense < 0 else monster.strength - self.defense
        theGame.theGame().addMessage(f"hero Hp:{self.hp} after meeting monster")
        monster.showInMap = True
        theGame.theGame().addMessage("The " + monster.name + " hits the " + self.description())
        if self.hp > 0:
            return False
        return True
