import tkinter
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib import pyplot as plt, animation
import numpy as np
import spectrometer

plt.rcParams["figure.figsize"] = [7.00, 3.50]
plt.rcParams["figure.autolayout"] = True

spec = spectrometer.Virtual_Spectrometer()
print(spec)
print(spec.get_both())

root = tkinter.Tk()
root.wm_title("Embedding in Tk")

plt.axes(xlim=(0, 2), ylim=(-2, 2))
fig = plt.Figure(dpi=100)
ax = fig.add_subplot(xlim=(300, 1000), ylim=(-1, 200))
line, = ax.plot([], [], lw=2)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.draw()

toolbar = NavigationToolbar2Tk(canvas, root, pack_toolbar=False)
toolbar.update()

canvas.mpl_connect(
    "key_press_event", lambda event: print(f"you pressed {event.key}"))
canvas.mpl_connect("key_press_event", key_press_handler)

button = tkinter.Button(master=root, text="Quit", command=root.quit)
button.pack(side=tkinter.BOTTOM)

toolbar.pack(side=tkinter.BOTTOM, fill=tkinter.X)
canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

def init():
    line.set_data([], [])
    return line,

def animate(i):
    #x = np.linspace(0, 2, 1000)
    #y = np.sin(2 * np.pi * (x - 0.01 * i))
    x,y = spec.get_both()
    line.set_data(x, y)
    return line,

anim = animation.FuncAnimation(fig, animate, init_func=init, interval=20, blit=True)


#plt.axes(xlim=(0, 2), ylim=(-2, 2))
fig1 = plt.Figure(dpi=100)
ax1 = fig1.add_subplot(xlim=(0, 2), ylim=(-1, 1))
line1, = ax1.plot([], [], lw=2)

canvas1 = FigureCanvasTkAgg(fig1, master=root)
canvas1.draw()

toolbar1 = NavigationToolbar2Tk(canvas, root, pack_toolbar=False)
toolbar1.update()

canvas1.mpl_connect(
    "key_press_event", lambda event: print(f"you pressed {event.key}"))
canvas1.mpl_connect("key_press_event", key_press_handler)

button1 = tkinter.Button(master=root, text="Quit", command=root.quit)
button1.pack(side=tkinter.BOTTOM)

toolbar1.pack(side=tkinter.BOTTOM, fill=tkinter.X)
canvas1.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

def init1():
    line1.set_data([], [])
    return line1,

def animate1(i):
    x = np.linspace(0, 2, 1000)
    y = np.sin(2 * np.pi * (x - 0.01 * i))
    line1.set_data(x, y)
    return line1,

anim1 = animation.FuncAnimation(fig1, animate1, init_func=init1,frames=200, interval=20, blit=True)

tkinter.mainloop()
