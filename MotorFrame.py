import tkinter as tk
import tkinter.messagebox as msgbox
import ThorLabsMotor

class MotorFrame(tk.Frame):
    def __init__(self,parent):
        tk.Frame.__init__(self,parent,highlightbackground='red',highlightthickness=2)
        
        #initialize the strings for user input
        self.step_size = tk.StringVar(self)
        self.delay_scan_width = tk.StringVar(self)
        self.jog_size = tk.StringVar(self)
        self.position = tk.StringVar(self)
        self.position.set('No position until motor connected')

        #name and serial numer for motor is needed
        #   maybe make it a user input later on?
        self.motor_name = tk.StringVar(self)
        self.serial_number = tk.StringVar(self)

        #Create Controls

        self.ControlFrame = tk.Frame(self,highlightbackground='black',highlightthickness=2)
        self.ControlFrame.grid(row=0,column=0)

        self.step_size_label = tk.Label(self.ControlFrame,text='Step size (fs)')
        self.step_size_label.grid(row=0,column=0)
        self.step_size_entry = tk.Entry(self.ControlFrame, textvariable=self.step_size)
        #bind it
        self.step_size_entry.grid(row=0,column=1)

        self.delay_scan_width_label = tk.Label(self.ControlFrame, text='Delay scan width')
        self.delay_scan_width_label.grid(row=1,column=0)
        self.delay_scan_width_entry = tk.Entry(self.ControlFrame, textvariable=self.delay_scan_width)
        
        self.delay_scan_width_entry.grid(row=1, column=1)

        self.jog_size_label = tk.Label(self.ControlFrame, text='Jog size')
        self.jog_size_label.grid(row=2,column=0)
        self.jog_size_entry = tk.Entry(self.ControlFrame, textvariable=self.jog_size)

        self.jog_size_entry.grid(row=2,column=1)

        self.position_label = tk.Label(self.ControlFrame, text='Position')
        self.position_label.grid(row=3,column=0)
        self.position_post = tk.Label(self.ControlFrame, text=self.position.get())
        self.position_post.grid(row=3,column=1)

        self.test_button = tk.Button(self.ControlFrame,text='test',command=self.test)
        self.test_button.grid(row=4,column=0)

    def test(self):
        self.position.set('nice')
        self.position_post.config(text=self.position.get())





