import pygame
from chessboard import Chessboard
from mcts import MCTS, Node
from minimax import MINIMAX
import datetime
import time


class Gomoku:

    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((800, 600))
        # self.screen = pygame.display.set_mode((500, 500))

        pygame.display.set_caption("Gomoku")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(r"C:\Windows\Fonts\consola.ttf", 24)
        self.going = True
        self.turn = 1  # 1 for black, 2 for white
        self.steps = 0

        self.gridSize = 15  #15
        self.grid = []
        for i in range(self.gridSize):
            self.grid.append(list("." * self.gridSize))
        self.player = 'b'
        self.preMove = None

        self.chessboard = Chessboard(self.grid, self.player, self.preMove)

        self.timeWhite = 0
        self.timeBlack = 0


    def humanPlayLoop(self):
        while self.going:
            self.update()
            self.draw()
            # result = self.chessboard.evalBoard()
            # print("result = {}".format(result))
            self.clock.tick(60)
        pygame.quit()

    def agentSelfPlayLoop(self, N):
        numGames = N
        black, white = 0, 0
        for i in range(numGames):
            gameOver = False
            while not gameOver:
            # while not self.chessboard.game_over:
                # self.randomAgentPlayer()
                # self.randomAgentPlayer()

                # self.minimaxAgentPlayerBlack()
                self.greedyAgentPlayer()
                # self.minimaxAgentPlayerWhite()
                self.mctsAgentPlayer(1500)
                # self.mctsRaveAgentPlayer(1500)
                gameOver, _ = self.chessboard.isGameOver()
                self.clock.tick(60)

            if self.chessboard.winner == 'b':
                print("Game {}: {} won, using {} steps".format(i + 1, 'black', self.steps))
                black += 1
            elif self.chessboard.winner == 'w':
                print("Game {}: {} won, using {} steps".format(i + 1, 'white', self.steps))
                white += 1
            else:
                print("Game {}: draw, using {} steps".format(i + 1, self.steps))

            self.steps = 0
            self.chessboard.reset()

        print("Black won: {}, White won: {}".format(black, white))
        # while True:
        #     i = 1
        pygame.quit()

    def agentSelfBetterPlayLoop(self, N):
        numGames = N
        black, white = 0, 0
        for i in range(numGames):
            self.draw()
            gameOver = False
            while not gameOver:
            # while not self.chessboard.game_over:
                # self.randomAgentPlayer()
                # self.randomAgentPlayer()

                # self.minimaxAgentPlayerBlack()
                # self.greedyAgentPlayer()
                # self.minimaxAgentPlayerWhite()
                self.mctsRaveAgentPlayer(1500, 3)
                self.mctsAgentPlayer(1500, 15)
                gameOver, _ = self.chessboard.isGameOver()
                self.clock.tick(60)

            if self.chessboard.winner == 'b':
                print("Game {}: {} won, using {} steps".format(i + 1, 'black', self.steps))
                black += 1
            elif self.chessboard.winner == 'w':
                print("Game {}: {} won, using {} steps".format(i + 1, 'white', self.steps))
                white += 1
            else:
                print("Game {}: draw, using {} steps".format(i + 1, self.steps))

            time.sleep(20)

            self.steps = 0
            self.chessboard.reset()

        print("Black won: {}, White won: {}".format(black, white))
        # while True:
        #     i = 1
        pygame.quit()


    def agentSelfDumbPlayLoop(self, N):
        numGames = N
        black, white = 0, 0
        for i in range(numGames):
            self.draw()
            gameOver = False
            while not gameOver:
                self.greedyAgentPlayer()
                # self.greedyAgentPlayer()
                self.mctsAgentPlayer(1500, 1)
                gameOver, _ = self.chessboard.isGameOver()
                self.clock.tick(60)

            if self.chessboard.winner == 'b':
                print("Game {}: {} won, using {} steps".format(i + 1, 'black', self.steps))
                black += 1
            elif self.chessboard.winner == 'w':
                print("Game {}: {} won, using {} steps".format(i + 1, 'white', self.steps))
                white += 1
            else:
                print("Game {}: draw, using {} steps".format(i + 1, self.steps))

            time.sleep(10)

            self.steps = 0
            self.chessboard.reset()

        print("Black won: {}, White won: {}".format(black, white))
        # while True:
        #     i = 1
        pygame.quit()


    def agentHumanPlayLoop(self):
        while self.going:
            # self.humanPlayer()
            # self.minimaxAgentPlayerWhite()

            # self.minimaxAgentPlayerBlack()
            self.humanPlayer()
            self.mctsAgentPlayer(1500, 3)
            # self.mctsRaveAgentPlayer(1500)
            # self.minimaxAgentPlayerWhite()
            self.clock.tick(60)
        pygame.quit()

    def randomAgentPlayer(self):
        gameOver, _ = self.chessboard.isGameOver()
        if not gameOver:
        # if not self.chessboard.game_over:
            r, c = self.chessboard.genRandomMove()
            done = self.chessboard.set_piece(r, c)
            if done:
                print("Turn {}: ({},{})".format(self.turn, r, c))
                self.chessboard.check_win(r, c)
        if self.turn == 1:
            self.turn = 2
        elif self.turn == 2:
            self.turn = 1
        self.draw()

    def greedyAgentPlayer(self):
        gameOver, _ = self.chessboard.isGameOver()
        if not gameOver:
        # if not self.chessboard.game_over:
            print("Agent Greedy's turn...")
            s, r, c = self.chessboard.greedyAgent(self.turn, 3)
            done = self.chessboard.set_piece(r, c)
            if done:
                if self.turn == 1:
                    self.steps += 1
                print("Agent Greedy: step = {}, ({},{})".format(self.steps, r, c))
                self.chessboard.check_win(r, c)
        if self.turn == 1:
            self.turn = 2
        elif self.turn == 2:
            self.turn = 1
        self.draw() ##

    def minimaxAgentPlayerWhite(self):
        gameOver, _ = self.chessboard.isGameOver()
        if not gameOver:
        # if not self.chessboard.game_over:
            print("Agent MINIMAX white's turn...")
            minimax = MINIMAX(self.chessboard)
            begin = datetime.datetime.utcnow()
            s, r, c = minimax.minimaxAgentWithPrunning(self.turn, 1)
            end = datetime.datetime.utcnow()
            print("Time = {}".format(end - begin))
            if r == -1 and c == -1:
                return
            done = self.chessboard.set_piece(r, c)
            if done:
                print("Agent White minimax: step = {}, ({},{})".format(self.steps, r, c))
                self.chessboard.check_win(r, c)
        if self.turn == 1:
            self.turn = 2
        elif self.turn == 2:
            self.turn = 1
        self.draw()

    def minimaxAgentPlayerBlack(self):
        gameOver, _ = self.chessboard.isGameOver()
        if not gameOver:
        # if not self.chessboard.game_over:
            print("Agent MINIMAX black's turn...")
            minimax = MINIMAX(self.chessboard)
            begin = datetime.datetime.utcnow()
            s, r, c = minimax.minimaxAgentWithPrunningBlack(self.turn, 1)
            end = datetime.datetime.utcnow()
            print("Time = {}".format(end - begin))
            # self.timeBlack += (end - begin)
            if r == -1 and c == -1:
                return
            done = self.chessboard.set_piece(r, c)
            if done:
                if self.turn == 1:
                    self.steps += 1
                print("Agent Black: step = {}, ({},{})".format(self.steps, r, c))
                self.chessboard.check_win(r, c)
        if self.turn == 1:
            self.turn = 2
        elif self.turn == 2:
            self.turn = 1
        # self.draw()

    def mctsAgentPlayer(self, games, timelimit = 30):
        gameOver, _ = self.chessboard.isGameOver()
        if not gameOver:
        # if not self.chessboard.game_over:
            print("Agent MCTS's turn...")
            root = Node(self.chessboard)
            mcts = MCTS(root, games, timelimit)
            begin = datetime.datetime.utcnow()
            r, c = mcts.search()
            end = datetime.datetime.utcnow()
            print("MCTS Time = {}".format(end - begin))
            done = self.chessboard.set_piece(r, c)
            if done:
                if self.turn == 1:
                    self.steps += 1
                print("Agent MCTS: step = {}, ({},{})".format(self.steps, r, c))
                self.chessboard.check_win(r, c)
        if self.turn == 1:
            self.turn = 2
        elif self.turn == 2:
            self.turn = 1
        self.draw() ##

    def mctsRaveAgentPlayer(self, games, timelimit = 30):
        gameOver, _ = self.chessboard.isGameOver()
        if not gameOver:
        # if not self.chessboard.game_over:
            print("Agent MCTS-RAVE's turn...")
            root = Node(self.chessboard)
            mcts = MCTS(root, games, timelimit)
            begin = datetime.datetime.utcnow()
            r, c = mcts.rave()
            end = datetime.datetime.utcnow()
            print("MCTS-RAVE Time = {}".format(end - begin))
            done = self.chessboard.set_piece(r, c)
            if done:
                if self.turn == 1:
                    self.steps += 1
                print("Agent MCTS: step = {}, ({},{})".format(self.steps, r, c))
                self.chessboard.check_win(r, c)
        if self.turn == 1:
            self.turn = 2
        elif self.turn == 2:
            self.turn = 1
        self.draw()

    def humanPlayer(self):
        print("Human's turn...")
        self.draw()
        done = False
        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    self.going = False
                    done = True
                    break
                elif e.type == pygame.MOUSEBUTTONDOWN:
                    self.chessboard.handle_key_event(e)
                    done = True
                    break
            if done:
                break
        if self.turn == 1:
            self.turn = 2
        elif self.turn == 2:
            self.turn = 1
        self.draw()

    def update(self):
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.going = False
            elif e.type == pygame.MOUSEBUTTONDOWN:
                self.chessboard.handle_key_event(e)

    def draw(self):
        self.screen.fill((255, 255, 255))
        # self.screen.blit(self.font.render("FPS: {0:.2F}".format(self.clock.get_fps()), True, (0, 0, 0)), (10, 10))

        self.chessboard.draw(self.screen, self.steps)
        if self.chessboard.game_over:
            self.screen.blit(self.font.render("{0} Won".format("Black" if self.chessboard.winner == 'b' else "White"), True, (0, 0, 0)), (500, 10))

        pygame.display.update()


if __name__ == '__main__':
    game = Gomoku()
    # game.humanPlayLoop()
    # game.agentHumanPlayLoop()
    # game.agentSelfPlayLoop(5)
    # game.agentSelfBetterPlayLoop(5)
    game.agentSelfDumbPlayLoop(5)