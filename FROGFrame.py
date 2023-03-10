import tkinter as tk
import tkinter.messagebox as msgbox
from tkinter.simpledialog import askstring
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
import time

class FROGFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self,parent, highlightbackground='green', highlightthickness=2)
        #initial variables
        self.FROG_measurement = False
        self.dark_measurement = False

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
        self.test_button = tk.Button(self.FROG_subframe, text='save FROG', command=self.saveFROG)
        self.test_button.grid(row=1,column=1)

    def FROG(self):
        if self.MotorFrame.step_size.get() == '' or self.MotorFrame.delay_scan_width.get() == '':
            msgbox.showerror('nice try','set up a delay scan width and step size')  
        elif self.MotorFrame.motor == None or self.SpecFrame.spec == None:
            msgbox.showerror('yikes','make sure a motor and spectrometer are connected')
        else:
            counter = 0
            self.step_size = float(self.MotorFrame.step_size.get())
            self.scan_width = float(self.MotorFrame.delay_scan_width.get())
            #what if they are not multiples of one another
            self.wavelengths = self.SpecFrame.spec.get_wavelengths()
            self.steps = int(self.scan_width / self.step_size)
            print('number of steps', 2*self.steps + 1)
            self.FROG_matrix = np.zeros((len(self.SpecFrame.spec.get_wavelengths()), 2*self.steps + 1)) #initialize matrix for data storage
            self.im = self.FROG_plot.imshow(self.FROG_matrix)
            self.MotorFrame.move_to_save() #go to time 0
            self.MotorFrame.motor.move_relative(-self.scan_width) #go to the very back of the scan to start
            while counter < 2*self.steps + 1:
                self.FROG_plot.clear() #clear previous plot from memory
                self.FROG_matrix[:, counter] = self.SpecFrame.spec.get_intensities() #entire new column of intensity data
                time.sleep(int(self.SpecFrame.integration_var.get())*(10**-3)) 
                #time.sleep(2)
                #wait to ensure our net time step will grab a different integration from spectrometer
                
                #remake from graph with new data
                #self.im.set_data(self.FROG_matrix)
                #self.im.autoscale()
                #self.FROG_canvas.draw()
                self.im = self.FROG_plot.imshow(self.FROG_matrix, aspect='auto',extent=[-self.scan_width,self.scan_width, self.wavelengths[-1], self.wavelengths[0]])
                self.FROG_canvas.draw()
                self.FROG_subframe.update()
                self.MotorFrame.motor.move_relative(self.step_size) #move to next step
                self.MotorFrame.refresh_position()
                counter +=1
                if counter == 2*self.steps - 1:
                    print(self.SpecFrame.spec.get_intensities())
                print(counter)
            self.MotorFrame.motor.move_relative(-self.step_size) #go back one step
            self.MotorFrame.refresh_position()
            self.FROG_plot.set_ylabel('Wavelength (nm)')
            self.FROG_plot.set_xlabel('Delay (fs)')
            self.FROG_measurement = True
            print('FROG done')

    def darkFrame(self):
        print('nice')

    def saveFROG(self):
        if not self.FROG_measurement:
            msgbox.showerror('yikes','no FROG scan has been taken yet')
        else:
            file_name = askstring('File name', 'Name the file please')
            file_name += '.txt'
            f = open('FROG_DATA/' + file_name,'w')
            #number of delay points
            f.write(str(self.steps*2 + 1) + '\n')
            #number of wavelength points
            f.write(str(len(self.wavelengths)) + '\n')
            #Delay Step size
            f.write(str(self.step_size) + '\n')
            #Wavelength step size
            wave_range = self.wavelengths[-1] - self.wavelengths[0]
            wave_step = wave_range / len(self.wavelengths)
            f.write(str(wave_step) + '\n')
            #wavelength center pixel
            center_wave = self.wavelengths[int(len(self.wavelengths) / 2)]
            f.write(str(center_wave) + '\n')
            #actual FROG data
            f.close()
            f = open('FROG_DATA/' + file_name, 'a')
            np.savetxt(f,self.FROG_matrix)
            f.close()

    def shutdown(self):
        self.SpecFrame.shutdown()
        self.MotorFrame.disconnect_motor()