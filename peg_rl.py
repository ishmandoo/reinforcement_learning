
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


if __name__ == "__main__":
    # parameters
    epsilon = .1  # exploration
    num_actions = 3  # [move_left, stay, move_right]
    epoch = 1000
    max_memory = 500
    hidden_size = 100
    batch_size = 50
    grid_size = 10

    model = Sequential()
    model.add(Dense(hidden_size, input_shape=(grid_size**2,), activation='relu'))
    model.add(Dense(hidden_size, activation='relu'))
    model.add(Dense(num_actions))
    model.compile(sgd(lr=.2), "mse")

    # If you want to continue training from a previous model, just uncomment the line bellow
    # model.load_weights("model.h5")

    # Define environment/game
    env = Catch(grid_size)

    # Initialize experience replay object
    exp_replay = ExperienceReplay(max_memory=max_memory)

    # Train
    win_cnt = 0
    for e in range(epoch):
        loss = 0.
        env.reset()
        game_over = False
        # get initial input
        input_t = env.observe()

        while not game_over:
            input_tm1 = input_t
            # get next action
            if np.random.rand() <= epsilon:
                action = np.random.randint(0, num_actions, size=1)
            else:
                q = model.predict(input_tm1)
                action = np.argmax(q[0])

            # apply action, get rewards and new state
            input_t, reward, game_over = env.act(action)
            if reward == 1:
                win_cnt += 1

            # store experience
            exp_replay.remember([input_tm1, action, reward, input_t], game_over)

            # adapt model
            inputs, targets = exp_replay.get_batch(model, batch_size=batch_size)

            loss += model.train_on_batch(inputs, targets)[0]
        print("Epoch {:03d}/999 | Loss {:.4f} | Win count {}".format(e, loss, win_cnt))

    # Save trained model weights and architecture, this will be used by the visualization code
    model.save_weights("model.h5", overwrite=True)
    with open("model.json", "w") as outfile:
        json.dump(model.to_json(), outfile)
