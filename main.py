import multiprocessing as mp
import json
import os
import re
import time
import threading
from queue import Queue
from ipc import MyIPC
from child import childMain
from mythread import ListenThread


MAIN_NODE = 20000
CLIENT_NODE = 20000 - 1
CHILD_NODE = 30000


CHILD_LIST = []


def add_child_process(nodeID):
    subProcess = mp.Process(
        target=childMain,
        args=(
            nodeID,
        ),
    )
    subProcess.daemon = True
    subProcess.start()


def message_handle(msg, ipc):
    global CHILD_NODE
    if msg == 'hello':
        ipc.send("received: hello", CLIENT_NODE)

    elif msg == 'add_child':
        add_child_process(CHILD_NODE)
        CHILD_LIST.append(CHILD_NODE)
        CHILD_NODE = CHILD_NODE + 1
        ipc.send("received", CLIENT_NODE)

    elif msg == 'hello_child':
        for a_child in CHILD_LIST:
            ipc.send("hello_child", a_child)
        ipc.send("received", CLIENT_NODE)

    elif msg == 'my_worker':
        ipc.send("received", CLIENT_NODE)

    else:
        ipc.send("Error Command!", CLIENT_NODE)


def Main():
    recv_thread = ListenThread(MAIN_NODE, message_handle)
    recv_thread.setDaemon(True)
    recv_thread.start()
    recv_thread.join()


if __name__ == '__main__':
    Main()
