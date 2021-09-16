from PySide2.QtWidgets import QApplication
from BaseWidget import BaseWidget,Chessman
import sys

class SingleWideget(BaseWidget):
    def __init__(self):
        super(SingleWideget,self).__init__()
        self.setWindowTitle("人机对战")

    def mousePressEvent(self, event):
        len1 = len(self.record)
        super(SingleWideget,self).mousePressEvent(event)
        len2 = len(self.record)
        if len2 > len1:
            self.autoPlay()


    def autoPlay(self):
        if self.startFlag == False:return
        score_list = []
        for y in range(15):
            for x in range(15):
                if self.chessboard[y][x] == None:
                    s1 = self.getScore(x,y,Chessman.Black)
                    s2 = self.getScore(x,y,Chessman.White)
                    s = max(s1,s2)
                    score_list.append(s)
                else:
                    score_list.append(0)

        value = max(*score_list)
        index = score_list.index(value)
        yi = index // 15
        xi = index % 15
        x = 28 + 40*xi - 18
        y = 28 + 40*yi - 18

        chess = Chessman(self.currentColor, x, y, self)
        self.chessboard[chess.yi][chess.xi] = chess
        self.record.append(chess)
        chess.show()
        # 判断输赢
        if self.isWin(chess):
            self.gameover()
        else:
            self.currentColor = Chessman.changeColor(self.currentColor)


    def getScore(self, x, y, color):
        # 统计四个方向相同棋子数量
        tmp = [0, 0, 0, 0]
        # 横向
        # 横向 左
        for i in range(1, 5):
            if x - i < 0: break
            if (not self.chessboard[y][x - i] is None) and self.chessboard[y][x - i].color == color:
                tmp[0] += 1
            else:
                break
        for i in range(1, 5):
            if x + i > 14: break
            if (not self.chessboard[y][x + i] is None) and self.chessboard[y][x + i].color == color:
                tmp[0] += 1
            else:
                break
        # 纵向
        for i in range(1, 5):
            if y - i < 0: break
            if (not self.chessboard[y - i][x] is None) and self.chessboard[y - i][x].color == color:
                tmp[1] += 1
            else:
                break
        for i in range(1, 5):
            if y + i > 14: break
            if (not self.chessboard[y + i][x] is None) and self.chessboard[y + i][x].color == color:
                tmp[1] += 1
            else:
                break
        #  斜上 左 x-i,y+i  右 x+i,y-i
        for i in range(1, 5):
            if x - i < 0 or y + i > 14: break
            if (not self.chessboard[y + i][x - i] is None) and self.chessboard[y + i][x - i].color == color:
                tmp[2] += 1
            else:
                break
        for i in range(1, 5):
            if x + i > 14 or y - i < 0: break
            if (not self.chessboard[y - i][x + i] is None) and self.chessboard[y - i][x + i].color == color:
                tmp[2] += 1
            else:
                break

        # 斜下 左 x-i,y-i  右 x+i,y+i
        for i in range(1, 5):
            if x - i < 0 or y - i < 0: break
            if (not self.chessboard[y - i][x - i] is None) and self.chessboard[y - i][x - i].color == color:
                tmp[3] += 1
            else:
                break
        for i in range(1, 5):
            if x + i > 14 or y + i > 14: break
            if (not self.chessboard[y + i][x + i] is None) and self.chessboard[y + i][x + i].color == color:
                tmp[3] += 1
            else:
                break

        return max(tmp)
if __name__ =="__main__":
    app =QApplication()
    wg = SingleWideget()
    wg.show()
    sys.exit(app.exec_())