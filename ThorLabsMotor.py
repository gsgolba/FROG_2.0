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
WAIT_TIME = 1
class Controller:
    def __init__(self, serial_num, motor_name):
        self.serial_num = serial_num
        self.motor_name = motor_name
        DeviceManagerCLI.BuildDeviceList()
        self.controller = KCubeStepper.CreateKCubeStepper(self.serial_num)
    def connect(self):
        if not self.controller == None:
            self.controller.Connect(self.serial_num)
            if not self.controller.IsSettingsInitialized():
                self.controller.WaitForSettingsInitialized(3000)
            
            self.controller.StartPolling(50) #send updates to PC, in ms
            time.sleep(0.1)
            self.controller.EnableDevice()
            time.sleep(0.1)

        config =  self.controller.LoadMotorConfiguration(self.serial_num, DeviceConfiguration.DeviceSettingsUseOptionType.UseFileSettings)
        config.DeviceSettingsName = str(self.motor_name)
        config.UpdateCurrentConfiguration()
        self.controller.SetSettings(self.controller.MotorDeviceSettings, True, False)
    def disconnect(self):
        self.controller.StopPolling()
        self.controller.Disconnect(False)
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
        self.controller.Home(0)
        self.wait()
    def move_relative(self, dis):
        #print('do relative move')
        self.controller.SetMoveRelativeDistance(Decimal(dis))
        self.controller.MoveRelative(0)
        self.wait()
    def move_absolute(self, pos):
        self.wait()
        self.controller.MoveTo(Decimal(pos), 0)
        self.wait()
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
        self.controller.MoveJog(MotorDirection.Forward, 0)
        self.wait()
        #print('forward done')
    def jog_backward(self):
        self.controller.MoveJog(MotorDirection.Backward, 0)
        self.wait()
        #print('backward done')
    def wait(self, waitTimeout = WAIT_TIME):
        if self.controller.IsDeviceBusy:
            #print('device busy')
            time.sleep(waitTimeout)
            self.wait()
        return
    def is_controller_busy(self):
        return self.controller.IsDeviceBusy
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
    myController = Controller(str('26001568'), str('ZST225'))
    myController.connect()
    myController.set_jog_step_size(0.5)
    print('my step size: ', myController.get_jog_step_size())
    #myController.jog_forward()
    #print(myController.get_position())
    #myController.jog_backward()
    #myController.move_absolute(3)
    print(myController.get_position())
    myController.move_absolute(4)
    #myController.save_this_motor_position()
    myController.move_absolute(0)
    myController.move_to_saved_motor_position()
    myController.move_absolute(0)
    myController.disconnect()

if __name__ == "__main__":
    main()