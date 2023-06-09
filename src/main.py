from gui import ChezGui
from board import Board
from consts import Targets, EventTypes
from logic import *

board = Board()

chez = ChezGui(
    board = board
)

init_logix(board)

chez.exec()

for event in chez.events:
    if event.target != Targets.Board:
        print("HANDLE THIS")
        continue
    
    if event.type != EventTypes.click:
        print("HANDLE THIS 2")
        continue

    needToUpdatePieces, needToUpdateTheatrics = handle_click(event.data)
    if needToUpdateTheatrics: chez.updateTheatrics()
    if needToUpdatePieces: chez.updateBoard()
