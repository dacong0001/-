# 实现看客户端类、 服务器类，提供给其他模块使用

from PySide2.QtCore import QObject,Signal
import threading
import socket
import json


class NetServer(QObject):

    recvslot = Signal(dict)
    errorslot = Signal(str)

    def __init__(self,ip,port):
        super(NetServer, self).__init__()
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.bind((ip,port))
        self.socket.listen(1)
        self.sock = None
        self.runFlag = True

    def start(self):
        self.th = threading.Thread(target=self.recv, args=())
        self.th.start()

    def recv(self):
        sock, addr = self.socket.accept()
        self.sock = sock
        try:
            while True:
                if self.runFlag == False: return
                data = self.sock.recv(4096)
                if data:
                    data = json.loads(data.decode())
                    self.recvslot.emit(data)  # dict
        except Exception as e:
            self.errorslot.emit(str(e))
            self.socket.close()


    def send(self,data):
        try:
            data = json.dumps(data).encode()
            self.sock.send(data)
        except Exception as e:
            self.errorslot.emit(str(e))
            self.socket.close()


class NetClinet(QObject):

    recvslot = Signal(dict)
    errorslot = Signal(str)

    def __init__(self,ip,port):
        super(NetClinet, self).__init__()
        self.ip = ip
        self.port = port
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.runFlag = True

    def start(self):
        try:
            self.socket.connect((self.ip,self.port))
        except Exception as e:
            self.errorslot.emit(str(e))
            self.runFlag = False
            return

        self.th = threading.Thread(target=self.recv,args=())
        self.th.start()


    def recv(self):
        try:
            while True:
                if self.runFlag == False: return
                data = self.socket.recv(4096)
                if data:
                    data = json.loads(data.decode())
                    self.recvslot.emit(data)
        except Exception as e:
            self.errorslot.emit(str(e))
            self.runFlag = False
            self.socket.close()

    def send(self,data):
        try:
            data = json.dumps(data).encode()
            self.socket.send(data)
        except Exception as e:
            self.runFlag = False
            self.errorslot.emit(str(e))
            self.socket.close()


