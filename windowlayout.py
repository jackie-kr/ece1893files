from __future__ import annotations
from typing import *
import sys
import os
from matplotlib.backends.qt_compat import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvas
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QCheckBox, QLineEdit
#pyqt check box
#pyqt file dialog, file menu bar, QMenuBar
from PyQt5.QtCore import pyqtSlot
import matplotlib as mpl
import numpy as np
import random
import time
from functools import partial

checks = []
live_button = None
sweep_button = None
fig = None
wave_min = None
wave_max = None

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1000,600)

        self.main_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.main_widget)

        self.full_horizontal = QtWidgets.QHBoxLayout(self.main_widget)

        self.left_vertical = QtWidgets.QVBoxLayout(self.main_widget)
        global checks
        for i in range(1,5):
            check = QtWidgets.QCheckBox(f'Channel {i}',self.main_widget)
            self.left_vertical.addWidget(check)
            checks.append(check)

        global fig
        fig = GraphCanvas(interval=20)

        self.save_button = QPushButton('Save Data',self.main_widget)
        self.save_button.clicked.connect(fig.save_data)
        self.left_vertical.addWidget(self.save_button)
        self.full_horizontal.addLayout(self.left_vertical)

        self.right_vertical = QtWidgets.QVBoxLayout(self.main_widget)
        self.top_horizontal = QtWidgets.QHBoxLayout(self.main_widget)
        global live_button, sweep_button, wave_max, wave_min
        live_button = QPushButton('Live',self.main_widget)
        sweep_button = QPushButton('Sweep',self.main_widget)
        sweep_button.clicked.connect(self.run_sweep)
        self.right_vertical.addLayout(self.top_horizontal)

        self.top_horizontal.addWidget(live_button)
        #run_live = partial(live_graph)
        self.top_horizontal.addWidget(sweep_button)
        wave_min = QLineEdit('Min wavelength',self.main_widget)
        wave_max = QLineEdit('Max wavelength',self.main_widget)
        self.top_horizontal.addWidget(wave_min)
        self.top_horizontal.addWidget(wave_max)
        self.right_vertical.addWidget(fig)

        self.full_horizontal.addLayout(self.right_vertical)

        self.show()
    @staticmethod
    def run_sweep():
        global wave_max, wave_min
        fig.sweep_graph(min=int(wave_min.text()),max=int(wave_max.text()))

class GraphCanvas(FigureCanvas):
    def __init__(self, interval:int):
        super().__init__()
        self.start_time = time.time()

        self.x_vals = []
        self.y_vals = [[],[],[],[]]

        self.ax = self.figure.subplots()
        self.x_label = "Time"
        self.y_label = "Output Power"
        self.file_legend = ["Channel 1","Channel 2","Channel 3","Channel 4"]

        self.timer = self.new_timer(interval, [(self.live_update, (), {})])
        self.timer.start()
        return

    def live_update(self) -> None:
        self.x_vals.append(time.time()-self.start_time)
        self.ax.clear()
        self.x_label = "Time"
        self.file_legend = ["Channel 1","Channel 2","Channel 3","Channel 4"]

        try:
            self.x_vals = self.x_vals[-100:]
        except:
            pass
        for i in range(0,4):
            self.y_vals[i].append(random.randint(1,20*(i+1)))
            try:
                self.y_vals[i] = self.y_vals[i][-100:]
            except:
                pass
            if checks[i].isChecked():
                self.ax.plot(self.x_vals, self.y_vals[i])
            else:
                self.ax.plot([],[])
        self.ax.legend(["Channel 1","Channel 2","Channel 3","Channel 4"],loc="upper left")
        self.ax.set_xlabel(self.x_label)
        self.ax.set_ylabel(self.y_label)
                    
        #self.ax.set_ylim(ymin=self.y_range[0], ymax=self.y_range[1])
        self.draw()
        return

    def sweep_graph(self, min:int,max:int):
        self.timer.stop()
        self.x_label = "Wavelength"
        self.file_legend = ["Output Power"]

        self.x_vals = []
        self.y_vals = [[]]

        for i in range(min,max):
            self.x_vals.append(i)
            self.y_vals[0].append(random.randint(10,20))
            
        self.ax.clear()
        self.ax.plot(self.x_vals,self.y_vals[0])
        self.ax.set_xlabel(self.x_label)
        self.ax.set_ylabel(self.y_label)
        self.draw()
        return
    def save_data(self):
        save_file = open("graphdata.txt","a")
        banner = ""
        banner += self.x_label + ", "
        for i in self.file_legend:
            banner += i + ", "
        save_file.write(f"{banner}\n")
        for i in range(len(self.y_vals[0])):
            val_line = ""
            val_line += str(self.x_vals[i]) + ", "
            for j in self.y_vals:
                val_line += str(j[i]) + ", "
            save_file.write(f"{val_line}\n")
        save_file.close()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    ui = MainWindow()
    ui.show()
    app.exec_()