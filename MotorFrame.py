import tkinter as tk
import tkinter.messagebox as msgbox

class MotorFrame(tk.Frame):
    def __init__(self,parent):
        tk.Frame.__init__(self,parent,highlightbackground='red',highlightthickness=2)
        self.test_label = tk.Label(self,text='test')
        self.test_label.grid(row=0,column=0)