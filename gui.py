import tkinter as tk
from tkinter import ttk
import sample
import _thread


class SpaceGUI:

    def draw_node(self, x, y, size, color):
        return self.canvas.create_oval(x - size, y - size, x + size, y + size,
                                       fill=color)

    def draw_nodes(self, size):
        node1 = self.draw_node(self.width/2, self.height/4, size, 'blue')
        node2 = self.draw_node(self.width/6, 5 * self.height/6, size, 'blue')
        node3 = self.draw_node(5 * self.width/6, 5 * self.height/6, size,
                               'blue')
        return [node1, node2, node3]

    def draw_canvas(self, items):
        for item in items:
            self.canvas.delete(item)
        sound_objs = self.bs.get_sound_objs()
        for obj in sound_objs:
            n1 = self.draw_node(obj.x, obj.y, obj.size, obj.color)
            items.append(n1)
        self.root.after(10, self.draw_canvas, items)

    def run(self):
        self.mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.rowconfigure(0, weight=1)

        self.draw_nodes(10)
        self.draw_canvas([])

        for child in self.mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        self.root.mainloop()

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Space Sound System")
        self.mainframe = ttk.Frame(self.root)
        self.width = 600
        self.height = 600
        self.canvas = tk.Canvas(self.mainframe, width=self.width,
                                height=self.height)
        self.bs = sample.BufferServer()
        _thread.start_new_thread(self.bs.start, ())


def main():
    gui = SpaceGUI()
    gui.run()

if __name__ == '__main__':
    main()
