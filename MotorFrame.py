import tkinter as tk
import tkinter.messagebox as msgbox
#import ThorLabsMotor
import pathlib

SPEED_OF_LIGHT = 3e8
FEMTO_TO_SEC = 1e-15
METERS_TO_MILLI = 1e3
FEMTO_TO_MILLI = SPEED_OF_LIGHT * FEMTO_TO_SEC * METERS_TO_MILLI #use later for conversion

class MotorFrame(tk.Frame):
    def __init__(self,parent):
        tk.Frame.__init__(self,parent,highlightbackground='red',highlightthickness=2)
        
        #initialize the strings for user input
        self.step_size = tk.StringVar(self)
        self.delay_scan_width = tk.StringVar(self)
        self.jog_size = tk.StringVar(self)
        self.position = tk.StringVar(self)
        self.saved_position = tk.StringVar(self)


        #name and serial numer for motor is needed
        #   maybe make it a user input later on?
        self.motor_name = tk.StringVar(self)
        self.serial_number = tk.StringVar(self)
        self.motor = None

        #Create Controls

        self.ControlFrame = tk.Frame(self,highlightbackground='black',highlightthickness=2)
        self.ControlFrame.grid(row=0,column=0)

        self.connect_motor_button = tk.Button(self.ControlFrame, text='Connect motor', command=self.connect_motor)
        self.connect_motor_button.grid(row=0,column=0)
        self.disconnect_motor_button = tk.Button(self.ControlFrame, text='Disconnect motor', command=self.disconnect_motor)
        self.disconnect_motor_button.grid(row=0,column=1)
        self.motor_status = tk.Label(self.ControlFrame, text='Disconnected')
        self.motor_status.grid(row=0, column=2)
        self.home_button = tk.Button(self.ControlFrame, text='Home motor',command=self.home)
        self.home_button.grid(row=0,column=3)

        self.step_size_label = tk.Label(self.ControlFrame,text='Step size (fs)')
        self.step_size_label.grid(row=1,column=0)
        self.step_size_entry = tk.Entry(self.ControlFrame, textvariable=self.step_size)
        #self.step_size_entry.bind('<Return>', self.)
        self.step_size_entry.grid(row=1,column=1)

        self.delay_scan_width_label = tk.Label(self.ControlFrame, text='Delay scan width (fs)')
        self.delay_scan_width_label.grid(row=2,column=0)
        self.delay_scan_width_entry = tk.Entry(self.ControlFrame, textvariable=self.delay_scan_width)
        
        self.delay_scan_width_entry.grid(row=2, column=1)

        self.jog_size_label = tk.Label(self.ControlFrame, text='Jog size (mm)')
        self.jog_size_label.grid(row=3,column=0)
        self.jog_size_entry = tk.Entry(self.ControlFrame, textvariable=self.jog_size)
        self.jog_size_entry.bind('<Return>',self.set_jog)
        self.jog_size_entry.grid(row=3,column=1)
        self.jog_forward_button = tk.Button(self.ControlFrame, text='Jog forward',command=self.jog_forward)
        self.jog_forward_button.grid(row=3,column=2)
        self.jog_backward_button = tk.Button(self.ControlFrame, text='Jog backward',command=self.jog_backward)
        self.jog_backward_button.grid(row=3,column=3)


        self.position_label = tk.Label(self.ControlFrame, text='Current Position (mm and fs)')
        self.position_label.grid(row=4,column=0)
        self.position_post = tk.Label(self.ControlFrame, text='No position until motor connected')
        self.position_post.grid(row=4,column=1)
        self.position_post_fs = tk.Label(self.ControlFrame, text='No position until motor connected')
        self.position_post_fs.grid(row=4,column=2)
        self.position_move_label = tk.Label(self.ControlFrame,text= 'Move to Position')
        self.position_move_label.grid(row=4,column=3)
        self.position_move_entry = tk.Entry(self.ControlFrame, textvariable=self.position)
        self.position_move_entry.bind('<Return>',self.move_to_position)
        self.position_move_entry.grid(row=4,column=4)

        self.move_to_save_button = tk.Button(self.ControlFrame,text='Move to saved position',command=self.move_to_save)
        self.move_to_save_button.grid(row=5,column=0)
        self.save_button = tk.Button(self.ControlFrame,text='Save current position',command=self.save_position)
        self.save_button.grid(row=5,column=1)
        self.saved_label = tk.Label(self.ControlFrame, text='Current saved position (mm)')
        self.saved_label.grid(row=5,column=2)
        self.saved_entry = tk.Label(self.ControlFrame, text='Connect the motor first')
        self.saved_entry.grid(row=5,column=3)


    def refresh_position(self):
        self.position_post.config(text="{:.5f}".format(self.motor.get_position()))
        self.position_post_fs.config(text="{:.5f}".format(self.motor.get_position() / FEMTO_TO_MILLI))
    def connect_motor(self):
        #can improve by letting the user define the motor serial number and name
        try:
            self.motor = ThorLabsMotor.Controller('26005057', 'ZST225')
            #self.motor = ThorLabsMotor.Controller('26002816', 'ZST225')
            self.motor.connect()
            self.motor_status.config(text='Connected')
            path = pathlib.Path('./saved_motor_position.p')
            if path.is_file():
                #print('path is indeed file')
                self.set_save()
            self.refresh_position()
        except:
            msgbox.showerror('yikes','issue with connecting to motor')
    def disconnect_motor(self):
        try:
            self.motor.disconnect()
            self.motor = None
            self.motor_status.config(text='Disconnected')
            self.motor_status
        except:
            msgbox.showerror('Yikes', 'Trouble with disconnecting motor')
    def home(self):
        if self.motor != None:
            if not self.motor.is_homed():
                try:
                    self.motor.home()
                except:
                    msgbox.showerror('Yikes','Issue with homing motor')
            else:
                msgbox.showerror('man','Motor is already homed')
        else:
            msgbox.showerror('Yikes','No motor connected')
    def set_jog(self,event):
        self.motor.set_jog_step_size(float(self.jog_size.get()))
    def jog_forward(self):
        self.motor.jog_forward()
        self.refresh_position()
    def jog_backward(self):
        self.motor.jog_backward()
        self.refresh_position()
    def move_to_position(self,event):
        self.motor.move_absolute(float(self.position.get()))
        self.refresh_position()
    def move_to_save(self):
        path = pathlib.Path('./saved_motor_position.p')
        if not path.is_file():
            msgbox.showerror('Yikes', 'no saved position file in directory')
        else:
            try:
                self.motor.move_to_saved_motor_position()
                self.refresh_position()
            except Exception as e:
                #print(e)
                msgbox.showerror('yikes','could not move to saved positon')
    def save_position(self):
        try:
            self.motor.save_this_motor_position()
            self.set_save()
        except:
            msgbox.showerror('yikes','could not save position')
    def set_save(self):
            self.saved_entry.config(text=self.motor.get_saved_position())






