import threading
from ipc import MyIPC
MyDebugMode = True


class ListenThread(threading.Thread):

    def __init__(self, nodeID=None, message_handle=None, threadID=None, threadType='main'):
        super(ListenThread, self).__init__()
        self.nodeID = nodeID
        self.message_handle = message_handle
        self.ipc = MyIPC(self.nodeID)
        self.threadID = threadID
        self.threadType = threadType

    def run(self):
        while True:
            try:
                msg = self.ipc.receive()
                if MyDebugMode is True:
                    print("{} {} recv: {}".format(
                        self.threadType, self.threadID, msg))
            except Exception as err:
                print(('IPC Recv Error: {}'.format(err)))
            else:
                self.message_handle(msg, self.ipc)
