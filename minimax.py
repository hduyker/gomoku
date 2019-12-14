import random



class MINIMAX:
    def __init__(self, board):
        self.board = board

    def minimaxAgentWithPrunning(self, turn, depth, alpha=-float('inf'), beta=float('inf')):
        over, winner = self.board.isGameOver()
        if depth == 0 or over:
            score = self.board.evalBoard()
            return score, 0, 0

        result = None
        maxVal, minVal = -float('inf'), float('inf')

        legalMoves = self.board.genLegalMoves()
        # legalMoves = self.board.getCandidates(turn, 5)
        if len(legalMoves) == 0:
            self.board.game_over = True
            self.board.winner = 'd'
            return 0, -1, -1

        #random.shuffle(legalMoves) # test minimax vs minimax agents
        nextTurn, nextDepth = turn, depth
        if turn == 2:
            nextTurn, nextDepth = 1, depth
        elif turn == 1:
            nextTurn, nextDepth = 2, depth - 1

        for s, r, c in legalMoves:
            self.board.grid[r][c] = self.board.piece_turn[turn]
            res = self.minimaxAgentWithPrunning(nextTurn, nextDepth, alpha, beta)
            self.board.grid[r][c] = self.board.piece_turn[0]

            val = res[0]
            if turn == 2:
                alpha = max(alpha, val)
                if val > maxVal:
                    maxVal = val
                    result = (maxVal, r, c)
            elif turn == 1:
                beta = min(beta, val)
                if val < minVal:
                    minVal = val
                    result = (minVal, r, c)
            if beta <= alpha:
                break
        return result

    def minimaxAgentWithPrunningBlack(self, turn, depth, alpha=-float('inf'), beta=float('inf')):
        over, winner = self.board.isGameOver()
        if depth == 0 or over:
            score = self.board.evalBoard()
            return score, 0, 0

        result = None
        maxVal, minVal = -float('inf'), float('inf')

        legalMoves = self.board.genLegalMoves()
        # legalMoves = self.board.getCandidates(turn, 5)
        if len(legalMoves) == 0:
            self.board.game_over = True
            self.board.winner = 'd'
            return 0, -1, -1

        #random.shuffle(legalMoves) # test minimax vs minimax agents
        nextTurn, nextDepth = turn, depth
        if turn == 1:
            nextTurn, nextDepth = 2, depth
        elif turn == 2:
            nextTurn, nextDepth = 1, depth - 1

        for s, r, c in legalMoves:
            self.board.grid[r][c] = self.board.piece_turn[turn]
            res = self.minimaxAgentWithPrunningBlack(nextTurn, nextDepth, alpha, beta)
            self.board.grid[r][c] = self.board.piece_turn[0]

            val = res[0]
            if turn == 2:
                alpha = max(alpha, val)
                if val > maxVal:
                    maxVal = val
                    result = (maxVal, r, c)
            elif turn == 1:
                beta = min(beta, val)
                if val < minVal:
                    minVal = val
                    result = (minVal, r, c)
            if beta <= alpha:
                break
        return result