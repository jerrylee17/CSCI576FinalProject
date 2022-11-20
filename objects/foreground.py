from typing import List


class Foreground:
    def __init__(self) -> None:
        # Is pixel part of foreground
        self.is_foreground: List[List[bool]] = []
        self.pixels: List[List[List[int]]] = []
