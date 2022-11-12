class Pixel:
    def __init__(self) -> None:
        """
        type: rgb / hsv in lowercase
        val: rgb / hsv values
        """
        self.type: str
        self.val: tuple[int, int, int]