import tkinter

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib as mpl
import matplotlib.pyplot as plt

import numpy as np

class Plotter:
    def __init__(self, x, y, label):
        self.x = x
        self.y = y
        self.label = label

class TkinterFigure:

    def draw(plotters):
        root = tkinter.Tk()
        root.wm_title("Embedding in Tk")
        
        """fig = Figure(figsize=(5, 4), dpi=100)
        t = np.arange(0, 3, .01)
        fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))"""
        
        
        fig = plt.figure(dpi=100)
        for plotter in plotters:
            plt.plot(plotter.x, plotter.y, 'o-', linewidth=1, markersize=3, label=plotter.label);
        plt.legend()
        plt.title('NABS01: EUR_HAB')
        plt.show()

        
        canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
        canvas.draw()
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
        
        toolbar = NavigationToolbar2Tk(canvas, root)
        toolbar.update()
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)
        
        
        def on_key_press(event):
            print("you pressed {}".format(event.key))
            key_press_handler(event, canvas, toolbar)
        
        
        canvas.mpl_connect("key_press_event", on_key_press)
        
        
        def _quit():
            root.quit()     # stops mainloop
            root.destroy()  # this is necessary on Windows to prevent
                            # Fatal Python Error: PyEval_RestoreThread: NULL tstate
        
        
        button = tkinter.Button(master=root, text="Quit", command=_quit)
        button.pack(side=tkinter.BOTTOM)
        
        tkinter.mainloop()
        # If you put root.destroy() here, it will cause an error if the window is
        # closed with the window manager.