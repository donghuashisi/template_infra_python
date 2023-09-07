import socket
import json

LOCAL_HOST = '127.0.0.1'


class MyIPC:

    def __init__(self, nodeID):
        super(MyIPC, self).__init__()
        self.nodeID = nodeID
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((LOCAL_HOST, self.nodeID))

    def send(self, msg, nodeID):
        str_json = json.dumps(msg)
        try:
            self.sock.sendto(str_json.encode(), (LOCAL_HOST, nodeID))
        except socket.error as err:
            print(('Failed to send message: {}'.format(err)))

    # def sendall(self, msg, type, nodes=None):
    #     # print("Send Process {} {} to {} {}: msg {}".format(self.type, self.node, type, nodes, msg))
    #     str_json = json.dumps(msg)
    #     if nodes is None:
    #         try:
    #             self.sock.sendto(str_json.encode(),
    #                              (socket.TIPC_ADDR_NAMESEQ, type, 0, ~0))
    #         except socket.error as err:
    #             print(('Failed to send message: {}'.format(err)))
    #     else:
    #         for a_node in nodes:
    #             try:
    #                 self.sock.sendto(str_json.encode(), (LOCAL_HOST, a_node))
    #             except socket.error as err:
    #                 print(('Failed to send message: {}'.format(err)))

    def receive(self, number=100000):
        try:
            msg = self.sock.recv(number).decode()
        except socket.error as err:
            print(('Failed to receive message: {}'.format(err)))
        res = json.loads(msg)
        return res

    def close(self):
        self.sock.close()
