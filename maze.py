class Maze:
    def __init__(self):
        self.w = 5
        self.h = 5
        p = Tile.player
        b = Tile.block
        e = Tile.empty
        g = Tile.goal
        self.map = [
            [e, e, e, e, g],
            [e, e, e, e, e],
            [b, e, b, b, b],
            [e, e, e, e, e],
            [e, e, e, e, e],
        ]
        self.playerPos = (0, 4)
        self.gameWon = False
    def __repr__(self):
        returnStr = ""
        for i in range(self.h):
            for j in range(self.w):
                if (j, i) == self.playerPos:
                    returnStr += str(Tile.player)
                else:
                    returnStr += str(self.map[i][j])
            returnStr += "\n"
        return returnStr
    def tileAt(self, (x, y)):
        return self.map[y][x]
    def isValidPos(self, (x, y)):
        return all([x >= 0, y >= 0, x < self.w, y < self.h])
    def move(self, dir):
        movePos = addTuple(self.playerPos, dir)
        if self.isValidPos(movePos):
            if self.tileAt(movePos) == Tile.empty:
                self.playerPos = movePos
                return True
            elif self.tileAt(movePos) == Tile.goal:
                self.playerPos = movePos
                self.gameWon = movePos
                return True
            else:
                return False
        else:
            return False


def addTuple((a1, a2), (b1, b2)):
    return (a1 + b1, a2 + b2)

class Dir:
    UP = (0,-1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class Tile:
    player = 2
    goal = 3
    block = 1
    empty = 0

maze = Maze()
print maze
print maze.move(Dir.UP)
print maze
print maze.move(Dir.UP)
print maze
print maze.move(Dir.RIGHT)
print maze
print maze.move(Dir.UP)
print maze
print maze.move(Dir.UP)
print maze
print maze.move(Dir.UP)
print maze
print maze.move(Dir.UP)
print maze
print maze.move(Dir.RIGHT)
print maze
print maze.move(Dir.RIGHT)
print maze
print maze.move(Dir.RIGHT)
print maze
