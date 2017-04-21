#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore

class Communicate(QtCore.QObject):
    
    updateBW = QtCore.pyqtSignal(int)


class BurningWidget(QtGui.QWidget):
  
    def __init__(self):      
        super(BurningWidget, self).__init__()
        
        self.initUI()
        
    def initUI(self):
        
        self.setMinimumSize(100, 100)
        self.value = 100


    def setValue(self, value):

        self.value = value


    def paintEvent(self, e):
      
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawWidget(qp)
        qp.end()
      
      
    def drawWidget(self, qp):
      
        # font = QtGui.QFont('Serif', 7, QtGui.QFont.Light)
        # qp.setFont(font)

        size = self.size()
        w = size.width()
        h = size.height()

        recx = 20
        recy = recx

        max_r = min(w,h)//2

        radius = max_r*self.value//100

        qp.setPen(QtCore.Qt.NoPen);

        x_start = (w//2) % recx #+ recx//2
        y_start = (h//2) % recy #+ recy//2


        for y in range(y_start, h, recy):
            for x in range(x_start, w, recx):
                if (x-w//2)**2 + (y-h//2)**2 < max(0,radius-+ recx//2)**2:
                    qp.setBrush(QtCore.Qt.blue)
                else:
                    qp.setBrush(QtCore.Qt.gray)
                qp.drawRect(x - recx//2 + 1, y - recy//2 + 1, recx - 2, recy - 2)


        circle_path = QtGui.QPainterPath()
        circle_path.addEllipse(w//2 - radius, h//2 - radius, radius*2, radius*2);

        circle_pen = QtGui.QPen(QtCore.Qt.green)
        circle_pen.setWidth(3)
        qp.setPen(circle_pen)
        qp.setBrush(QtCore.Qt.NoBrush)
        qp.drawPath(circle_path)




class CircleWindow(QtGui.QWidget):
    
    def __init__(self):
        super(CircleWindow, self).__init__()
        
        self.initUI()
        
        
    def initUI(self):
        
        self.setGeometry(400, 300, 600, 600)
        self.setWindowTitle('Circle!')
        self.setWindowIcon(QtGui.QIcon('circle.png'))   

        vbox = QtGui.QVBoxLayout()

        self.c = Communicate()        
        self.wid = BurningWidget()

        vbox.addWidget(self.wid,1)

        sld = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        vbox.addWidget(sld)

        self.c.updateBW[int].connect(self.wid.setValue)

        sld.valueChanged[int].connect(self.changeValue)

        qbtn = QtGui.QPushButton('Quit', self)
        qbtn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())

        vbox.addWidget(qbtn)
        
        self.setLayout(vbox)    

        sld.setValue(50)

        self.show()

    def changeValue(self, value):
             
        self.c.updateBW.emit(value)        
        self.wid.repaint()

def main():

    app = QtGui.QApplication(sys.argv)

    cw = CircleWindow()

    sys.exit(app.exec_())





if __name__ == '__main__':
    main()