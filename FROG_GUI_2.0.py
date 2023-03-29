import tkinter as tk
import tkinter.messagebox as msgbox
import numpy as np
from pyparsing import col
#import ThorLabsMotor
import timeit
from PIL import ImageTk, Image
import SpectrometerFrame
import MotorFrame
import FROGFrame


class FROGWindow(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.CreateCtrls()
    def CreateCtrls(self):
        self.FROGFrame = FROGFrame.FROGFrame(self)
        self.FROGFrame.grid(row=0,column=0)

    def kill_it(self):
        self.FROGFrame.shutdown()
        self.destroy()




if __name__ == "__main__":
    window = FROGWindow()
    window.geometry('1300x900')
    window.protocol('WM_DELETE_WINDOW', window.kill_it)
    window.mainloop()