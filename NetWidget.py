from PySide2.QtMultimedia import QSound

from BaseWidget import BaseWidget,Chessman
from PySide2.QtWidgets import QMessageBox


class NetWidget(BaseWidget):
    def __init__(self,net):
        super(NetWidget, self).__init__()
        self.setWindowTitle("联网对战")
        self.net = net
        self.selfColor = Chessman.Black

        self.net.recvslot.connect(self.processSlot)

    def mousePressEvent(self, event):
        if self.selfColor != self.currentColor:return
        len1 = len(self.record)
        super(NetWidget, self).mousePressEvent(event)
        len2 = len(self.record)
        if len2 <= len1:return

        chess = self.record[-1]
        data = {
            "req_type":"position",
            "args":{
                "xi":chess.xi,
                "yi":chess.yi
            }
        }
        self.net.send(data)


    def startbtnSlot(self):
        # 发送询问给对方
        data = {
            "req_type":"startReq"
        }
        self.net.send(data)


    def regretSlot(self):
        # 发送询问给对方
        if self.startFlag == False: return
        if self.selfColor != self.currentColor: return
        data = {
            "req_type":"huiqi"
        }
        self.net.send(data)

    def fastSlot(self):
        # 发送询问给对方
        if self.startFlag == False :return
        data = {
            "req_type":"cuicu"
        }
        self.net.send(data)


    def giveupSlot(self):
        # 发送询问给对方
        if self.selfColor == self.currentColor:
            data = {
                "req_type":"renshu"
            }
            self.net.send(data)
            super().giveupSlot()


    def processSlot(self,data):
        func_map = {
            "startReq":self.startReqProcess,
            "startReqResult":self.startReqResultProcess,
            "position":self.positionProcess,
            "huiqi":self.huiqiProcess,
            "huiqigame":self.huiqigameProcess,
            "cuicu":self.cuicugameProcess,
            "renshu":self.renshugameProcess
        }
        req_type = data.get("req_type",None)
        if req_type is None:return
        func = func_map.get(req_type,None)
        args = data.get("args",{})
        if func:
            func(args)


    def startReqProcess(self,args):
        res = QMessageBox.question(self,"收到请求","收到开始游戏请求，是否开始？",
                                   QMessageBox.Ok,QMessageBox.No)
        if res == QMessageBox.Ok:
            data = {
                "req_type":"startReqResult",
                "args":{
                    "result":"success",
                    "msg":"同意开始游戏"
                }
            }
            self.net.send(data)
            super().startbtnSlot()
            self.selfColor = Chessman.White

        else:
            data = {
                "req_type": "startReqResult",
                "args": {
                    "result": "error",
                    "msg": "不想和你玩"
                }
            }
            self.net.send(data)


    def huiqiProcess(self,args):
        res = QMessageBox.question(self,"收到请求","收到悔棋请求，是否同意？",
                                   QMessageBox.Ok,QMessageBox.No)
        if res == QMessageBox.Ok:
            data = {
                "req_type":"huiqigame",
                "args":{
                    "result":"success",
                    "msg":"同意悔棋"
                }
            }
            self.net.send(data)
            super().regretSlot()
            self.selfColor = Chessman.White

        else:
            data = {
                "req_type": "huiqigame",
                "args": {
                    "result": "error",
                    "msg": "不同意悔棋"
                }
            }
            self.net.send(data)

    def startReqResultProcess(self,args):
        result = args.get("result",None)
        msg = args.get("msg","")
        if result == "success":
            QMessageBox.information(self,"收到回复","对方同意！",QMessageBox.Ok)
            super().startbtnSlot()
        else:
            QMessageBox.information(self, "收到回复", f"对方拒绝！{msg}。", QMessageBox.Ok)


    def positionProcess(self,args):
        xi = args.get('xi')
        yi = args.get('yi')
        color = Chessman.changeColor(self.selfColor)
        x = 28+40*xi-18
        y = 28+40*yi-18
        chess = Chessman(color,x,y,self)
        self.chessboard[yi][xi] = chess
        self.record.append(chess)
        chess.show()
        if self.isWin(chess):
            self.gameover()
        else:
            self.currentColor = Chessman.changeColor(self.currentColor)


    def huiqigameProcess(self,args):
        result = args.get("result", None)
        msg = args.get("msg", "")
        if result == "success":
            QMessageBox.information(self, "收到回复", "对方同意！", QMessageBox.Ok)
            super().regretSlot()
        else:
            QMessageBox.information(self, "收到回复", f"对方拒绝！{msg}。", QMessageBox.Ok)


    def cuicugameProcess(self):
        QSound.play('./123/cuicu.wav')

    def renshugameProcess(self,args):
        if self.startFlag != False:
            if self.currentColor == Chessman.Black:
                self.whiteWinLable.show()
            else:
                self.blackWinLable.show()
            self.startFlag = False