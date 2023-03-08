import tkinter as tk
import tkinter.messagebox as msgbox
from matplotlib import image
import numpy as np
import matplotlib
from pyparsing import col
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
import MotorFrame
import SpectrometerFrame

class FROGFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self,parent, highlightbackground='green', highlightthickness=2)
        #other classes I implemented
        self.SpecFrame = SpectrometerFrame.SpectrometerFrame(self)
        self.SpecFrame.grid(row=0,column=0)
        self.MotorFrame = MotorFrame.MotorFrame(self)
        self.MotorFrame.grid(row=1,column=1)

        #FROG figure
        self.FROG_subframe = tk.Frame(self,highlightbackground='black', highlightthickness=2)
        self.FROG_subframe.grid(row=0,column=1)
        self.FROG_figure = plt.figure(figsize=(5,5))
        self.FROG_plot = self.FROG_figure.add_subplot()
        self.FROG_plot.set_xlabel('Time (fs)')
        self.FROG_plot.set_ylabel('Wavelengths (nm)')
        self.FROG_plot.set_title('FROG Reading')        
        self.FROG_plot.grid(True)

        self.FROG_canvas = FigureCanvasTkAgg(self.FROG_figure, self.FROG_subframe)
        self.FROG_canvas.draw()
        self.FROG_canvas.get_tk_widget().grid(row=0,column=0,columnspan=2)

        self.FROG_button = tk.Button(self.FROG_subframe, text='FROG', command=self.FROG)
        self.FROG_button.grid(row=1,column=0)
        self.test_button = tk.Button(self.FROG_subframe, text='test')
        self.test_button.grid(row=1,column=1)

    def FROG(self):
        if self.MotorFrame.step_size.get() == '' or self.MotorFrame.delay_scan_width.get() == '':
            msgbox.showerror('nice try','set up a delay scan width and step size')  
        elif self.MotorFrame.motor == None or self.SpecFrame.spec == None:
            msgbox.showerror('yikes','make sure a motor and spectrometer are connected')
        else:
            counter = 0
            step_size = float(self.MotorFrame.step_size.get())
            scan_width = float(self.MotorFrame.delay_scan_width.get())
            steps = int(scan_width / step_size)
            self.FROG_matrix = np.zeros((len(self.SpecFrame.spec.get_wavelengths()), 2*steps + 1)) #initialize matrix for data storage
            self.im = self.FROG_plot.imshow(self.FROG_matrix)
            self.MotorFrame.move_to_save() #go to time 0
            self.MotorFrame.motor.move_relative(-scan_width) #go to the very back of the scan to start
            while counter < 2*steps + 1:
                self.FROG_plot.clear() #clear previous plot from memory
                self.FROG_matrix[:, counter] = self.SpecFrame.spec.get_intensities() #entire new column of intensity data
                self.im.set_data(self.FROG_matrix)
                self.im.autoscale()
                self.FROG_canvas.draw()
                self.MotorFrame.motor.move_relative(step_size) #move to next step
                counter +=1
                print(counter)
            self.MotorFrame.motor.move_relative(-step_size) #go back one step
            print('FROG done')




    def shutdown(self):
        self.SpecFrame.shutdown()
        self.MotorFrame.disconnect_motor()