from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from chez.logic import Board

from functools import lru_cache
from .engine import Engine, CancellationToken
from .evaluators import naive_evaluate

INF = float("inf")

class PrunedMinimaxEngine(Engine):
    def get_static_evaluation(self, board: Board):
        return naive_evaluate(board)

    def evaluate(self, depth: int,  cancellation_token: CancellationToken):
        """Just get the best move to play in the given position"""  
        best_move = None
        if self.board.is_white_move:   
            best_eval = -INF
            for move in self.board.legal_moves:
                tmp_board = self.board.copy()
                tmp_board.make_move(move)
                tmp_board.compute_all_legal_moves()
                curr_eval = self.minimax(tmp_board, depth, -INF, INF, cancellation_token)
                if cancellation_token.cancelled:return
                if curr_eval > best_eval:
                    best_eval = curr_eval
                    best_move = move
        else:
            best_eval = INF
            for move in self.board.legal_moves:
                tmp_board = self.board.copy()
                tmp_board.make_move(move)
                tmp_board.compute_all_legal_moves()
                curr_eval = self.minimax(tmp_board, depth, -INF, INF, cancellation_token)
                if cancellation_token.cancelled:return
                if curr_eval < best_eval:
                    best_eval = curr_eval
                    best_move = move
        print(depth, best_move, best_eval)

    
    # @lru_cache(None)
    def minimax(self, curr_board: Board, depth: int, alpha: float, beta: float, cancellation_token: CancellationToken):
        """Refer to https://www.youtube.com/watch?v=l-hh51ncgDI&t=531s"""
        # TODO! FIX THIS SHIT
        if cancellation_token.cancelled:return
        if curr_board.is_checkmated():
            return -INF if curr_board.is_white_move else INF # If white was checkmated black is winning
        elif not curr_board.legal_moves:
            return 0 # Stalemate moment

        if depth == 0:
            return self.get_static_evaluation(curr_board)

        if curr_board.is_white_move: # We need to maximize white
            max_eval = -INF
            for move in curr_board.legal_moves:
                tmp_board = curr_board.copy()
                tmp_board.make_move(move)
                tmp_board.compute_all_legal_moves()
                
                # TODO! Investigate this, there is no back propogation of alpha beta
                eval = self.minimax(tmp_board, depth-1, alpha, beta, cancellation_token)
                if cancellation_token.cancelled:return
                max_eval = max(eval, max_eval)
                alpha = max(alpha, eval)
                if beta <= alpha: break
            return max_eval

        else: # Maximize black == Minimize white
            min_eval = INF
            for move in curr_board.legal_moves:
                tmp_board = curr_board.copy()
                tmp_board.make_move(move)
                tmp_board.compute_all_legal_moves()

                eval = self.minimax(tmp_board, depth-1, alpha, beta, cancellation_token)
                if cancellation_token.cancelled:return
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha: break
            return min_eval

