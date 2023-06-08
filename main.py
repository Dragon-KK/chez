from gui import ChezGui
from board import Board
from consts import BOARD, EventTypes
from logic import *

board = Board()

chez = ChezGui(
    board = board
)

init_logix(board)

chez.exec()

for event in chez.events:
    if event.target != BOARD:
        print("HANDLE THIS")
        continue
    
    if event.type != EventTypes.click:
        print("HANDLE THIS 2")
        continue

    needToUpdate = handle_click(event.data)
    if needToUpdate: chez.updateBoard()

