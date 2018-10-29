import sys
from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui, QtCore, Qt
import numpy as np
import pyqtgraph as pg


class num_methods(qw.QWidget):
    
    #initialize method
    def __init__(self):
        super(num_methods, self).__init__()
        
        #init conditions
        self.x_0 = 0
        self.y_0 = 1
        self.step = 0.1
        self.c1 = (self.y_0 + self.x_0 - 1) / np.e ** (-self.x_0)

        self.X = 10

        self.x_axis = np.arange(self.x_0, self.X + self.step, self.step, float)

        self.t = 0
        
        self.init_ui() #init user interface components
        self.qt_connections() #add events to buttons
        
        #create curves for graph of numerical methods
        self.plotcurve_euler = pg.PlotCurveItem(name='...Euler', pen=(255, 0, 0))
        self.plotcurve_adv_euler = pg.PlotCurveItem(name='..Improved Euler', pen=(0, 255, 0))
        self.plotcurve_runge_kutt = pg.PlotCurveItem(name='...Runge-Kutta', pen=(0, 0, 255))
        
        #create curves for graph of errors
        self.plotcurve_err_euler = pg.PlotCurveItem(name='...Euler', pen=(255, 0, 0))
        self.plotcurve_err_adv_euler = pg.PlotCurveItem(name='..Improved Euler', pen=(0, 255, 0))
        self.plotcurve_err_runge_kutt = pg.PlotCurveItem(name='...Runge-Kutta', pen=(0, 0, 255))
        
        #create curve for exact solution graph
        self.plotcurve_ex = pg.PlotCurveItem(name='..Exact')
        
        #adding curves to the first graph (methods)
        self.plotwidget.addItem(self.plotcurve_euler)
        self.plotwidget.addItem(self.plotcurve_adv_euler)
        self.plotwidget.addItem(self.plotcurve_runge_kutt)
        
        #adding curves to the second graph (errors)
        self.plotwidget_err.addItem(self.plotcurve_err_euler)
        self.plotwidget_err.addItem(self.plotcurve_err_adv_euler)
        self.plotwidget_err.addItem(self.plotcurve_err_runge_kutt)
        
        #adding curve to the exact solution graph
        self.plotwidget_ex.addItem(self.plotcurve_ex)
        
        #update plot
        self.updateplot()
        
        #for debug
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.moveplot)
        self.timer.start(500)
    
    #create UI components
    def init_ui(self):
        self.setWindowTitle('Numerical methods')
        
        #layout for elements positioning
        hbox = qw.QGridLayout()
        self.setLayout(hbox)
        
        #create graph for methods
        self.plotwidget = pg.PlotWidget()
        self.plotwidget.addLegend()
        self.plotwidget.showGrid(x=True, y=True, alpha=0.3)
        hbox.addWidget(self.plotwidget, 0, 0, 3, 3)
        
        #create graph for errors
        self.plotwidget_err = pg.PlotWidget()
        self.plotwidget_err.setRange(yRange=[0.0001, 20])
        self.plotwidget_err.addLegend()
        self.plotwidget_err.showGrid(x=True, y=True, alpha=0.3)
        hbox.addWidget(self.plotwidget_err, 0, 4, 3, 3)
        
        #create graph for exact
        self.plotwidget_ex = pg.PlotWidget()
        self.plotwidget_ex.addLegend()
        self.plotwidget_ex.showGrid(x=True, y=True, alpha=0.3)
        hbox.addWidget(self.plotwidget_ex, 4, 4, 8, 3)
        
        #create buttons for setting init conditions
        self.btn_set_step = qw.QPushButton('Set step')
        self.btn_set_reg = qw.QPushButton('Set region')
        self.btn_set_x0 = qw.QPushButton('Set x0')
        self.btn_set_y0 = qw.QPushButton('Set y0')
        
        #create buttons for resetting init conditions
        self.btn_reset_step = qw.QPushButton('Default (0.1)')
        self.btn_reset_reg = qw.QPushButton('Default (10)')
        self.btn_reset_x0 = qw.QPushButton('Default (0)')
        self.btn_reset_y0 = qw.QPushButton('Default (1)')
        
        #fields for init conditions input
        self.lbl_step = qw.QLineEdit('0.1')
        self.lbl_region = qw.QLineEdit('10')
        self.lbl_x_0 = qw.QLineEdit('0')
        self.lbl_y_0 = qw.QLineEdit('1')
        
        #validators for only Double/Int input
        self.onlyDouble = QtGui.QDoubleValidator()
        self.onlyInt = QtGui.QIntValidator()
        locale = QtCore.QLocale(QtCore.QLocale.English)
        self.onlyDouble.setLocale(locale)

        self.lbl_step.setValidator(self.onlyDouble)
        self.lbl_region.setValidator(self.onlyInt)
        self.lbl_x_0.setValidator(self.onlyDouble)
        self.lbl_y_0.setValidator(self.onlyDouble)
        
        #adding created components to the layout
        hbox.addWidget(self.lbl_step, 4, 0, 1, 1)
        hbox.addWidget(self.lbl_region, 6, 0, 1, 1)
        hbox.addWidget(self.lbl_x_0, 8, 0, 1, 1)
        hbox.addWidget(self.lbl_y_0, 10, 0, 1, 1)

        hbox.addWidget(self.btn_set_step, 4, 1, 1, 1)
        hbox.addWidget(self.btn_reset_step, 5, 0, 1, 2)
        hbox.addWidget(self.btn_set_reg, 6, 1, 1, 1)
        hbox.addWidget(self.btn_reset_reg, 7, 0, 1, 2)
        hbox.addWidget(self.btn_set_x0, 8, 1, 1, 1)
        hbox.addWidget(self.btn_reset_x0, 9, 0, 1, 2)
        hbox.addWidget(self.btn_set_y0, 10, 1, 1, 1)
        hbox.addWidget(self.btn_reset_y0, 11, 0, 1, 2)
        
        #change size of window and show
        self.setGeometry(10, 10, 1000, 600)
        self.show()
    
    #events
    def qt_connections(self):
        self.btn_set_step.clicked.connect(self.on_set_step_event)
        self.btn_reset_step.clicked.connect(self.on_reset_step_event)

        self.btn_set_reg.clicked.connect(self.on_set_reg_event)
        self.btn_reset_reg.clicked.connect(self.on_reset_reg_event)

        self.btn_set_x0.clicked.connect(self.on_set_x0_event)
        self.btn_reset_x0.clicked.connect(self.on_reset_x0_event)

        self.btn_set_y0.clicked.connect(self.on_set_y0_event)
        self.btn_reset_y0.clicked.connect(self.on_reset_y0_event)
    
    #for debug
    def moveplot(self):
        self.t += 1
        self.updateplot()
    
    #--------------------HERE GOES EVENT HANDLERS-----------------------------
    def on_set_step_event(self):
        if not self.lbl_step.text() == "":
            self.step = float(self.lbl_step.text())
        else:
            self.step = 0.1
        self.updateplot()

    def on_reset_step_event(self):
        self.step = 0.1
        self.updateplot()

    def on_set_reg_event(self):
        if not self.lbl_region.text() == "":
            self.X = int(self.lbl_region.text())
        else:
            self.X = 0.1
        self.updateplot()

    def on_reset_reg_event(self):
        self.X = 10
        self.updateplot()

    def on_set_x0_event(self):
        if not self.lbl_x_0.text() == "":
            self.x_0 = float(self.lbl_x_0.text())
            self.c1 = (self.y_0 + self.x_0 - 1) / np.e ** (-self.x_0)
        else:
            self.x_0 = 0
            self.c1 = (self.y_0 + self.x_0 - 1) / np.e ** (-self.x_0)
        self.updateplot()

    def on_reset_x0_event(self):
        self.x_0 = 0
        self.c1 = (self.y_0 + self.x_0 - 1) / np.e ** (-self.x_0)
        self.updateplot()

    def on_set_y0_event(self):
        if not self.lbl_y_0.text() == "":
            self.y_0 = float(self.lbl_y_0.text())
            self.c1 = (self.y_0 + self.x_0 - 1) / np.e ** (-self.x_0)
        else:
            self.y_0 = 1
            self.c1 = (self.y_0 + self.x_0 - 1) / np.e ** (-self.x_0)
        self.updateplot()

    def on_reset_y0_event(self):
        self.y_0 = 1
        self.c1 = (self.y_0 + self.x_0 - 1) / np.e ** (-self.x_0)
        self.updateplot()
    #----------------------END OF EVENT HANDLERS-------------------------------
    
    #update plots
    def updateplot(self):
        #set region and step for x axis
        self.x_axis = np.arange(self.x_0, self.X + self.step, self.step, float)
        
        #calculate y values for num methods
        data_1, err_1 = self.euler()
        data_2, err_2 = self.adv_euler()
        data_3, err_3 = self.runge_kutta_mon()
        
        #calculate exact solution
        data_4 = self.plot_exact()
        
        #update plots for first graph (mehods)
        self.plotcurve_euler.setData(x=self.x_axis, y=data_1)
        self.plotcurve_adv_euler.setData(x=self.x_axis, y=data_2)
        self.plotcurve_runge_kutt.setData(x=self.x_axis, y=data_3)
        
        #update plots for second graph (errors)
        self.plotcurve_err_euler.setData(x=self.x_axis, y=err_1)
        self.plotcurve_err_adv_euler.setData(x=self.x_axis, y=err_2)
        self.plotcurve_err_runge_kutt.setData(x=self.x_axis, y=err_3)
        
        #update plot of exact
        self.plotcurve_ex.setData(x=self.x_axis, y=data_4)

    # ////////////////MATH GOES FROM HERE////////////////////////////////////////////////////////
    
    #return function y`=f(x,y)
    def func(self, x, y):
        return -y - x
    
    #return exact value
    def exact(self, x):
        return self.c1 * np.e ** (-x) - x + 1
    
    #return y values for exact
    def plot_exact(self):
        #init y field
        y_axis = np.zeros(len(self.x_axis), dtype=float)

        counter = 0
        
        #fill with exact values for each x
        for x in self.x_axis:
            y_axis[counter] = self.exact(x)
            counter += 1

        return y_axis
    
    #return values of Euler's method and errors
    def euler(self):
        #init y fields
        y_axis = np.zeros(len(self.x_axis), dtype=float)
        err_axis = np.zeros(len(self.x_axis), dtype=float)
        
        y_axis[0] = self.y_0

        counter = 1
        
        #calculating y's with Euler method, comparing with exact
        for x in self.x_axis[1:]:
            #y[n]
            y_axis[counter] = y_axis[counter - 1] + self.step * self.func(self.x_axis[counter - 1], y_axis[counter - 1])
            #error
            err_axis[counter] = self.exact(self.x_axis[counter]) - y_axis[counter]
            counter += 1

        return y_axis, err_axis
    
    #return y values for improved Euler's method and errors
    def adv_euler(self):
        #init y fields
        y_axis = np.zeros(len(self.x_axis), dtype=float)
        err_axis = np.zeros(len(self.x_axis), dtype=float)

        y_axis[0] = self.y_0

        counter = 1
        
        #calculating y's with imp. Euler's method, comparing with exact
        for x in self.x_axis[1:]:
            #y's from formula
            y_axis[counter] = y_axis[counter - 1] + self.step * self.func(self.x_axis[counter - 1] + self.step / 2,
                                                                          y_axis[counter - 1] + self.step / 2 *
                                                                          self.func(self.x_axis[counter - 1],
                                                                                    y_axis[counter - 1]))
            #error
            err_axis[counter] = self.exact(self.x_axis[counter]) - y_axis[counter]
            counter += 1

        return y_axis, err_axis
    
    #delta y for RK formula, too big to include in calc method itself
    def delta_y_runga(self, x, y):
        k_1 = self.func(x, y)
        k_2 = self.func(x + self.step / 2, y + self.step * k_1 / 2)
        k_3 = self.func(x + self.step / 2, y + self.step * k_2 / 2)
        k_4 = self.func(x + self.step, y + self.step * k_3)
        return self.step / 6 * (k_1 + 2 * k_2 + 2 * k_3 + k_4)
    
    #return y values with Runge-Kutta's method and errors
    def runge_kutta_mon(self):
        #init y fields
        y_axis = np.zeros(len(self.x_axis), dtype=float)
        err_axis = np.zeros(len(self.x_axis), dtype=float)

        y_axis[0] = self.y_0

        counter = 1
        
        #calculate y's, compare with exact
        for x in self.x_axis[1:]:
            #formula, calculating delta y with separate method
            y_axis[counter] = y_axis[counter - 1] + self.delta_y_runga(self.x_axis[counter - 1], y_axis[counter - 1])
            #error
            err_axis[counter] = self.exact(self.x_axis[counter]) - y_axis[counter]
            counter += 1

        return y_axis, err_axis


# ////////////////END/////////////////////////////////

def main():
    app = qw.QApplication([])
    app.setApplicationName('Numerical methods')
    ex = num_methods()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
