from socket import *
from threading import Thread

RSIZE = 1024

class Chatter:
    def __init__(self, user, ip, port):
        self._user = user
        self._ip = ip
        self._port = port
        self._client = socket(AF_INET, SOCK_STREAM)

    def receive_message(self):
        while True:
            data = self._client.recv(RSIZE).decode('utf-8')
            if data:
                print(data)

    def send_message(self):
        while True:
            message = input(self._user + ': ')
            self._client.send(message.encode())
        self._client.close()

    def chat(self):
        self._client.connect((self._ip, self._port))
        self._client.send(self._user.encode())
        recv = Thread(target=self.receive_message)
        recv.start()
        send = Thread(target=self.send_message)
        send.start()

if __name__ == '__main__':
    user_name = input('User Name: ')
    ip = '127.0.0.1'
    port = 8080

    client = Chatter(user_name, ip, port)
    client.chat()