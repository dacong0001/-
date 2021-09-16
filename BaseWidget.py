from PySide2.QtMultimedia import QSound
from PySide2.QtWidgets import QApplication,QWidget,QLabel
from PySide2.QtGui import QPixmap, QPalette, QBrush, QImage, QIcon
from MyButton import Mybutton
from PySide2.QtCore import Signal
import sys

class Chessman(QLabel):
    Black = True
    White = False
    def __init__(self,color,x,y,parent=None):
        super().__init__(parent=parent)
        self.xi=(x-8)//40
        self.yi=(y-8)//40
        self.x=28+40*self.xi-18
        self.y=28+40*self.yi-18
        self.color=color
        QSound.play('./123/luozisheng.wav')
        if color == self.Black:
            self.setPixmap(QPixmap("./123/黑子.png"))
        else:
            self.setPixmap(QPixmap("./123/白子.png"))

        self.setFixedSize(QPixmap("./123/黑子.png").size())

    def show(self):
        self.move(self.x, self.y)
        super().show()

    @staticmethod
    def changeColor(color):
        return not color


class BaseWidget(QWidget):
    back = Signal()
    def __init__(self):
        super(BaseWidget,self).__init__()

        p = QPalette(self.palette())
        b = QBrush(QImage("./123/游戏界面.png"))
        self.setWindowTitle("五子棋游戏")
        self.setWindowIcon(QIcon('./123/icon.ico'))
        p.setBrush(QPalette.Background, b)
        self.setPalette(p)
        self.setFixedSize(QImage("./123/游戏界面.png").size())

        self.startbtn = Mybutton("./123/开始1.png",
                                 "./123/开始3.png",
                                 "./123/开始2.png", self)
        self.giveupbtn = Mybutton("./123/认输1.png",
                                 "./123/认输3.png",
                                 "./123/认输2", self)
        self.regretbtn = Mybutton("./123/悔棋1.png",
                                 "./123/悔棋3.png",
                                 "./123/悔棋2.png", self)
        self.returnbtn = Mybutton("./123/返回1.png",
                                 "./123/返回3.png",
                                 "./123/返回2.png", self)
        self.fastbtn = Mybutton("./123/催促1.png",
                                 "./123/催促3.png",
                                 "./123/催促2", self)
        self.startbtn.move(640,170)
        self.giveupbtn.move(640,310)
        self.regretbtn.move(640, 240)
        self.returnbtn.move(650, 500)
        self.fastbtn.move(640, 380)

        self.blackWinLable = QLabel(self)
        self.whiteWinLable = QLabel(self)
        self.blackWinLable.setPixmap("./123/黑棋胜利.png")
        self.whiteWinLable.setPixmap("./123/白棋胜利.png")
        self.blackWinLable.hide()
        self.whiteWinLable.hide()

        self.startFlag = False
        self.chessboard =[[None for x in range(15)] for y in range(15)]
        self.record = []
        self.currentColor = Chessman.Black

        self.startbtn.clicked.connect(self.startbtnSlot)
        self.giveupbtn.clicked.connect(self.giveupSlot)
        self.regretbtn.clicked.connect(self.regretSlot)
        self.returnbtn.clicked.connect(self.returnSlot)
        self.fastbtn.clicked.connect(self.fastSlot)

    def startbtnSlot(self):
        self.startFlag = True
        self.chessboard = [[None for x in range(15)] for y in range(15)]
        for c in self.record:
            c.close()
            del c
        self.record = []
        self.currentColor = Chessman.Black
        self.blackWinLable.hide()
        self.whiteWinLable.hide()

    def mousePressEvent(self, event):
        if self.startFlag == False: return


        x, y = event.x(), event.y()
        # 创建棋子
        chess = Chessman(self.currentColor, x, y, self)
        # 检查边界
        if chess.xi < 0 or chess.xi > 14 or chess.yi < 0 or chess.yi > 14: return
        # 判断该位置是否为空，该位置没有棋子时才可以下棋
        if not self.chessboard[chess.yi][chess.xi] is None: return

        # 添加记录在棋盘数组中
        self.chessboard[chess.yi][chess.xi] = chess
        # 添加记录到数组中，记录下棋顺序
        self.record.append(chess)
        chess.show()
        if self.isWin(chess):
            # 如果赢了，游戏结束，显示提示
            self.gameover()
        else:
            # 没有赢的话继续下去，切换棋子颜色
            self.currentColor = Chessman.changeColor(self.currentColor)

    def isWin(self,chess):
        x,y,color = chess.xi,chess.yi,chess.color
        count = 1
        #横向
        for i in range(1,5):
            if x-i< 0 :break
            if  (not self.chessboard[y][x - i] is None) and self.chessboard[y][x - i].color == color :
                count+=1
            else:
                break
        for i in range(1,5):
            if x + i > 14: break
            if (not self.chessboard[y][x + i] is None) and self.chessboard[y][x + i].color ==color :
                count += 1
            else:
                break
        if count >=5 :
            return True
        count = 1
        #纵向
        for i in range(1, 5):
            if y - i < 0: break
            if (not self.chessboard[y - i][x] is None) and self.chessboard[y - i][x].color == color:
                count += 1
            else:
                break
        for i in range(1, 5):
            if y + i > 14: break
            if (not self.chessboard[y + i][x] is None) and self.chessboard[y + i][x].color == color:
                count += 1
            else:
                break
        if count >= 5:
            return True
        count = 1
        #斜上
        for i in range(1, 5):
            if y - i < 0 or  x + i > 14: break
            if (not self.chessboard[y - i][x + i] is None) and self.chessboard[y - i][x + i].color == color:
                count += 1
            else:
                break
        for i in range(1, 5):
            if y + i > 14 or x - i <0: break
            if (not self.chessboard[y + i][x - i] is None) and self.chessboard[y + i][x - i].color == color:
                count += 1
            else:
                break
        if count >= 5:
            return True
        count = 1
        #斜下
        for i in range(1, 5):
            if y - i < 0 and x - i < 0: break
            if (not self.chessboard[y - i][x - i] is None) and self.chessboard[y - i][x - i].color == color:
                count += 1
            else:
                break
        for i in range(1, 5):
            if y + i > 14 or x + i > 14: break
            if (not self.chessboard[y + i][x + i] is None) and self.chessboard[y + i][x + i].color == color:
                count += 1
            else:
                break
        if count >= 5:
            return True


    def gameover(self):
        if self.currentColor == Chessman.Black:
            self.blackWinLable.show()
        else:
            self.whiteWinLable.show()
        self.startFlag = False

    def regretSlot(self):
        if self.startFlag != False:
            if len(self.record)>2:
                c1 = self.record.pop(-1)
                c1.close()
                self.chessboard[c1.yi][c1.xi]=None
                del c1
                c2 = self.record.pop(-1)
                c2.close()
                self.chessboard[c2.yi][c2.xi]=None
                del c2
    def giveupSlot(self):
        if self.startFlag != False:
            if self.currentColor == Chessman.Black:
                self.whiteWinLable.show()
            else:
                self.blackWinLable.show()
            self.startFlag = False

    def returnSlot(self):
        self.back.emit()

    def fastSlot(self):
        QSound.play('./123/cuicu.wav')

if __name__ == '__main__':
    app=QApplication()
    wg = BaseWidget()
    wg.show()
    sys.exit(app.exec_())