from collections import deque
from asynch import asyncdef, Signal
from typing import Generator, TYPE_CHECKING
if TYPE_CHECKING:
    from board import Board

from consts import EventTypes, Targets, Theatrics
import tkinter
import consts

SQUARE_SIZE = 76

PIECE_IMAGES = [""]
def loadImages():
    from PIL.Image import open
    from PIL.ImageTk import PhotoImage
    from pathlib import Path
    root = Path(__file__).parent.joinpath("assets").as_posix()
    PIECE_IMAGES.extend([
        PhotoImage(open(f"{root}//bP.png").resize((SQUARE_SIZE, SQUARE_SIZE))),
        PhotoImage(open(f"{root}//bN.png").resize((SQUARE_SIZE, SQUARE_SIZE))),
        PhotoImage(open(f"{root}//bB.png").resize((SQUARE_SIZE, SQUARE_SIZE))),
        PhotoImage(open(f"{root}//bR.png").resize((SQUARE_SIZE, SQUARE_SIZE))),
        PhotoImage(open(f"{root}//bQ.png").resize((SQUARE_SIZE, SQUARE_SIZE))),
        PhotoImage(open(f"{root}//bK.png").resize((SQUARE_SIZE, SQUARE_SIZE))),
        PhotoImage(open(f"{root}//wP.png").resize((SQUARE_SIZE, SQUARE_SIZE))),
        PhotoImage(open(f"{root}//wN.png").resize((SQUARE_SIZE, SQUARE_SIZE))),
        PhotoImage(open(f"{root}//wB.png").resize((SQUARE_SIZE, SQUARE_SIZE))),
        PhotoImage(open(f"{root}//wR.png").resize((SQUARE_SIZE, SQUARE_SIZE))),
        PhotoImage(open(f"{root}//wQ.png").resize((SQUARE_SIZE, SQUARE_SIZE))),
        PhotoImage(open(f"{root}//wK.png").resize((SQUARE_SIZE, SQUARE_SIZE))),
    ])


def createViewportOptions(
    width = 1200,
    height = 720
):
    """
    Provide the height and width of the viewport.

    Args:
        height (int): The desired height of the viewport.
        width (int): The desired width of the viewport.

    Returns:
        Options: The viewport options.
    """
    return {
        "width": width,
        "height": height
    }


class Event:
    def __init__(self, target = None, type = None, data = None):
        self.target: Targets = target
        self.type: EventTypes = type
        self.data: any = data


class ChezGui:
    def __init__(self,
        title = "Chezz ;)",
        viewportOptions = createViewportOptions(),
        board = None
    ):
        self.isexecing = False

        self.title = title
        self.viewportOptions = viewportOptions
        
        self.board: Board = board
        
        if board is None:
            raise Exception("Board is None boss")

        self._events = deque()
        self._provide_events_signal = Signal()

    def registerSquareClickEvent(self, squareLoc, tkSquare):
        tkSquare.bind("<Button-1>", lambda event: self.addEvent(Event(consts.Targets.Board, consts.EventTypes.click, squareLoc)))

    def addEvent(self, e):
        self._events.append(e)
        self._provide_events_signal.set()

    @asyncdef(name="GUI", main_delay=0.1)
    def exec(self):
        self.isexecing = True

        self.root = tkinter.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self._close)
        self.root.resizable(False, False)

        loadImages()
        
        self.root.title(self.title)
        self.root.geometry(f"{self.viewportOptions['width']}x{self.viewportOptions['height']}")

        self.container = tkinter.Frame(self.root, bg="#1e1e1e")
        self.container.place(relheight=1, relwidth=1, relx=0, rely=0)

        self.tkBoardContainer = tkinter.Frame(self.container, bg="#4f4f4f")
        self.tkBoardContainer.place(anchor=tkinter.W, width=SQUARE_SIZE*8, height=SQUARE_SIZE*8, x=(self.viewportOptions['height'] - (8 * SQUARE_SIZE)) // 2, rely=0.5)

        self.tkSquares = [
            tkinter.Label(self.tkBoardContainer, borderwidth=0, fg="#000000") for _ in range(64)
        ]

        self.updateBoard()
        self.updateTheatrics()

        for i, tkSquare in enumerate(self.tkSquares):
            tkSquare.place(width=SQUARE_SIZE, height=SQUARE_SIZE, x=(i % 8) * SQUARE_SIZE, y=(i//8) * SQUARE_SIZE)
            self.registerSquareClickEvent(i, tkSquare)


        self.root.mainloop()

    def _close(self):
        self.isexecing = False

        self._provide_events_signal.set()

        self.root.destroy()

    def updateBoard(self):
        for index, val in enumerate(self.board):
            self.tkSquares[index].configure(
                image=PIECE_IMAGES[val],
                # text=f"{index}"
            )

    def updateTheatrics(self):
        for index in range(64):
            self.tkSquares[index].configure(
                bg=\
                    ("#f0d9b5" if (index%2 if (index//8)%2 else not index%2) else "#b58863") if self.board.theatrics[index] == Theatrics.none else \
                    ("#cdd26a" if (index%2 if (index//8)%2 else not index%2) else "#aaa23a") if self.board.theatrics[index] == Theatrics.highlight else \
                    ("#829769" if (index%2 if (index//8)%2 else not index%2) else "#646f40") if self.board.theatrics[index] == Theatrics.target else \
                    ("#aeb187" if (index%2 if (index//8)%2 else not index%2) else "#84794e") if self.board.theatrics[index] == Theatrics.marked else \
                    "#000000", # unreachable
            )
            

    @property
    def events(self) -> Generator[Event, None, None]:
        while True:
            if not self.isexecing: return
            
            if self._events:
                yield self._events.popleft()
            else:
                self._provide_events_signal.clear() # if our deque is empty we just wait for a new event
                self._provide_events_signal.wait()                
                # some place in the code added an event to the deque
