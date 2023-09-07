import atexit
import threading
from ipc import MyIPC
import fcntl
import os
import json
import socket
import errno
from time import sleep

MAIN_NODE = 20000
CLIENT_NODE = 20000 - 1


class Singleton(object):

    def __init__(self, cls):
        self._cls = cls
        self._instance = {}

    def __call__(self, *args, **kw):
        if self._cls not in self._instance:
            self._instance[self._cls] = self._cls(*args, **kw)
        return self._instance[self._cls]


def once_print():
    print("I have been lanuched")


def always_do():
    print("I will be called anyway")


@Singleton
class MyClient(object):

    def __init__(self, name):
        once_print()
        self.ipc = MyIPC(CLIENT_NODE)
        self.sock = self.ipc.sock
        fcntl.fcntl(self.sock, fcntl.F_SETFL, os.O_NONBLOCK)

    def cleanup(self):
        always_do()

    def recv(self):
        while True:
            try:
                msg = self.sock.recv(10000)
            except socket.error as e:
                err = e.args[0]
                if err == errno.EAGAIN or err == errno.EWOULDBLOCK:
                    sleep(0.1)
                    continue
                else:
                    sys.exit(1)
            else:
                res = json.loads(msg.decode())
                print("Client recv:{}".format(res))
                return res

    def send(self, payload, nodeID=None):
        if nodeID is None:
            nodeID = MAIN_NODE
        self.ipc.send(payload, nodeID)

    def demo_test(self, payload='client'):
        self.send(payload)
        return self.recv()


def cgt_clean(instance):
    instance.cleanup()


alwaysMe = MyClient("test")
atexit.register(cgt_clean, alwaysMe)


if __name__ == '__main__':
    ins1 = MyClient("test1")
    import pdb
    pdb.set_trace()
    ins1.demo_test()
    # ins2 = MyClient("test2")
    # import pdb
    # pdb.set_trace()
