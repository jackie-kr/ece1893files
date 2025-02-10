from __future__ import annotations
from typing import *
import sys
import os
from matplotlib.backends.qt_compat import QtCore, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvas
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QCheckBox
#pyqt check box
#pyqt file dialog, file menu bar, QMenuBar
from PyQt5.QtCore import pyqtSlot
import matplotlib as mpl
import numpy as np
import random
import time
from functools import partial

class ApplicationWindow(QtWidgets.QMainWindow):
    #this was the previous set-up with buttons and homescreen, obselete
    """def __init__(self):
        super().__init__()
        self.setGeometry(300,300,800,400)
        
        self.channels = []
        for i in range(1,5):
            button = QPushButton(f'Channel {i}',self)
            button.move(i*150,70)
            run_graph = partial(self.on_click, i, i*20)
            button.clicked.connect(run_graph)

        self.show()

    def on_click(self, ch:int, max:int):
        self.setGeometry(300, 300, 800, 400)
        self.setWindowTitle("Channel 1")
        self.frm = QtWidgets.QFrame(self)
        
        self.lyt = QtWidgets.QHBoxLayout()
        self.left_lyt = QtWidgets.QVBoxLayout()
        self.checks = []
        for i in range(1,5):
            wave_check = QCheckBox(f'Channel {i}',self)
            self.checks.append(wave_check)
        self.frm.setLayout(self.lyt)
        self.setCentralWidget(self.frm)

        self.fig = GraphCanvas(limit=max, interval=20)
        self.left_lyt.addWidget(self.left_lyt)
        self.lyt.addWidget(self.fig)

        self.show()"""
    def __init__(self):
        super().__init__()
        self.setGeometry(1000, 700, 1000, 700)
        self.setWindowTitle("Channel 1")
        self.main_widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.main_widget)
        #self.frm = QtWidgets.QFrame(self)
        
        self.lyt = QtWidgets.QHBoxLayout(self.main_widget)
        self.left_lyt = QtWidgets.QVBoxLayout(self.main_widget)
        self.checks = []
        for i in range(1,5):
            wave_check = QCheckBox(f'Channel {i}',self)
            self.checks.append(wave_check)
            self.left_lyt.addWidget(wave_check)
        #self.frm.setLayout(self.lyt)
        #self.setCentralWidget(self.frm)

        self.fig = GraphCanvas(limit=60, interval=20)
        
        self.left_lyt.addWidget(self.fig)
        self.left_lyt.addLayout(self.left_lyt)

        self.show()

class GraphCanvas(FigureCanvas):
    def __init__(self, limit:int, interval:int):
        super().__init__()
        self.start_time = time.time()

        self.limit = limit
        self.y_range = [0,limit]

        self.x_vals = []
        self.y_vals = []

        self.ax = self.figure.subplots()

        self.timer = self.new_timer(interval, [(self.update_canvas, (), {})])
        self.timer.start()
        return

    def update_canvas(self) -> None:
        self.x_vals.append(time.time()-self.start_time)
        self.y_vals.append(random.randint(1,self.limit))     
        self.ax.clear()
        self.ax.plot(self.x_vals, self.y_vals)            
        #self.ax.set_ylim(ymin=self.y_range[0], ymax=self.y_range[1])
        self.draw()
        return

if __name__ == "__main__":
    qapp = QtWidgets.QApplication(sys.argv)
    app = ApplicationWindow()
    qapp.exec_()