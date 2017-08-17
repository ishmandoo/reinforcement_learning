import numpy as np
from random import randint

class Maze:
    def __init__(self):
        self.w = 5
        self.h = 5
        p = Tile.player
        b = Tile.block
        e = Tile.empty
        g = Tile.goal
        self.map = [
            [e, e, e, b, g],
            [e, b, e, b, e],
            [e, b, e, e, e],
            [e, b, b, b, b],
            [e, e, e, e, e],
        ]
        self.reset()
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
    def reset(self):
        self.playerPos = (0, 4)
        self.gameWon = False
    def move(self, dir):
        movePos = addTuple(self.playerPos, dir)
        if self.isValidPos(movePos):
            if self.tileAt(movePos) == Tile.empty:
                self.playerPos = movePos
                return 0
            elif self.tileAt(movePos) == Tile.goal:
                self.playerPos = movePos
                self.gameWon = True
                return 1
            else:
                return 0
        else:
            return 0

class QLearner:
    def __init__(self, maze):
        self.maze = maze
        self.Q = np.zeros((self.maze.w, self.maze.h, 4))
        self.alpha = 0.1
        self.gamma = 0.9
    def learn(self, n):
        for r in range(n):
            while self.maze.gameWon == False:
                i = randint(0,3)
                self.updateQ(i)
            self.maze.reset()
    def updateQ(self, i):
        x0, y0 = self.maze.playerPos
        moveDir = Dir.moveOptions[i]
        reward = self.maze.move(moveDir)
        x, y = self.maze.playerPos

        maxQ = max(self.Q[x, y, [0,1,2,3]])

        self.Q[x0, y0, i] = self.Q[x0, y0, i] + (self.alpha * (reward + (self.gamma * maxQ) - self.Q[x0, y0, i]))
    def getBestMove(self, (x, y)):
        bestMove = Dir.moveOptions[np.argmax(self.Q[x, y, [0,1,2,3]])]
        return bestMove


def addTuple((a1, a2), (b1, b2)):
    return (a1 + b1, a2 + b2)

class Dir:
    UP = (0,-1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)
    moveOptions = [UP, RIGHT, DOWN, LEFT]

class Tile:
    player = 'p'
    goal = 'g'
    block = 'X'
    empty = ' '

maze = Maze()
learner = QLearner(maze)
learner.learn(1000)

maze.reset()
while maze.gameWon == False:
    maze.move(learner.getBestMove(maze.playerPos))
    print maze
