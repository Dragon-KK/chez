from abc import abstractclassmethod
from chez.general.asynch import Signal
from chez.logic import Board
from multiprocessing import Process

def run_start(obj):
    obj._start()

class CancellationToken:
    def __init__(self):
        self.cancelled = False
        """Set to true if the operation is to be cancelled"""

class Engine:
    def __init__(self):
        self.board = Board()
        """The root board from which evaluations are to be made"""

        self.is_running = False
        """Set to true while the engine is running"""
        
        self.cancellation_token = None
        """The cancellation token for the current active evaluation"""

        self.begin_evaluation_signal = Signal()
        """Signal to begin evaluation when idle"""
        
        self.depth = 0
        """Depth of evaluation (increases by one after every succesive evaluation)"""

    def abort(self):
        """Aborts the current evaluation and resets the depth counter"""
        if self.cancellation_token is not None:
            self.cancellation_token.cancelled = True
            self.cancellation_token = None

        self.depth = 0

    def update_board(self, board: Board):
        """Updates the root board"""
        self.board = board.copy()

    def begin_evaluation(self):
        """Begins the evaluation from the root board and current depth"""
        self.cancellation_token = CancellationToken()
        self.begin_evaluation_signal.set()

    def _start(self):
        print(1231)
        return
        self.is_running = True

        while self.is_running:
            if self.cancellation_token is not None:
                self.depth += 1
                self.evaluate(self.depth, self.cancellation_token)
            else:
                self.begin_evaluation_signal.clear()
                self.begin_evaluation_signal.wait()
    
    def start(self):
        """Starts the engine"""
        Process(target=run_start, name="Engine", args=(self,), daemon=True).start()
        

    @abstractclassmethod
    def evaluate(self, depth: int,  cancellation_token: CancellationToken):
        """
        Evaluates the given board
        NOTE: When the board is updated the cancellation_token is expected to be cancelled)
        NOTE: The depth is incremented automatically whenever an evaluation finishes
        """
