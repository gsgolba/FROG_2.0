import tkinter as tk
import tkinter.messagebox as msgbox
import numpy as np
from pyparsing import col
#import ThorLabsMotor
import timeit
from PIL import ImageTk, Image
import SpectrometerFrame
import MotorFrame

class FROGWindow(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.CreateCtrls()
    def CreateCtrls(self):
        #Spectrometer
        self.SpecFrame = SpectrometerFrame.SpectrometerFrame(self)
        self.SpecFrame.grid(row=0,column=0)
        self.MotorFrame = MotorFrame.MotorFrame(self)
        self.MotorFrame.grid(row=0,column=1)

    def kill_it(self):
        self.destroy()
        self.SpecFrame.shutdown()




if __name__ == "__main__":
    window = FROGWindow()
    window.protocol('WM_DELETE_WINDOW', window.kill_it)
    window.mainloop()