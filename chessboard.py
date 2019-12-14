import pygame
import random
from enum import Enum
from copy import deepcopy
import collections

class Pattern(Enum):
    CHECKED = -1
    UNCHECKED = 0
    FIVE = 1
    OPEN_FOUR = 2
    HALF_FOUR = 3
    OPEN_THREE = 4
    HALF_THREE = 5
    OPEN_TWO = 6
    HALF_TWO = 7

class Chessboard:

    def __init__(self, grid, piece, preMove):
        self.grid_size = 26
        self.start_x, self.start_y = 30, 50
        self.edge_size = self.grid_size / 2
        self.grid_count = len(grid)
        self.piece = piece
        self.winner = None
        self.game_over = False
        self.piece_turn = ['.', 'b', 'w']

        self.pattern_value = {Pattern.FIVE.value: 6000, Pattern.OPEN_FOUR.value: 4800, Pattern.HALF_FOUR.value: 500,
                  Pattern.OPEN_THREE.value: 500, Pattern.HALF_THREE.value: 200, Pattern.OPEN_TWO.value: 50,
                  Pattern.HALF_TWO.value: 10}

        self.preMove = preMove
        self.grid = grid

        self.pattern_count = []
        for i in range(self.grid_count):
            self.pattern_count.append([])
            for j in range(self.grid_count):
                self.pattern_count[i].append([Pattern.UNCHECKED.value] * 4)

        self.preWeight = []
        for i in range(self.grid_count):
            self.preWeight.append([0] * self.grid_count)
        w = 1
        for i in range(1, self.grid_count // 2 + 1):
            for j in range(i, self.grid_count - i):
                self.preWeight[i][j] = w
                self.preWeight[j][i] = w
                self.preWeight[self.grid_count - i - 1][j] = w
                self.preWeight[j][self.grid_count - i - 1] = w
            w += 1
        self.preWeight[self.grid_count // 2][self.grid_count // 2] = self.preWeight[self.grid_count // 2][self.grid_count // 2 + 1]
        # print(self.preWeight)

    def reset_pattern_count(self):
        for i in range(self.grid_count):
            for j in range(self.grid_count):
                self.pattern_count[i][j] = [Pattern.UNCHECKED.value] * 4

    def reset(self):
        self.piece = 'b'
        self.winner = None
        self.game_over = False
        self.grid = []
        for i in range(self.grid_count):
            self.grid.append(list("." * self.grid_count))

    def genLegalMoves(self):
        moves = []
        for i in range(self.grid_count):
            for j in range(self.grid_count):
                if self.grid[i][j] == '.':
                    moves.append((self.preWeight[i][j], i, j))
        moves.sort(reverse=True)
        return moves


    def handle_key_event(self, e):
        origin_x = self.start_x - self.edge_size
        origin_y = self.start_y - self.edge_size
        size = (self.grid_count - 1) * self.grid_size + self.edge_size * 2
        pos = e.pos
        if origin_x <= pos[0] <= origin_x + size and origin_y <= pos[1] <= origin_y + size:
            if not self.game_over:
                x = pos[0] - origin_x
                y = pos[1] - origin_y
                r = int(y // self.grid_size)
                c = int(x // self.grid_size)
                if self.set_piece(r, c):
                    print("({},{})".format(r, c))
                    self.check_win(r, c)
                    # result = self.evalBoard()
                    # print("result = {}".format(result))

    def set_piece(self, r, c):
        if self.grid[r][c] == '.':
            self.grid[r][c] = self.piece
            if self.piece == 'b':
                self.piece = 'w'
            else:
                self.piece = 'b'
            return True
        return False

    def update(self, r, c, piece):
        newGrid = deepcopy(self.grid)
        preMove = (r, c)
        if newGrid[r][c] == '.':
            newGrid[r][c] = piece
            if piece == 'b':
                piece = 'w'
            else:
                piece = 'b'
            return Chessboard(newGrid, piece, preMove)
        else:
            raise ValueError("move is invalid!")

    def isGameOver(self):
        cnt = 0
        for r in range(self.grid_count):
            for c in range(self.grid_count):
                piece = self.grid[r][c]
                if piece != '.':
                    cnt += 1
                    if self._check(r, c):
                        return (True, piece)
        if cnt == (self.grid_count * self.grid_count):
            return (True, None)
        return (False, None)

    def check_win(self, r, c):
        if self._check(r, c):
            self.winner = self.grid[r][c]
            self.game_over = True

    def _check(self, r, c):
        n_count = self.get_continuous_count(r, c, -1, 0)
        s_count = self.get_continuous_count(r, c, 1, 0)

        e_count = self.get_continuous_count(r, c, 0, 1)
        w_count = self.get_continuous_count(r, c, 0, -1)

        se_count = self.get_continuous_count(r, c, 1, 1)
        nw_count = self.get_continuous_count(r, c, -1, -1)

        ne_count = self.get_continuous_count(r, c, -1, 1)
        sw_count = self.get_continuous_count(r, c, 1, -1)

        if (n_count + s_count + 1 >= 5) or (e_count + w_count + 1 >= 5) or \
                (se_count + nw_count + 1 >= 5) or (ne_count + sw_count + 1 >= 5):
            return True
        return False

    def get_continuous_count(self, r, c, dr, dc):
        piece = self.grid[r][c]
        result = 0
        i = 1
        while True:
            new_r = r + dr * i
            new_c = c + dc * i
            if 0 <= new_r < self.grid_count and 0 <= new_c < self.grid_count:
                if self.grid[new_r][new_c] == piece:
                    result += 1
                else:
                    break
            else:
                break
            i += 1
        return result

    def draw(self, screen, step):
        pygame.draw.rect(screen, (185, 122, 87),
                         [self.start_x - self.edge_size, self.start_y - self.edge_size,
                          (self.grid_count - 1) * self.grid_size + self.edge_size * 2, (self.grid_count - 1) * self.grid_size + self.edge_size * 2], 0)

        for r in range(self.grid_count):
            y = self.start_y + r * self.grid_size
            pygame.draw.line(screen, (0, 0, 0), [self.start_x, y], [self.start_x + self.grid_size * (self.grid_count - 1), y], 2)

        for c in range(self.grid_count):
            x = self.start_x + c * self.grid_size
            pygame.draw.line(screen, (0, 0, 0), [x, self.start_y], [x, self.start_y + self.grid_size * (self.grid_count - 1)], 2)

        for r in range(self.grid_count):
            for c in range(self.grid_count):
                piece = self.grid[r][c]
                if piece != '.':
                    if piece == 'b':
                        color = (0, 0, 0)
                    else:
                        color = (255, 255, 255)

                    x = self.start_x + c * self.grid_size
                    y = self.start_y + r * self.grid_size
                    pygame.draw.circle(screen, color, [x, y], self.grid_size // 2)

    def getCandidates(self, turn, N=1):
        legalMoves = self.genLegalMoves()
        candidates, shortList = [], []
        for s, r, c in legalMoves:
            self.grid[r][c] = self.piece_turn[turn]
            score = self.evalBoard()
            candidates.append((score, r, c))
            self.grid[r][c] = self.piece_turn[0]
        candidates.sort(reverse=True)
        M = min(len(candidates), N)
        if turn == 2:
            shortList = candidates[0:M]
        elif turn == 1:
            shortList = candidates[-M:]
        return shortList

    def greedyAgent(self, turn, N=1):
        shortList = self.getCandidates(turn, N)
        result = random.choice(shortList)
        return result

    def genRandomMove(self):
        # if self.grid[self.grid_count // 2][self.grid_count // 2] == '.':
        #     return self.grid_count // 2, self.grid_count // 2
        return random.choice(self.genLegalMoves())

    def evalBoard(self):
        self.reset_pattern_count()
        for r in range(self.grid_count):
            for c in range(self.grid_count):
                if self.grid[r][c] != '.':
                    if self.pattern_count[r][c][0] == Pattern.UNCHECKED.value:
                        self.checkRow(r, c)
                    if self.pattern_count[r][c][1] == Pattern.UNCHECKED.value:
                        self.checkCol(r, c)
                    if self.pattern_count[r][c][2] == Pattern.UNCHECKED.value:
                        self.checkLeftDiag(r, c)
                    if self.pattern_count[r][c][3] == Pattern.UNCHECKED.value:
                        self.checkRightDiag(r, c)
        count = {}
        count['b'] = collections.defaultdict(int)
        count['w'] = collections.defaultdict(int)

        for r in range(self.grid_count):
            for c in range(self.grid_count):
                if self.grid[r][c] != '.':
                    for i in range(4):
                        if self.pattern_count[r][c][i] in self.pattern_value:
                            count[self.grid[r][c]][self.pattern_count[r][c][i]] += 1

        whiteScore, blackScore = 0, 0
        for x in count['w']:
            whiteScore += self.pattern_value[x] * count['w'][x]
        for x in count['b']:
            blackScore += self.pattern_value[x] * count['b'][x]
        for r in range(self.grid_count):
            for c in range(self.grid_count):
                if self.grid[r][c] == 'w':
                    whiteScore += self.preWeight[r][c]
                elif self.grid[r][c] == 'b':
                    blackScore += self.preWeight[r][c]
        score = whiteScore - blackScore
        return score

    def checkRow(self, r, c):
        line = []
        for i in range(self.grid_count):
            line.append(self.grid[r][i])

        # print("checkRow: r = {}, c = {}, line = {}".format(r, c, line))

        result = self.checkLine(line, self.grid_count, c)

        # print("checkRow: r = {}, c = {}, result = {}".format(r, c, result))

        for i in range(self.grid_count):
            if result[i] != Pattern.UNCHECKED.value:
                self.pattern_count[r][i][0] = result[i]

        # print("checkRow: self.pattern_count = {}".format(self.pattern_count))

    def checkCol(self, r, c):
        line = []
        for i in range(self.grid_count):
            line.append(self.grid[i][c])
        result = self.checkLine(line, self.grid_count, r)

        # print("checkCol: r = {}, c = {}, result = {}".format(r, c, result))

        for i in range(self.grid_count):
            if result[i] != Pattern.UNCHECKED.value:
                self.pattern_count[i][c][1] = result[i]

    def checkLeftDiag(self, r, c):
        line = []
        if r + c < self.grid_count:
            r0, c0 = r + c, 0
            length, pos = r + c + 1, c - c0
        else:
            r0, c0 = self.grid_count - 1, r + c - (self.grid_count - 1)
            length, pos = (self.grid_count - 1) - c0 + 1, c - c0
        for i in range(length):
            line.append(self.grid[r0 - i][c0 + i])
        result = self.checkLine(line, length, pos)

        # print("checkLeftDiag: r = {}, c = {}, result = {}".format(r, c, result))

        for i in range(length):
            if result[i] != Pattern.UNCHECKED.value:
                self.pattern_count[r0 - i][c0 + i][2] = result[i]

    def checkRightDiag(self, r, c):
        line = []
        if r <= c:
            r0, c0 = 0, c - r
            length, pos = self.grid_count - c0, r
        else:
            r0, c0 = r - c, 0
            length, pos = self.grid_count - r0, c
        for i in range(length):
            line.append(self.grid[r0 + i][c0 + i])
        result = self.checkLine(line, length, pos)

        # print("checkRightDiag: r = {}, c = {}, result = {}".format(r, c, result))

        for i in range(length):
            if result[i] != Pattern.UNCHECKED.value:
                self.pattern_count[r0 + i][c0 + i][3] = result[i]

    def checkLine(self, line, length, pos):
        result = [0 for i in range(length)]
        if length < 5:
            for i in range(length):
                result[i] = Pattern.CHECKED.value
            return result

        left, right, start, end = pos, pos, pos, pos
        piece = line[pos]
        pieceOpponent = 'b' if piece == 'w' else 'w'

        while start > 0:
            if line[start - 1] == piece:
                start -= 1
            else:
                break
        left = start
        while left > 0:
            if line[left - 1] == pieceOpponent:
                break
            else:
                left -= 1

        while end < length - 1:
            if line[end + 1] == piece:
                end += 1
            else:
                break
        right = end
        while right < length - 1:
            if line[right + 1] == pieceOpponent:
                break
            else:
                right += 1

        piecePotential = right - left + 1
        if piecePotential < 5:  # dead pattern
            for i in range(left, right + 1):
                result[i] = Pattern.CHECKED.value
            return result

        # mark the same pieces as checked
        for i in range(start, end + 1):
            result[i] = Pattern.CHECKED.value

        pieceRange = end - start + 1

        # print("checkLine: piecePotential = {}, pieceRange = {}, left = {}, right = {}, start = {}, end = {}, Pattern.OPEN_TWO.value = {}".format(piecePotential, pieceRange, left, right, start, end, Pattern.OPEN_TWO.value))

        # five in a row
        if pieceRange >= 5:
            result[pos] = Pattern.FIVE.value
            return result
        # four in a row
        if pieceRange == 4:
            if left < start and right > end:
                result[pos] = Pattern.OPEN_FOUR.value
            else:
                result[pos] = Pattern.HALF_FOUR.value
            return result
        # three in a row
        if pieceRange == 3:
            if left < start and right > end:
                result[pos] = Pattern.OPEN_THREE.value
            else:
                result[pos] = Pattern.HALF_THREE.value
            return result
        # two in a row
        if pieceRange == 2:
            if left < start and right > end:
                result[pos] = Pattern.OPEN_TWO.value
            else:
                result[pos] = Pattern.HALF_TWO.value
            return result

        return result