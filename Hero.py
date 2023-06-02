from Creature import Creature
from Equipment import Equipment
from Weapon import Weapon

XP_PER_LEVEL = 10


class Hero(Creature):
    """The hero of the game.
        Is a creature. Has an inventory of elements. """

    def __init__(self, name="Hero", hp=10, abbrv="@", strength=2, defense=0, satiety=100, inventorySize=10):
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

    def description(self):
        """Description of the hero"""
        return Creature.description(self) + str(self._inventory)

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
        if len(self._inventory) >= self._inventorySize:
            from main import theGame
            theGame.theGame().addMessage(f"you reached maxmimum inventory size {self._inventorySize}")
        else:
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
        from main import theGame
        for i in range(10):
            theGame.theGame()._floor.moveAllMonsters()

    def consumeSatiety(self, statietyConsumed=1):
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
