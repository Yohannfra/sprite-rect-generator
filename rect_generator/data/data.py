from dataclasses import dataclass

@dataclass
class Pixel:
    y: int
    x: int

@dataclass
class Rect:
    x1: int
    y1: int
    x2: int
    y2: int
