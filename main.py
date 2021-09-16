from PySide2.QtGui import QBrush, QPalette, QImage, QIcon
from PySide2.QtWidgets import QWidget,QApplication
from MyButton import Mybutton
import sys
from  SingleWidget import SingleWideget
from  DoubleWidget import DoubleWideget
from NetConFig import NetConfig
class MainWidget(QWidget):
    def __init__(self):
        super(MainWidget, self).__init__()
        p = QPalette(self.palette())
        b = QBrush(QImage("./123/五子棋界面.png"))
        self.setWindowTitle("五子棋游戏")
        self.setWindowIcon(QIcon('./123/icon.ico'))
        p.setBrush(QPalette.Background, b)
        self.setPalette(p)
        self.setFixedSize(QImage("./123/五子棋界面.png").size())
        self.singlebtn = Mybutton("./123/人机对战1.png",
                                 "./123/人机对战2.png",
                                 "./123/人机对战2.png", self)
        self.doublebtn = Mybutton("./123/双人对战1.png",
                                  "./123/双人对战3.png",
                                  "./123/双人对战2.png", self)
        self.webbtn = Mybutton("./123/联机对战1.png",
                                  "./123/联机对战2.png",
                                  "./123/联机对战3.png", self)

        self.singlebtn.move(-50,500)
        self.doublebtn.move(200,500)
        self.webbtn.move(450, 500)

        self.nextWidget = None

        self.singlebtn.clicked.connect(self.singleSlot)
        self.doublebtn.clicked.connect(self.doubleSlot)
        self.webbtn.clicked.connect(self.webSlot)

    def singleSlot(self):
        s = SingleWideget()
        s.show()
        self.nextWidget = s
        self.nextWidget.back.connect(self.backSlot)
        self.hide()


    def doubleSlot(self):
        d = DoubleWideget()
        d.show()
        self.nextWidget = d
        self.nextWidget.back.connect(self.backSlot)
        self.hide()


    def webSlot(self):
        n = NetConfig()
        n.show()
        self.nextWidget = n
        self.nextWidget.back.connect(self.backSlot)
        self.hide()

    def backSlot(self):
        self.nextWidget.close()
        self.nextWidget = None
        self.show()





if __name__ == "__main__":
    app = QApplication()
    mw = MainWidget()
    mw.show()
    sys.exit(app.exec_())