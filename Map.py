import random
from collections import deque

from Coord import Coord
from Element import Element
from Hero import Hero
from Monster import Monster
from Room import Room
from utils import sign


class Map(object):
    """A map of a game floor.
        Contains game elements."""

    ground = '.'  # A walkable ground cell
    dir = {'z': Coord(0, -1), 's': Coord(0, 1), 'd': Coord(1, 0), 'q': Coord(-1, 0)}  # four direction user keys
    empty = ' '  # A non walkable cell

    def __init__(self, size=20, hero=None):
        self.size = size
        self._mat = []
        self._elem = {}
        self._rooms = []
        self._roomsToReach = []
        self.showedCords = []
        for i in range(size):
            self._mat.append([Map.empty] * size)
            self.showedCords.append([False] * size)
        if hero is None:
            hero = Hero()
        self._hero = hero
        self.generateRooms(7)
        self.reachAllRooms()
        heroInitialPosition = self._rooms[0].center()
        self.put(heroInitialPosition, hero)
        self.showedCords[heroInitialPosition.y][heroInitialPosition.x] = True
        self.showSurroundingCords(heroInitialPosition)
        for r in self._rooms:
            r.decorate(self)

    def showSurroundingCords(self, initialCord):
        possibleCoords = []
        for x in range(3):
            for y in range(3):
                possibleCoords += [Coord(x, y), Coord(x, -1 * y), Coord(-1 * x, y), Coord(-1 * x, -1 * y)]

        # possibleCoords = [Coord(0, 1), Coord(0, -1), Coord(-1, 0, ), Coord(1, 0), Coord(1, 1), Coord(-1, 1),
        #                   Coord(1, -1), Coord(-1, -1)]
        for cord in possibleCoords:
            try:
                newCord = initialCord + cord
                self.checkCoord(newCord)
                self.showedCords[newCord.y][newCord.x] = True
            except Exception as e:
                pass

    def addRoom(self, room):
        """Adds a room in the map."""
        self._roomsToReach.append(room)
        for y in range(room.c1.y, room.c2.y + 1):
            for x in range(room.c1.x, room.c2.x + 1):
                self._mat[y][x] = Map.ground

    def findRoom(self, coord):
        """If the coord belongs to a room, returns the room elsewhere returns None"""
        for r in self._roomsToReach:
            if coord in r:
                return r
        return None

    def intersectNone(self, room):
        """Tests if the room shall intersect any room already in the map."""
        for r in self._roomsToReach:
            if room.intersect(r):
                return False
        return True

    def dig(self, coord):
        """Puts a ground cell at the given coord.
            If the coord corresponds to a room, considers the room reached."""
        self._mat[coord.y][coord.x] = Map.ground
        r = self.findRoom(coord)
        if r:
            self._roomsToReach.remove(r)
            self._rooms.append(r)

    def corridor(self, cursor, end):
        """Digs a corridors from the coordinates cursor to the end, first vertically, then horizontally."""
        d = end - cursor
        self.dig(cursor)
        while cursor.y != end.y:
            cursor = cursor + Coord(0, sign(d.y))
            self.dig(cursor)
        while cursor.x != end.x:
            cursor = cursor + Coord(sign(d.x), 0)
            self.dig(cursor)

    def reach(self):
        """Makes more rooms reachable.
            Start from one random reached room, and dig a corridor to an unreached room."""
        roomA = random.choice(self._rooms)
        roomB = random.choice(self._roomsToReach)

        self.corridor(roomA.center(), roomB.center())

    def reachAllRooms(self):
        """Makes all rooms reachable.
            Start from the first room, repeats @reach until all rooms are reached."""
        self._rooms.append(self._roomsToReach.pop(0))
        while len(self._roomsToReach) > 0:
            self.reach()

    def randRoom(self):
        """A random room to be put on the map."""
        c1 = Coord(random.randint(0, len(self) - 3), random.randint(0, len(self) - 3))
        c2 = Coord(min(c1.x + random.randint(3, 8), len(self) - 1), min(c1.y + random.randint(3, 8), len(self) - 1))
        return Room(c1, c2)

    def generateRooms(self, n):
        """Generates n random rooms and adds them if non-intersecting."""
        for i in range(n):
            r = self.randRoom()
            if self.intersectNone(r):
                self.addRoom(r)

    def __len__(self):
        return len(self._mat)

    def __contains__(self, item):
        if isinstance(item, Coord):
            return 0 <= item.x < len(self) and 0 <= item.y < len(self)
        return item in self._elem

    def __repr__(self):
        s = ""
        for i in self._mat:
            for j in i:
                s += str(j)
            s += '\n'
        return s

    def checkCoord(self, c):
        """Check if the coordinates c is valid in the map."""
        if not isinstance(c, Coord):
            raise TypeError('Not a Coord')
        if not c in self:
            raise IndexError('Out of map coord')

    def checkElement(self, o):
        """Check if o is an Element."""
        if not isinstance(o, Element):
            raise TypeError('Not a Element')

    def put(self, c, o):
        """Puts an element o on the cell c"""
        self.checkCoord(c)
        self.checkElement(o)
        if self._mat[c.y][c.x] != Map.ground:
            raise ValueError('Incorrect cell')
        if o in self._elem:
            raise KeyError('Already placed')
        self._mat[c.y][c.x] = o
        self._elem[o] = c

    def get(self, c):
        """Returns the object present on the cell c"""
        self.checkCoord(c)
        return self._mat[c.y][c.x]

    def pos(self, o):
        """Returns the coordinates of an element in the map """
        self.checkElement(o)
        return self._elem[o]

    def rm(self, c):
        """Removes the element at the coordinates c"""
        self.checkCoord(c)
        del self._elem[self._mat[c.y][c.x]]
        self._mat[c.y][c.x] = Map.ground

    def move(self, e, way, calculated_dest=None):
        """Moves the element e in the direction way."""
        orig = self.pos(e)
        if calculated_dest:
            dest = calculated_dest
        else:
            dest = orig + way
        if dest in self:
            if self.get(dest) == Map.ground:
                self._mat[orig.y][orig.x] = Map.ground
                self._mat[dest.y][dest.x] = e
                self._elem[e] = dest
                if type(e) == Hero:
                    self.showSurroundingCords(dest)
            elif self.get(dest) != Map.empty and self.get(dest).meet(e) and self.get(dest) != self._hero:
                self.rm(dest)

    def moveAllMonsters(self):
        """Moves all monsters in the map.
            If a monster is at distance lower than 6 from the hero, the monster advances."""
        h = self.pos(self._hero)
        for e in self._elem:
            c = self.pos(e)
            if isinstance(e, Monster) and e != self._hero and c.distance(h) < 6:
                for i in range(e.actionPerRole):
                    c = self.pos(e)
                    nextCord = self.getShortestNextMovement(c, h)
                    if self.get(nextCord) in [Map.ground, self._hero]:
                        self.move(e, None, nextCord)

    def shortestRoute(self, start, end):
        matrix = self._mat
        # initialize a queue with the starting point
        queue = deque([start])
        # initialize a dictionary to store the distance and the previous node for each cell
        visited = {start: (0, None)}
        # initialize a list to store the route
        route = []
        # loop until the queue is empty or the end point is reached
        while queue:
            # get the current cell from the queue
            x, y = queue.popleft()
            # if the end point is reached, break the loop
            if (x, y) == end:
                break
            # get the current distance and the previous node
            dist, prev = visited[(x, y)]
            # loop through the four possible directions: up, down, left, right
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0), (-1, -1), (1, -1), (1, 1), (-1, 0)]:
                # get the next cell coordinates
                nx = x + dx
                ny = y + dy
                # check if the next cell is valid and not visited
                if 0 <= nx < len(matrix) and 0 <= ny < len(matrix[0]) and (nx, ny) not in visited and (
                        matrix[ny][nx] == Map.ground or type(matrix[ny][nx]) == Hero):
                    # add the next cell to the queue
                    queue.append((nx, ny))
                    # update the distance and the previous node for the next cell
                    visited[(nx, ny)] = (dist + 1, (x, y))
        # if the end point is not reached, return an empty route
        if (x, y) != end:
            return route
        # otherwise, backtrack from the end point to the start point using the previous nodes
        while (x, y) != start:
            # add the current cell to the route
            route.append((x, y))
            # get the previous node
            x, y = visited[(x, y)][1]
        # reverse the route to get it from start to end
        route.reverse()
        # return the route
        return route

    def getShortestNextMovement(self, start, end):
        start_cord = (start.x, start.y)
        end_cord = (end.x, end.y)
        shortest_route = self.shortestRoute(start_cord, end_cord)
        if shortest_route:
            return Coord(shortest_route[0][0], shortest_route[0][1])
        return start
