from PySide2.QtWidgets import  QApplication,QWidget,QPushButton,QLabel
from PySide2.QtGui import QPixmap
from PySide2.QtCore import Signal


class Mybutton(QLabel):
    clicked=Signal()
    def __init__(self,normal,hover,press,parent=None):
        super(Mybutton,self).__init__(parent=parent)
        self.normalPixmap=QPixmap(normal)
        self.enterPixmap=QPixmap(hover)
        self.pressPixmap=QPixmap(press)
        self.setPixmap(self.normalPixmap)
        self.setFixedSize(self.normalPixmap.size())
    def enterEvent(self, event):
        self.setPixmap(self.enterPixmap)

    def leaveEvent(self, event):
        self.setPixmap(self.normalPixmap)

    def mousePressEvent(self, event):
        self.setPixmap(self.pressPixmap)
        self.clicked.emit()
