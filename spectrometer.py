# Get any spectrometer
import seatease.spectrometers as s
import seatease.cseatease as c
import seabreeze.spectrometers as S
#import matplotlib.pyplot as plt
MILLI_TO_MICRO = 1000
def main(): 
    print('not meant to be used as primary file')
    print(S.list_devices())
    print(s.list_devices())
    spec = s.Spectrometer.from_first_available()
    min_, max_ = spec.integration_time_micros_limits
    print(min_, max_)
    print(len(spec.intensities()))
    print(len(spec.wavelengths()))
    print(spec.wavelengths()[1203:1242])
    spec.close()
    for i in range(1):
        print(i)

#if we have time, create a super class
#for both virtual and real spectrometer

class Spectrometer:
    def __init__(self):
        #for now we just connect from first available
        self.spec = S.Spectrometer.from_first_available()
        self.spec.integration_time_micros(5000)
        #create function to change integration time
    def get_intensities(self):
        return self.spec.intensities()
    def get_wavelengths(self): #range from 195.055 - 1112.235, 3648 points
        return self.spec.wavelengths()
    def get_both(self):
        return self.spec.spectrum()
    def change_integration_time(self, time): #in us
        time = int(time)
        time *= MILLI_TO_MICRO
        self.spec.integration_time_micros(time)
    def destroy(self):
        self.spec.close()

class Virtual_Spectrometer:
    def __init__(self):
        #for now we just connect from first available
        self.spec = s.Spectrometer.from_first_available()
        self.spec.integration_time_micros(5000)
        #create function to change integration time
    def get_intensities(self):
        return self.spec.intensities()
    def get_wavelengths(self): #range from 300 - 1000, 4096 points
        return self.spec.wavelengths()
    def get_both(self):
        return self.spec.spectrum()
    def change_integration_time(self, time): #in us
        time = int(time)
        time *= MILLI_TO_MICRO
        self.spec.integration_time_micros(time)
    def destroy(self):
        self.spec.close()


if __name__ == "__main__":
    main()
