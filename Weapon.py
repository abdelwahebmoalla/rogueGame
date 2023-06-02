import theGame
from Equipment import Equipment


class Weapon(Equipment):
    def __init__(self, name, symbol, usage=None, weapon_type="", maxUsageCount=10, extraStrength=0, extraDefense=0,
                 extraHp=0):
        super().__init__(name, symbol, usage)
        self.usageCount = 0
        self.maxUsageCount = maxUsageCount
        self.extraStrength = extraStrength
        self.extraHp = extraHp
        self.extraDefense = extraDefense
        self.weapon_type = weapon_type

    def use(self, creature):
        """Uses the piece of equipment. Has effect on the hero according usage.
            Return True if the object is consumed."""
        # check if weapon is active
        game = theGame.theGame()
        # check if same type of weapon included
        if self.weaponUsable():
            addWeapon = True
            for active_weapon in game._hero._activeWeapons:
                if active_weapon.name == self.name:
                    # weapon already included
                    addWeapon = False
                    break
                if active_weapon.weapon_type == self.weapon_type:
                    # unequip old weapon
                    game._hero.unequipWeapon(active_weapon)
                    break
            if addWeapon:
                game._hero.equipWeapon(self)
                game.addMessage("The " + self.name + " equiped")
        else:
            game.addMessage("The " + self.name + "cannot be equiped")
        if self.usage is None:
            game.addMessage("The " + self.name + " is not usable")
            return False
        else:
            game.addMessage("The " + creature.name + " uses the " + self.name)
            return self.usage(self, creature)

    def weaponUsable(self):
        if self.usageCount >= self.maxUsageCount:
            return False
        else:
            return True


class Sword(Weapon):
    def __init__(self, name, symbol, usage=None, extraStrength=1):
        super().__init__(name, symbol, usage=usage, weapon_type="sword", extraStrength=extraStrength)


class Armor(Weapon):
    def __init__(self, name, symbol, usage=None, extraDefense=1):
        super().__init__(name, symbol, usage=usage, weapon_type="armor", extraDefense=extraDefense)


class Amulette(Weapon):
    def __init__(self, name, symbol, usage=None, extraHp=1):
        super().__init__(name, symbol, usage=usage, weapon_type="amulette", extraHp=extraHp)
