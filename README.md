# FROG_
Creating an API for spectrometer and motor controller
**Currently only compatible with Windows OS**

# How to use
* Run the prgram by either launching the executible or running the "FROG_GUI_2.0.py" script

<img src="tutorial_photos/full_gui.png">

## Spectrometer Controls
* Connecting to a real or virtual spectrometer
* The virtual spectrometer will output a spectrum sharply peaked at 500 nm
* The program will attempt to connect to the first OceanOptics spectrometer it sees connected to the computer when prompted by the user
  * Does not allow for the user to choose which spectrometer it will connect to (yet)
* Change the wavelength range that will be outputted on the graph
  * This also changes the range of data recorded on the FROG
* Change the intensity range that will be outputted on the graph (useful for rescaling)
* Change the integration time
  * Expect lag/slowdown for long integration times (>500 ms) when graphing the spectrum. For this, I recommend breifly graphing the spectrum to ensure the output is what you expect and then stop graphing. When FROGing, the spectrum will be shown and updated at each step.
* Toggle to start and stop graphing the spectrum
* Toggle to automatically subtract the background from the spectrometer reading or display the raw spectrometer output.
  * This will also affect the data collected when FROGing
* Anytime the user attempts to connect a spectrometer or change the integration time, a pop-up will appear to ask the user to block the beam for the program to collect a new background measurement

<img src="tutorial_photos/spec_controls.png">

## Motor Controls
* Nice

<img src="tutorial_photos/motor_controls.png">

## FROG Controls
* Nice

<img src="tutorial_photos/frog_controls.png">

## Example FROG
* Ncie

<img src="tutorial_photos/example_frog.png">

# Necessary Downloads
* Download Thorlabs kinesis software for the DLLS: https://www.thorlabs.com/software_pages/ViewSoftwarePage.cfm?Code=Motion_Control&viewtab=0
  * There is a file called Thorlabs.MotionControl.DotNet_API.chm which is basically the documentation for all the functions that the motor controller software provides
* A couple of Python libraries to import:
  * tkinter
  * seabreeze
    * Note: Installing seeabreeze is a bit tricky on Windows. You'll need to ensure you have Visual Studio and Windows SDK installed then restart computer
  * seatease
  * pythonnet

# Some GOATED githubs:
* [SeaBreeze](https://github.com/ap--/python-seabreeze): Lets you use Ocean Optics spectrometer through python
* [SeaTease](https://github.com/jonathanvanschenck/python-seatease): Simulates Ocean Optics spectrometer to test code without need of physical spectrometer
* [ThorLabs Motor Stepper](https://github.com/rwalle/py_thorlabs_ctrl/blob/master/py_thorlabs_ctrl/kinesis/motor.py): Code to interface with Thorlabs motor via python. Not exactly what I implemented, but helpful reference to functions in the Thorlabs dll.

God speed brother
