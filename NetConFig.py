from PySide2.QtWidgets import QApplication,QWidget,QLineEdit,QPushButton,\
    QFormLayout,QVBoxLayout,QHBoxLayout,QMessageBox
from PySide2.QtCore import Signal
from NetWidget import NetWidget
from NetObject import NetServer,NetClinet
from PySide2.QtMultimedia import QSound
import  sys

class NetConfig(QWidget):
    back = Signal()
    def __init__(self):
        super(NetConfig, self).__init__()
        self.ipEidt = QLineEdit("127.0.0.1",self)
        self.portEidt = QLineEdit("8000",self)
        self.serverBtn = QPushButton("服务器",self)
        self.clientBtn = QPushButton("客户端",self)

        f_layout = QFormLayout()
        f_layout.addRow("ip",self.ipEidt)
        f_layout.addRow("port",self.portEidt)

        h_layout = QHBoxLayout()
        h_layout.addWidget(self.serverBtn)
        h_layout.addWidget(self.clientBtn)

        v_layout = QVBoxLayout()
        v_layout.addLayout(f_layout)
        v_layout.addLayout(h_layout)

        self.setLayout(v_layout)

        self.nextWidget = None

        self.serverBtn.clicked.connect(self.serverBtnSlot)
        self.clientBtn.clicked.connect(self.clientBtnSlot)

    def serverBtnSlot(self):
        ip,port = self.ipEidt.text(),int(self.portEidt.text())
        ns = NetServer(ip,port)
        ns.start()
        self.nextWidget = NetWidget(ns)
        self.nextWidget.back.connect(self.backSlot)
        ns.errorslot.connect(self.showErrorSlot)
        self.nextWidget.show()
        self.hide()

    def clientBtnSlot(self):
        ip, port = self.ipEidt.text(), int(self.portEidt.text())
        nc = NetClinet(ip, port)
        nc.start()
        self.nextWidget = NetWidget(nc)
        self.nextWidget.back.connect(self.backSlot)
        nc.errorslot.connect(self.showErrorSlot)
        self.nextWidget.show()
        self.hide()

    def showErrorSlot(self,msg):
        if self.nextWidget:
            self.nextWidget.close()
        self.show()
        QMessageBox.warning(self,"异常",f"发生错误! {msg}!",QMessageBox.Ok)
        self.nextWidget = None

    def backSlot(self):
        if self.nextWidget:
            self.nextWidget.net.socket.close()
            self.nextWidget.close()
            self.nextWidget = None
            self.show()

    def closeEvent(self, event):
        self.back.emit()


if __name__ == "__main__":
    app = QApplication()
    nc = NetConfig()
    nc.show()
    sys.exit(app.exec_())
