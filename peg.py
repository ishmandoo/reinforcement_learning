
class Game:
    def __init__(self, w, h):
        # makes a 2d list for the board
        self.board = [[True for j in range(w)] for i in range(h)]
        # remvoes one peg to start
        self.board[0][0] = False
        self.w = w
        self.h = h
    def __repr__(self):
        returnStr = ""
        for i in range(self.h):
            for j in range(self.w):
                if self.isOccupied((j, i)):
                    returnStr += "X"
                else:
                    returnStr += " "
            returnStr += "\n"
        return returnStr
    def go(self, (x, y), dir):
        # adds direction once for the kill position and twice for the move position
        killPos = addTuple((x, y), dir)
        movePos = addTuple(killPos, dir)
        if self.isOccupied((x, y)):
            if not self.isOccupied(movePos):
                if self.isValidPos(movePos):
                    if self.isOccupied(killPos):
                        self.removePeg((x, y))
                        self.removePeg(killPos)
                        self.addPeg(movePos)

    def isValidPos(self, (x, y)):
        return all([x >= 0, y >= 0, x < self.w, y < self.h])
    def isOccupied(self, (x, y)):
        return self.board[y][x]
    def addPeg(self, (x, y)):
        self.board[y][x] = True
    def removePeg(self, (x, y)):
        self.board[y][x] = False

def addTuple((a1, a2), (b1, b2)):
    return (a1 + b1, a2 + b2)

assert(addTuple((1,1),(1,1)) == (2,2))

class Dir:
    UP = (0,-1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)



game = Game(5,5)
print game
game.go((2,0), Dir.LEFT)
print game
game.go((2,2), Dir.UP)
print game
