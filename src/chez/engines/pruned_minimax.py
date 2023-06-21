from functools import lru_cache
from .engine import Engine, CancellationToken

class PrunedMinimaxEngine(Engine):
    def __init__(self):
        super.__init__(self)

    @lru_cache(None)
    def minimax(self, curr_board, depth, alpha, beta, maximising_player_is_white):
        if depth == 0:
            return self.evaluate(depth=0, self.cancellation_token)
        # how do i return static evaluation of curr_board??????
        curr_board.compute_all_legal_moves()
        if len(curr_board.legal_moves) == 0:
            return self.evaluate(depth=depth, self.cancellation_token)
        if curr_board.is_white_move == maximising_player_is_white:
            max_eval = float('-inf')
            for start, end, idk in curr_board.legal_moves:
                eval = self.minimax(curr_board._temporary_move(start, end),
                                    depth-1,
                                    alpha,
                                    beta,
                                    not maximising_player_is_white
                                    )
                max_eval = max(eval, max_eval)
                alpha = max(alpha, eval)
                if beta <= alpha: break
            return max_eval

        else:
            min_eval = float('inf')
            for start, end, idk in curr_board.legal_moves:
                eval = self.minimax(curr_board._temporary_move(start, end),
                                    depth-1,
                                    alpha,
                                    beta,
                                    not maximising_player_is_white
                                    )
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha: break
            return min_eval

