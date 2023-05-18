'''
display module to graphically show configurations
'''

from tkinter import *


class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.master.title("Display")


def show_config(configuration):
    root = Tk()
    win = Window(root)
    root.geometry("140x140")

    canvas = Canvas(root, bg="white")
    canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
    canvas.create_rectangle(20, 20, 120, 120)

    for line in configuration.lines:
        start_x = (line.start.x * 100) + 20
        start_y = (line.start.y * 100) + 20
        end_x = (line.end.x * 100) + 20
        end_y = (line.end.y * 100) + 20
        canvas.create_line(start_x, start_y, end_x, end_y)

    canvas.pack()

    root.mainloop()
