import random, math, datetime


class Node:
    def __init__(self, board, parent=None):
        self.board = board
        self.parent = parent
        self.children = []
        self.numOfPlays = 0
        self.numOfWins = 0
        self.numOfPlaysRave = 0
        self.numOfWinsRave = 0
        self.beta = 0.0
        self.threshold = 200
        self.untriedMoves = None
        self.steps = 40

    def getUntriedMoves(self):
        if self.untriedMoves is None:
            # self.untriedMoves = self.board.genLegalMoves()
            moves = self.board.genLegalMoves()
            self.untriedMoves = self.untryCandidates(moves)
        return self.untriedMoves

    def untryCandidates(self, moves):
        shortList = None
        candidates = []
        piece = self.board.piece
        for s, r, c in moves:
            self.board.grid[r][c] = piece
            score = self.board.evalBoard()
            candidates.append((score, r, c))
            self.board.grid[r][c] = '.'
        candidates.sort(reverse=True)
        M = min(len(candidates), 10)
        if piece == 'w':
            shortList = candidates[0:M]
        elif piece == 'b':
            shortList = candidates[-M:]
        return shortList

    def isTerminalNode(self):
        done, piece = self.board.isGameOver()
        return done

    def isFullyExpanded(self):
        return len(self.getUntriedMoves()) == 0

    def expand(self):
        move = self.getUntriedMoves().pop(0)
        newBoard = self.board.update(move[1], move[2], self.board.piece)
        childNode = Node(newBoard, parent=self)
        self.children.append(childNode)
        return childNode

    def rollout(self):
        actions = []
        currentBoard = self.board
        done, piece = currentBoard.isGameOver()
        step = 0
        begin = datetime.datetime.utcnow()
        while not done and step < self.steps:
            moves = currentBoard.genLegalMoves()
            if len(moves) == 0:
                return 'd', actions
            move = self.randomPolicy(moves)
            # move = random.choice(moves[0:20])   # default policy in simulation stage
            # move = self.simPolicy(currentBoard, moves)
            actions.append((move[1], move[2]))
            currentBoard = currentBoard.update(move[1], move[2], currentBoard.piece)
            step += 1
            done, piece = currentBoard.isGameOver()
            # done = False

        end = datetime.datetime.utcnow()
        # print("CheckTime = {}".format(end - begin))
        # print('rollout step = {}'.format(step))

        if not done and step == self.steps:
            return 'd', actions
        return piece, actions

    def randomPolicy(self, moves):
        return random.choice(moves)

    def simPolicy(self, board, moves):
        result, shortList = None, None
        candidates = []
        piece = board.piece
        for s, r, c in moves:
            board.grid[r][c] = piece
            score = board.evalBoard()
            candidates.append((score, r, c))
            board.grid[r][c] = '.'
        candidates.sort(reverse=True)
        M = min(len(candidates), 5)
        if piece == 'w':
            shortList = candidates[0:M]
        elif piece == 'b':
            shortList = candidates[-M:]
        result = random.choice(shortList)
        return result

    def backup(self, winner):
        self.numOfPlays += 1
        # if winner != 'd' and self.board.piece != winner:
        if self.board.piece != winner:
            self.numOfWins += 1
        if self.parent:
            self.parent.backup(winner)

    def backupRave(self, winner, states, actions):
        L = len(actions)
        for idx1, node in enumerate(states):
            p = node.parent
            for c in p.children:
                for idx2 in range(idx1, L, 2):
                    if actions[idx2] == c.board.preMove:
                        c.numOfPlaysRave += 1
                        # if winner != 'd' and c.board.piece != winner:
                        if c.board.piece != winner:
                            c.numOfWinsRave += 1


    def bestChild(self, coeff, option):
        val, maxVal, best = 0, -float('inf'), None
        for node in self.children:
            if option == 0:
                val = node.numOfWins / node.numOfPlays + coeff * math.sqrt(
                    2 * math.log(self.numOfPlays) / node.numOfPlays)
            elif option == 1:
                beta = max(0, (self.threshold - node.numOfPlays)/self.threshold)
                val = (1 - beta) * (node.numOfWins / node.numOfPlays) + beta * (
                            node.numOfWinsRave / node.numOfPlaysRave) + coeff * math.sqrt(
                    2 * math.log(self.numOfPlays) / node.numOfPlays)

            if val > maxVal:
                maxVal, best = val, node
        return best


class MCTS:
    def __init__(self, node, games):
        self.root = node
        self.timeLimit = datetime.timedelta(seconds=30)
        self.games = games
        self.states = []
        self.actions = []
        # self.moveLimit = 30

    def rave(self):
        option = 1
        games = 0
        begin = datetime.datetime.utcnow()
        while datetime.datetime.utcnow() - begin < self.timeLimit:
        # while games <= self.games:
            self.simulation(option)
            games += 1
            self.states, self.actions = [], []  # reset for each simulated game
        print('simulated games = {}'.format(games))
        # for node in self.root.children:
        #     print("preMove = {}, Plays = {}, Wins = {}, PlaysRave = {}, WinsRave = {}".format(node.board.preMove, node.numOfPlays, node.numOfWins, node.numOfPlaysRave, node.numOfWinsRave))
        return self.root.bestChild(0.0, option).board.preMove

    def search(self):
        option = 0
        games = 0
        begin = datetime.datetime.utcnow()
        while datetime.datetime.utcnow() - begin < self.timeLimit:
        # while games <= self.games:
            self.simulation(option)
            games += 1
            # self.states, self.actions = [], []  # reset for each simulated game
        print('simulated games = {}'.format(games))
        # for node in self.root.children:
        #     print("preMove = {}, Plays = {}, Wins = {}".format(node.board.preMove, node.numOfPlays, node.numOfWins))
        return self.root.bestChild(0.0, option).board.preMove

    def simulation(self, option):
        node = self.treePolicy(option)
        winner, actions = node.rollout()
        node.backup(winner)
        if option == 1:
            self.actions += actions
            node.backupRave(winner, self.states, self.actions)

    def treePolicy(self, option):
        currentNode = self.root
        # self.states.append(currentNode)
        while not currentNode.isTerminalNode():
            if not currentNode.isFullyExpanded():
                newNode = currentNode.expand()
                if option == 1:
                    self.states.append(newNode)
                    self.actions.append(newNode.board.preMove)
                return newNode
            else:
                currentNode = currentNode.bestChild(1.0, option)
                if option == 1:
                    self.states.append(currentNode)
                    self.actions.append(currentNode.board.preMove)
        return currentNode
