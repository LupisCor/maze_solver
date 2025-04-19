from tkinter import Tk, BOTH, Canvas


# Class to create window
class Window:
    def __init__(self, width, height):
        self._root = Tk() # Instantiate Tk as the root widget
        self._root.title("Maze Solver")
        self._canvas = Canvas(self._root, bg="white", height=height, width=width)
        self._canvas.pack(expand=1, fill=BOTH)
        self._running = False
        self._root.protocol("WM_DELETE_WINDOW", self.close)

    def redraw(self):
        self._root.update_idletasks()
        self._root.update()

    def wait_for_close(self):
        self._running = True
        while self._running:
            self.redraw()
        print("Window Closed")
    
    def draw_line(self, line, fill_color="black"):
        line.draw(self._canvas, fill_color)

    def close(self):
        self._running = False


# Class to create points 
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


# Class to draw lines
class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
    
    def draw(self, canvas, fill_color="black"):
        canvas.create_line(self.p1.x, self.p1.y, # x,y value of point 1
                           self.p2.x, self.p2.y, # x,y value of point 2
                           fill=fill_color, width=2)