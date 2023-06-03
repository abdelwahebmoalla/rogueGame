import theGame
from Element import Element


class Equipment(Element):
    """A piece of equipment"""

    def __init__(self, name, abbrv="", usage=None):
        Element.__init__(self, name, abbrv)
        self.usage = usage

    def meet(self, hero):
        """Makes the hero meet an element. The hero takes the element."""
        # check if creature is hero:
        from Hero import Hero
        if isinstance(hero, Hero):
            hero.take(self)
            theGame.theGame().addMessage("You pick up a " + self.name)
        return True

    def use(self, creature):
        """Uses the piece of equipment. Has effect on the hero according usage.
            Return True if the object is consumed."""
        if self.usage is None:
            theGame.theGame().addMessage("The " + self.name + " is not usable")
            return False
        else:
            theGame.theGame().addMessage("The " + creature.name + " uses the " + self.name)
            return self.usage(self, creature)


class Gold(Equipment):
    pass
