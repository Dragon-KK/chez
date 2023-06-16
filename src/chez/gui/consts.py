from enum import IntEnum, auto

class Targets(IntEnum):
    Board = auto()

class EventTypes(IntEnum):
    click = auto()

class Theatrics(IntEnum):
    none = auto()
    highlight = auto() # highlights the square (to show previous move)
    marked = auto() # marks a square (to show valid moves)
    target = auto() # shows that the square was clicked
