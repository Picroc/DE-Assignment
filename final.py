import sys
from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui, QtCore, Qt
import numpy as np
import pyqtgraph as pg


class num_methods(qw.QWidget):

    def __init__(self):
        super(num_methods, self).__init__()
        self.x_0 = 0
        self.y_0 = 1
        self.step = 0.1
        self.c1 = (self.y_0 + self.x_0 - 1) / np.e ** (-self.x_0)

        self.X = 10

        self.x_axis = np.arange(self.x_0, self.X + self.step, self.step, float)

        self.t = 0

        self.init_ui()
        self.qt_connections()
        self.plotcurve_euler = pg.PlotCurveItem(name='...Euler', pen=(255, 0, 0))
        self.plotcurve_adv_euler = pg.PlotCurveItem(name='..Improved Euler', pen=(0, 255, 0))
        self.plotcurve_runge_kutt = pg.PlotCurveItem(name='...Runge-Kutta', pen=(0, 0, 255))
        self.plotcurve_err_euler = pg.PlotCurveItem(name='...Euler', pen=(255, 0, 0))
        self.plotcurve_err_adv_euler = pg.PlotCurveItem(name='..Improved Euler', pen=(0, 255, 0))
        self.plotcurve_err_runge_kutt = pg.PlotCurveItem(name='...Runge-Kutta', pen=(0, 0, 255))
        self.plotcurve_ex = pg.PlotCurveItem(name='..Exact')

        self.plotwidget.addItem(self.plotcurve_euler)
        self.plotwidget.addItem(self.plotcurve_adv_euler)
        self.plotwidget.addItem(self.plotcurve_runge_kutt)

        self.plotwidget_err.addItem(self.plotcurve_err_euler)
        self.plotwidget_err.addItem(self.plotcurve_err_adv_euler)
        self.plotwidget_err.addItem(self.plotcurve_err_runge_kutt)

        self.plotwidget_ex.addItem(self.plotcurve_ex)

        self.updateplot()

        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.moveplot)
        self.timer.start(500)

    def init_ui(self):
        self.setWindowTitle('Numerical methods')
        hbox = qw.QGridLayout()
        self.setLayout(hbox)

        self.plotwidget = pg.PlotWidget()
        self.plotwidget.addLegend()
        self.plotwidget.showGrid(x=True, y=True, alpha=0.3)
        hbox.addWidget(self.plotwidget, 0, 0, 3, 3)

        self.plotwidget_err = pg.PlotWidget()
        self.plotwidget_err.setRange(yRange=[0.0001, 20])
        self.plotwidget_err.addLegend()
        self.plotwidget_err.showGrid(x=True, y=True, alpha=0.3)
        hbox.addWidget(self.plotwidget_err, 0, 4, 3, 3)

        self.plotwidget_ex = pg.PlotWidget()
        self.plotwidget_ex.addLegend()
        self.plotwidget_ex.showGrid(x=True, y=True, alpha=0.3)
        hbox.addWidget(self.plotwidget_ex, 4, 4, 8, 3)

        self.btn_set_step = qw.QPushButton('Set step')
        self.btn_set_reg = qw.QPushButton('Set region')
        self.btn_set_x0 = qw.QPushButton('Set x0')
        self.btn_set_y0 = qw.QPushButton('Set y0')

        self.btn_reset_step = qw.QPushButton('Default (0.1)')
        self.btn_reset_reg = qw.QPushButton('Default (10)')
        self.btn_reset_x0 = qw.QPushButton('Default (0)')
        self.btn_reset_y0 = qw.QPushButton('Default (1)')

        self.lbl_step = qw.QLineEdit('0.1')
        self.lbl_region = qw.QLineEdit('10')
        self.lbl_x_0 = qw.QLineEdit('0')
        self.lbl_y_0 = qw.QLineEdit('1')

        self.onlyDouble = QtGui.QDoubleValidator()
        self.onlyInt = QtGui.QIntValidator()
        locale = QtCore.QLocale(QtCore.QLocale.English)
        self.onlyDouble.setLocale(locale)

        self.lbl_step.setValidator(self.onlyDouble)
        self.lbl_region.setValidator(self.onlyInt)
        self.lbl_x_0.setValidator(self.onlyDouble)
        self.lbl_y_0.setValidator(self.onlyDouble)

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

        self.setGeometry(10, 10, 1000, 600)
        self.show()

    def qt_connections(self):
        self.btn_set_step.clicked.connect(self.on_set_step_event)
        self.btn_reset_step.clicked.connect(self.on_reset_step_event)

        self.btn_set_reg.clicked.connect(self.on_set_reg_event)
        self.btn_reset_reg.clicked.connect(self.on_reset_reg_event)

        self.btn_set_x0.clicked.connect(self.on_set_x0_event)
        self.btn_reset_x0.clicked.connect(self.on_reset_x0_event)

        self.btn_set_y0.clicked.connect(self.on_set_y0_event)
        self.btn_reset_y0.clicked.connect(self.on_reset_y0_event)

    def moveplot(self):
        self.t += 1
        self.updateplot()

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

    def updateplot(self):
        self.x_axis = np.arange(self.x_0, self.X + self.step, self.step, float)

        data_1, err_1 = self.euler()
        data_2, err_2 = self.adv_euler()
        data_3, err_3 = self.runge_kutta_mon()
        data_4 = self.plot_exact()

        self.plotcurve_euler.setData(x=self.x_axis, y=data_1)
        self.plotcurve_adv_euler.setData(x=self.x_axis, y=data_2)
        self.plotcurve_runge_kutt.setData(x=self.x_axis, y=data_3)

        self.plotcurve_err_euler.setData(x=self.x_axis, y=err_1)
        self.plotcurve_err_adv_euler.setData(x=self.x_axis, y=err_2)
        self.plotcurve_err_runge_kutt.setData(x=self.x_axis, y=err_3)

        self.plotcurve_ex.setData(x=self.x_axis, y=data_4)

    # ////////////////MATH GOES FROM HERE////////////////////////////////////////////////////////

    def func(self, x, y):
        return -y - x

    def exact(self, x):
        return self.c1 * np.e ** (-x) - x + 1

    def plot_exact(self):
        y_axis = np.zeros(len(self.x_axis), dtype=float)

        counter = 0

        for x in self.x_axis:
            y_axis[counter] = self.exact(x)
            counter += 1

        return y_axis

    def euler(self):
        y_axis = np.zeros(len(self.x_axis), dtype=float)
        err_axis = np.zeros(len(self.x_axis), dtype=float)

        y_axis[0] = self.y_0

        counter = 1

        for x in self.x_axis[1:]:
            y_axis[counter] = y_axis[counter - 1] + self.step * self.func(self.x_axis[counter - 1], y_axis[counter - 1])
            err_axis[counter] = self.exact(self.x_axis[counter]) - y_axis[counter]
            counter += 1

        return y_axis, err_axis

    def adv_euler(self):
        y_axis = np.zeros(len(self.x_axis), dtype=float)
        err_axis = np.zeros(len(self.x_axis), dtype=float)

        y_axis[0] = self.y_0

        counter = 1

        for x in self.x_axis[1:]:
            y_axis[counter] = y_axis[counter - 1] + self.step * self.func(self.x_axis[counter - 1] + self.step / 2,
                                                                          y_axis[counter - 1] + self.step / 2 *
                                                                          self.func(self.x_axis[counter - 1],
                                                                                    y_axis[counter - 1]))
            err_axis[counter] = self.exact(self.x_axis[counter]) - y_axis[counter]
            counter += 1

        return y_axis, err_axis

    def delta_y_runga(self, x, y):
        k_1 = self.func(x, y)
        k_2 = self.func(x + self.step / 2, y + self.step * k_1 / 2)
        k_3 = self.func(x + self.step / 2, y + self.step * k_2 / 2)
        k_4 = self.func(x + self.step, y + self.step * k_3)
        return self.step / 6 * (k_1 + 2 * k_2 + 2 * k_3 + k_4)

    def runge_kutta_mon(self):
        y_axis = np.zeros(len(self.x_axis), dtype=float)
        err_axis = np.zeros(len(self.x_axis), dtype=float)

        y_axis[0] = self.y_0

        counter = 1

        for x in self.x_axis[1:]:
            y_axis[counter] = y_axis[counter - 1] + self.delta_y_runga(self.x_axis[counter - 1], y_axis[counter - 1])
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
