import theGame

def heal(creature):
    """Heal the creature"""
    creature.hp += 3
    return True

def teleport(creature, unique):
    """Teleport the creature"""
    r = theGame.theGame()._floor.randRoom()
    c = r.randCoord()
    theGame.theGame()._floor.rm(theGame.theGame()._floor.pos(creature))
    theGame.theGame()._floor.put(c, creature)
    return unique

def throw(power, loss):
    """Throw an object"""
    pass