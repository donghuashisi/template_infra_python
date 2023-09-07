from queue import Queue
from mythread import ListenThread
import threading
import time

MAIN_NODE = 20000
CLIENT_NODE = 20000 - 1
CHILD_NODE = 30000


class workerThread(threading.Thread):

    def __init__(self, messageQueue=None):
        super(workerThread, self).__init__()
        self.messageQueue = messageQueue

    def run(self):
        while True:
            self.messageQueue.put("my_worker")
            time.sleep(10)
            # try:
            #     msg = self.ipc.receive()
            #     self.message_handle(msg, self.ipc)
            #     # self.shareQ.put(msg)
            # except Exception as err:
            #     print(('IPC receive Error: {}'.format(err)))


def message_handle(msg, ipc):
    global q
    if msg == 'hello_child':
        message = q.get()
        ipc.send(message, MAIN_NODE)
        q.task_done()


def childMain(nodeID):
    global q
    q = Queue()
    ipcThread = ListenThread(nodeID, message_handle,
                             threadID=nodeID, threadType='child')
    ipcThread.setDaemon(True)
    ipcThread.start()
    worker = workerThread(q)
    worker.start()
