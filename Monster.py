from Creature import Creature
import theGame

XP_PER_LEVEL = 10


class Monster(Creature):
    """The hero of the game.
        Is a creature. Has an inventory of elements. """

    def __init__(self, name="Hero", hp=10, abbrv="@", strength=2, actionPerRole=1, showInMap=True):
        Creature.__init__(self, name, hp, abbrv, strength)
        self.actionPerRole = actionPerRole
        self.showInMap = showInMap

    def meet(self, hero):
        """The monster is encountered by a hero.
            The other one hits the creature. Return True if the creature is dead."""
        theGame.theGame().addMessage(f"monster HP:{self.hp} meeting hero")
        self.hp -= hero.strength
        self.showInMap = True
        theGame.theGame().addMessage(f"monster Hp:{self.hp} after meeting hero")
        theGame.theGame().addMessage("The " + hero.name + " hits the " + self.description())
        if self.hp <= 0:
            # IF HERO KILLS MONSTER it takes its XP
            theGame.theGame().addMessage("hero killed monster")
            hero.gainXP(self.xp)
            hero.equipedWeaponsUsed()
            return True
        return False
