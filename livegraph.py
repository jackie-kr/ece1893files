import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import style
import time
import random
import sys

from PyQt5.QtCore import QSize, Qt, QThread, pyqtSignal, QObject
from matplotlib.backends.qt_compat import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow, QPushButton, QHBoxLayout, QVBoxLayout, QProgressBar
from PyQt5.QtGui import QFont
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

style.use('fivethirtyeight')

fig = plt.figure()
axl = fig.add_subplot(1,1,1)


"""
data = []
for i in range(100):
    data.append(random.randint(1,10))
"""

start_time = time.time()

"""
#how long between each updated frame
frame_time = 0.01

x_vals = []
y_vals = []

def animate(i):
    live_time = time.time() - start_time

    #graphing a function of time and wavelength, using sample random data
    x_vals.append(live_time)
    y_vals.append(random.randint(1,10))

    #if needed, adding a frame time
    #time.sleep(frame_time)

    axl.clear()
    axl.plot(x_vals,y_vals)

#ani = animation.FuncAnimation(fig, animate, interval=1000)
#plt.show()
"""

class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        start_time = time.time()

        channels = []
        """for i in range(1,5):
            button = QPushButton(f'Channel {i}', self)
            button.move(100*i,70)
            button.clicked.connect(lambda: self.on_click(i*20))"""
        
        self.lyt = QtWidgets.QVBoxLayout()
        self.graph_fig = GraphCanvas(10)
        self.lyt.addWidget(self.graph_fig)

        self.show()
        return


class GraphCanvas(FigureCanvas):
    def __init__(self, limit:int):
        super().__init__()
        self.start_time = time.time()
        
        self.x_vals = []
        self.y_vals = []
        self.limit = limit

        self.ax = self.figure.subplots()

        self.timer_ = self.new_timer(30, [(self.update_graph, (), {})])
        self.timer_.start()
        return
    def update_graph(self):
        self.x_vals.append(time.time()-self.start_time)
        self.y_vals.append(random.randint(1,self.limit))
        self.ax.clear()
        self.ax.plot(self.x_vals,self.y_vals)
        self.draw()


app = QApplication(sys.argv)
ex = ApplicationWindow()
sys.exit(app.exec_())