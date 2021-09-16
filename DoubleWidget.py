from PySide2.QtWidgets import QApplication
from BaseWidget import BaseWidget
import sys

class DoubleWideget(BaseWidget):
    def __init__(self):
        super(DoubleWideget,self).__init__()
        self.setWindowTitle("双人对战")


if __name__ =="__main__":
    app =QApplication()
    wg = DoubleWideget()
    wg.show()
    sys.exit(app.exec_())