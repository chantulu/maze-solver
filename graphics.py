from tkinter import Tk, BOTH, Canvas


class Window:
    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height
        self.__root = Tk()
        self.__root.title = "Maze Solver"
        self.canvas = Canvas(self.__root, bg="white", height=height, width=width)
        self.canvas.pack(fill=BOTH, expand=1)
        self.__running = False
        self.__root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self) -> None:
        self.__root.update_idletasks()
        self.__root.update()

    def wait_for_close(self) -> None:
        self.__running = True
        while self.__running:
            self.redraw()
        print("window closed...")

    def close(self) -> None:
        self.__running = False

    def draw_line(self, line, fill="black"):
        line.draw(self.canvas, fill)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x},{self.y})"

    def __repr__(self):
        return f"({self.x},{self.y})"


class Line:
    def __init__(self, p1, p2) -> None:
        self.p1 = p1
        self.p2 = p2

    def draw(self, canvas, fill):
        canvas.create_line(
            self.p1.x, self.p1.y, self.p2.x, self.p2.y, fill=fill, width=2
        )
