# FROG_
Creating an API for spectrometer and motor controller
**Currently only compatible with Windows OS**

# Necessary Downloads
* Download Thorlabs kinesis software for the DLLS: https://www.thorlabs.com/software_pages/ViewSoftwarePage.cfm?Code=Motion_Control&viewtab=0
  * There is a file called Thorlabs.MotionControl.DotNet_API.chm which is basically the documentation for all the functions that the motor controller software provides
* A couple of Python libraries to import:
  * tkinter
  * seabreeze
  * seatease
  * pythonnet

# Some GOATED githubs:
* [SeaBreeze](https://github.com/ap--/python-seabreeze): Lets you use Ocean Optics spectrometer through python
* [SeaTease](https://github.com/jonathanvanschenck/python-seatease): Simulates Ocean Optics spectrometer to test code without need of physical spectrometer
* [ThorLabs Motor Stepper](https://github.com/rwalle/py_thorlabs_ctrl/blob/master/py_thorlabs_ctrl/kinesis/motor.py): Code to interface with Thorlabs motor via python. Not exactly what I implemented, but helpful reference to functions in the Thorlabs dll.

There was somethign wacky with seabreeeze. I think you have to update the visual c++ things, but I don't quite remember the steps
