import time
import clr
import pickle
clr.AddReference("C:\Program Files\Thorlabs\Kinesis\Thorlabs.MotionControl.DeviceManagerCLI.dll")
clr.AddReference("C:\Program Files\Thorlabs\Kinesis\Thorlabs.MotionControl.GenericMotorCLI.dll")
clr.AddReference("C:\Program Files\Thorlabs\Kinesis\Thorlabs.MotionControl.KCube.StepperMotorCLI.dll")
from Thorlabs.MotionControl.DeviceManagerCLI import *
from Thorlabs.MotionControl.GenericMotorCLI import *
from Thorlabs.MotionControl.GenericMotorCLI import KCubeMotor
from Thorlabs.MotionControl.GenericMotorCLI.ControlParameters import JogParametersBase
from Thorlabs.MotionControl.KCube.StepperMotorCLI import *
from System import Decimal


UNIT_CONVERTER = 4.901960784313725
WAIT_TIME = 1.0
MOVE_WAIT_TIME = 60000
class Controller:
    def __init__(self, serial_num, motor_name):
        self.serial_num = serial_num
        self.motor_name = motor_name
        try:
            DeviceManagerCLI.BuildDeviceList()
        except:
            print('Trouble with building device on DeviceManagerCLI')
            return
        try:
            self.controller = KCubeStepper.CreateKCubeStepper(self.serial_num)
        except:
            print('Could not make the KCubeStepper motor instance ')
            self.controller = None
    def connect(self):
        if self.controller == None:
            print('no KCubeStepper instance is succesfully created')
            return
        else:
            self.controller.Connect(self.serial_num)
            if not self.controller.IsSettingsInitialized():
                try:
                    self.controller.WaitForSettingsInitialized(3000) #wait for the device settings to initialize
                except:
                    print('Could not initialize settings')
            self.controller.StartPolling(50) #send updates to PC, in ms. Basically a way to keep track of device
            time.sleep(0.5)
            self.controller.EnableDevice()
            time.sleep(0.5)
            # Call LoadMotorConfiguration on the device to 
            #   initialize the DeviceUnitConverter object 
            #   required for real world unit parameters
            # maybe attempt with the second parameter
            config =  self.controller.LoadMotorConfiguration(self.serial_num, DeviceConfiguration.DeviceSettingsUseOptionType.UseFileSettings)
            config.DeviceSettingsName = str(self.motor_name)
            config.UpdateCurrentConfiguration()
            self.controller.SetSettings(self.controller.MotorDeviceSettings, True, False)
    def disconnect(self):
        self.controller.StopPolling()
        self.controller.Disconnect(True)
    def get_serial_number(self):
        device_info = self.controller.GetDeviceInfo()
        return device_info.SerialNumber
    def get_name(self):
        device_info = self.controller.GetDeviceInfo()
        return device_info.Name
    def get_position(self):
        return Decimal.ToDouble(self.controller.DevicePosition)
    def is_homed(self):
        return self.controller.Status.IsHomed
    def home(self):
        #print('homing')
        self.controller.Home(MOVE_WAIT_TIME)
    def move_relative(self, dis):
        #print('do relative move')
        self.controller.SetMoveRelativeDistance(Decimal(dis))
        self.controller.MoveRelative(MOVE_WAIT_TIME)
    def move_absolute(self, pos):
        #print('moving device to ', Decimal(pos))
        self.controller.MoveTo(Decimal(pos), MOVE_WAIT_TIME)
        #print('move absolute done')
    def disable(self):
        self.controller.DisableDevice()
    def set_jog_step_size(self, step_size):
        jog_params = self.controller.GetJogParams()
        jog_params.StepSize = Decimal(step_size)
        jog_params.JogMode = JogParametersBase.JogModes.SingleStep
        self.controller.SetJogParams(jog_params)
    def get_jog_step_size(self):
        return self.controller.GetJogStepSize()
    def jog_forward(self):
        while self.controller.IsDeviceBusy:
            print('waiting for motor')
            time.sleep(WAIT_TIME)
        #print('doing forward jog')
        self.controller.MoveJog(MotorDirection.Forward, MOVE_WAIT_TIME)
    def jog_backward(self):
        while self.controller.IsDeviceBusy:
            print('waiting for motor')
            time.sleep(WAIT_TIME)
        #print('doing backward jog')
        self.controller.MoveJog(MotorDirection.Backward, MOVE_WAIT_TIME)
    def save_this_motor_position(self):
        '''
        Couldn't think of a simpler solution:
        we use pickle to store the current motor position in a file
        we can then grab this value by opening the file
        we edit this file each time to save a new position
        if we want to save multiple positions,
            just add more files, or have it be a list in a single file
        '''
        with open('saved_motor_position.p', 'wb') as f:
            pickle.dump(self.get_position(),f)
    def move_to_saved_motor_position(self):
        with open('saved_motor_position.p', 'rb') as f:
            self.move_absolute(pickle.load(f))
            self.wait()
    def get_saved_position(self):
        with open('saved_motor_position.p', 'rb') as f:
            return str(pickle.load(f))
        
def main():
    #Below is just code to test whether we can move the motor accordingly
    myController = Controller('26002816', 'ZST225')
    myController.connect()
    myController.set_jog_step_size(0.5)
    print('my step size: ', myController.get_jog_step_size())
    myController.move_absolute(2.0)
    print(myController.is_homed())
    myController.home()
    print(myController.is_homed())
    myController.jog_forward()
    myController.jog_forward()
    myController.jog_backward()
    print(myController.is_homed())

    myController.disconnect()
    #CURERNT POS: 5.3664

if __name__ == "__main__":
    main()