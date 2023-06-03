from Element import Element


class Creature(Element):
    """A creature that occupies the dungeon.
        Is an Element. Has hit points and strength."""

    def __init__(self, name, hp, abbrv="", strength=1):
        Element.__init__(self, name, abbrv)
        self.hp = hp
        self.strength = strength
        self.xp = self.strength * 5

    def description(self):
        """Description of the creature"""
        return Element.description(self) + "(" + str(self.hp) + ")" + "(" + str(self.strength) + ")" + "(" + str(
            self.xp) + ")"

    # def meet(self, other):
    #     """The creature is encountered by an other creature.
    #         The other one hits the creature. Return True if the creature is dead."""
    #     from Hero import Hero
    #     if type(self) == Hero:
    #         self.hp -= 0 if other.strength - self.defense < 0 else other.strength - self.defense
    #     else:
    #         self.hp -= other.strength
    #     theGame.theGame().addMessage("The " + other.name + " hits the " + self.description())
    #     if self.hp > 0:
    #         # IF HERO KILLS MONSTER it takes its XP
    #         from Hero import Hero
    #         if type(other) == Hero:
    #             other.gainXP(self.xp)
    #             other.equipedWeaponsUsed()
    #         return False
    #     return True

    def meet(self, creature):
        raise NotImplementedError('Abstract Element')
