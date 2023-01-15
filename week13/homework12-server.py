import time
import queue
from socket import *
from threading import Thread, Lock

RSIZE = 1024

server_path = 'E:\\BUAA\\大三上\\程设\\week13\\server.txt'

lock = Lock()

class ChatManager:
    def __init__(self, ip, port, max_connection):
        self._server = socket(AF_INET, SOCK_STREAM)
        self._ip = ip
        self._port = port
        self._maxconnection = max_connection
        print("SERVER is listening on %s" % port)
        self._users = []
        self._messages = queue.Queue()

    def load(self, data, user, flag, to_user):
        lock.acquire()
        self._messages.put((data, user, flag, to_user))
        lock.release()

    def receive_message(self, conn, addr):
        user_name = conn.recv(RSIZE).decode(encoding='utf-8')
        self._users.append((user_name, conn))

        try:
            f = open(server_path, 'a')
            while True:
                message = conn.recv(RSIZE).decode(encoding='utf-8')
                print('\n' + user_name + ': ' + message)
                f.write(time.strftime('%X') + '\t' + user_name + ': ' + message + '\n')
                flag = 0
                to_user = ''
                if message.split()[0] == '@':
                    flag = 1
                    to_user = message.split()[1]
                self.load(message, user_name, flag, to_user)
            f.close()
            conn.close()
        except:
            self._users.remove(user_name)

    def send_message(self):
        while True:
            if not self._messages.empty():
                message = self._messages.get()
                for user in self._users:
                    if message[2]:   #如果有@, 定向转发
                        if user[0] == message[3]:
                            msg_to_send = message[1] + ': ' + message[0]
                            user[1].send(msg_to_send.encode())
                    else:
                        if user[0] != message[1]:
                            msg_to_send = message[1] + ': ' + message[0]
                            user[1].send(msg_to_send.encode())
    
    def serve(self):
        self._server.setsockopt(SOL_SOCKET, SO_REUSEADDR, True)
        self._server.bind((self._ip, self._port))
        self._server.listen(self._maxconnection)

        p = Thread(target=self.send_message)
        p.start()
        while True:
            conn, addr = self._server.accept()
            print(f"client's connection: {conn}, address:{addr}")
            t = Thread(target=self.receive_message, args=(conn, addr))
            t.start()
        self._server.close()

if __name__ == '__main__':
    ip = '127.0.0.1'
    port = 8080
    max_connection = 10

    manager = ChatManager(ip, port, max_connection)
    manager.serve()