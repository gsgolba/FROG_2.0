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
import spectrometer
import time

class SpectrometerFrame(tk.Frame):
    def __init__(self,parent):
        tk.Frame.__init__(self,parent,highlightbackground='orange',highlightthickness=2)

        #initiialize the strings for user input
        self.spec = None
        self.min_wave_var = tk.StringVar(self)
        self.max_wave_var = tk.StringVar(self)
        self.max_intense_var = tk.StringVar(self)
        self.min_intense_var = tk.StringVar(self)
        self.integration_var = tk.StringVar(self)
        self.spectral_cancel_id = None

        #figure
        self.spectral_figure = plt.figure(figsize=(5,5))
        self.I_vs_wave = self.spectral_figure.add_subplot()
        self.I_vs_wave.set_xlabel('Wavelength (nm)')
        self.I_vs_wave.set_ylabel('Intensity (a.u.)')
        self.I_vs_wave.grid(True)

        self.spectral_canvas = FigureCanvasTkAgg(self.spectral_figure, self)
        self.spectral_canvas.draw()
        self.spectral_canvas.get_tk_widget().grid(row=0,column=0)

        #Create Controls

        self.ControlFrame = tk.Frame(self,highlightbackground='blue', highlightthickness=2)
        self.ControlFrame.grid(row=1, column=0)

        self.connect_spectrometer = tk.Button(self.ControlFrame, text='Connect Virtual Spectrometer', command=self.connect_virtual)
        self.connect_spectrometer.grid(row=0,column=0)
        self.connect_spectrometer_= tk.Button(self.ControlFrame, text='Connect Real Spectrometer', command=self.connect_real)
        self.connect_spectrometer_.grid(row=0,column=1)
        self.disconnect_spectrometer = tk.Button(self.ControlFrame, text = 'Disconnect (either) Spectrometer', command=self.disconnect)
        self.disconnect_spectrometer.grid(row=0,column=2)

        self.min_wave_entry = tk.Entry(self.ControlFrame, textvariable=self.min_wave_var)
        self.min_wave_entry.bind('<Return>', self.set_min_wave)
        self.min_wave_entry.grid(column=1,row=1)
        self.min_wave_label = tk.Label(self.ControlFrame, text='Wavelength min (nm)')
        self.min_wave_label.grid(column=0,row=1)

        self.max_wave_entry = tk.Entry(self.ControlFrame, textvariable=self.max_wave_var)
        self.max_wave_entry.bind('<Return>', self.set_max_wave)
        self.max_wave_entry.grid(column=1,row=2)
        self.max_wave_label = tk.Label(self.ControlFrame, text='Wavelength max (nm)')
        self.max_wave_label.grid(column=0,row=2)

        self.min_intens_entry = tk.Entry(self.ControlFrame, textvariable=self.min_intense_var)
        self.min_intens_entry.bind('<Return>', self.set_min_intens)
        self.min_intens_entry.grid(column=1,row=3)
        self.min_intens_label = tk.Label(self.ControlFrame, text='Intensity min (a.u.)')
        self.min_intens_label.grid(column=0,row=3)
    
        self.max_intens_entry = tk.Entry(self.ControlFrame, textvariable=self.max_intense_var)
        self.max_intens_entry.bind('<Return>', self.set_max_intens)
        self.max_intens_entry.grid(column=1,row=4)
        self.max_intens_label = tk.Label(self.ControlFrame, text='Intensity max (a.u.)')
        self.max_intens_label.grid(column=0,row=4)

        self.integration_entry = tk.Entry(self.ControlFrame, textvariable=self.integration_var)
        self.integration_entry.bind('<Return>', self.set_integration_length)
        self.integration_entry.grid(column=1,row=5)
        self.integration_label = tk.Label(self.ControlFrame, text='Integration time (ms)')
        self.integration_label.grid(column=0,row=5)

        self.graph_button = tk.Button(self.ControlFrame, text='Graph Spectrum!', command=self.graph_spectrum)
        self.graph_button.grid(row=6,column=0)
        self.stop_button = tk.Button(self.ControlFrame,text='Stop Graphing', command=self.stop_graphing)
        self.stop_button.grid(row=6,column=1)

        #self.spec_run_button = tk.Button(self.ControlFrame, text='Run Spec', command=self.spectral_reading)
        #self.spec_run_button.grid(column=0,row=6)
        #self.spec_stop_run_button = tk.Button(self.ControlFrame, text='Stop Run', command=self.stop_spectral_reading)
        #self.spec_stop_run_button.grid(column=1,row=6)
        
    def connect_virtual(self):
        try:
            self.spec = spectrometer.Virtual_Spectrometer()
            print(self.spec)
        except:
            msgbox.showerror('Yikes', 'Could not connect virtual spectrometer')
    def connect_real(self):
        try:
            self.spec = spectrometer.Spectrometer()
            print(self.spec)
        except:
            msgbox.showerror('Yikes', 'Could not connect real spectrometer')
    def disconnect(self):
        if self.spec != None:
            self.spec.destroy()
            self.spec = None
        else:
            msgbox.showerror('Yikes', 'No spectormeter to disconnect')
    def set_min_wave(self,event): #find old bounds, and update them accordingly
        left, right = self.I_vs_wave.get_xlim()
        min_ = int(self.min_wave_var.get())
        self.I_vs_wave.set_xlim([min_,right])
        self.spectral_canvas.draw()
    def set_max_wave(self,event):
        left, right = self.I_vs_wave.get_xlim()
        max_ = int(self.max_wave_var.get())
        self.I_vs_wave.set_xlim([left,max_])
        self.spectral_canvas.draw()
    def set_max_intens(self,event):
        down,up = self.I_vs_wave.get_ylim()
        self.I_vs_wave.set_ylim([down,int(self.max_intense_var.get())])
        self.spectral_canvas.draw()
    def set_min_intens(self,event):
        down,up = self.I_vs_wave.get_ylim()
        self.I_vs_wave.set_ylim([int(self.min_intense_var.get()), up])
        self.spectral_canvas.draw()
    def set_integration_length(self,event):
        if self.spec != None:
            self.spec.change_integration_time(self.integration_entry.get())
            #and need backgorund subtraction?
        else:
            msgbox.showerror('Yikes', 'No spectrometer connected to change integration length')
    def graph_spectrum(self):
        if self.spec != None:
            #clear previous frame, 
            #   otherwise it'll be behind the next plot 
            #   and take up lots memory
            self.I_vs_wave.clear()
            wavelengths, intensities = self.spec.get_both() #maybe don't use local variable, does it waste memory?
            self.I_vs_wave.plot(wavelengths,intensities)
            self.I_vs_wave.set_xlabel('Wavelength (nm)')
            self.I_vs_wave.set_ylabel('Intensity (a.u.)')
            self.I_vs_wave.grid(True)

            #remake bounds
            left,right = self.I_vs_wave.get_xlim()
            down,up = self.I_vs_wave.get_ylim()
            if self.min_wave_var.get() != '':
                left = int(self.min_wave_var.get())
                self.I_vs_wave.set_xlim([left,right])
            if self.max_wave_var.get() != '':
                self.I_vs_wave.set_xlim([left,int(self.max_wave_var.get())])
            if self.min_intense_var.get() != '':
                down = int(self.min_intense_var.get())
                self.I_vs_wave.set_ylim([down,up])
            if self.max_intense_var.get() != '':
                self.I_vs_wave.set_ylim([down,int(self.max_intense_var.get())])
            
            self.spectral_canvas.draw()
            
            #keep repeating this function
            self.spectral_cancel_id = self.after(1,self.graph_spectrum)

        else:
            msgbox.showerror('Yikes', 'No spectrometer connected')
    def stop_graphing(self):
        if self.spectral_cancel_id != None:
            self.after_cancel(self.spectral_cancel_id)
            self.spectral_cancel_id = None
        else:
            msgbox.showerror('Yikes','No graph to stop')



    def shutdown(self):
        plt.close('all')
        if self.spec != None:
            try:
                self.spec.destroy()
            except:
                msgbox.showerror('Yikes', 'No spectrometer to disconnect')
        





