import socket
from _thread import *
from collections import defaultdict as df
import random
from cfb import _cfb_encrypt
from gm import encrypt

class Server:
    def __init__(self):
        self.rooms = df(list)
        self.folder_users = "D:\\lolita\\university\\7semester\\kbrs\\practice\\lab2\\clients\\"
        self.folder_keys = "D:\\lolita\\university\\7semester\\kbrs\\practice\\lab2\\keys\\"
        self.folder_files = "D:\\lolita\\university\\7semester\\kbrs\\practice\\lab2\\files\\"
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def accept_connections(self, ip_address, port):
        self.ip_address = ip_address
        self.port = port
        self.server.bind((self.ip_address, int(self.port)))
        self.server.listen(100)

        while True:
            connection, address = self.server.accept()
            print(str(address[0]) + ":" + str(address[1]) + " Connected")
            start_new_thread(self.clientThread, (connection,))
        self.server.close()

    def clientThread(self, connection):
        file_name = connection.recv(1024).decode()
        public_key = []
        public_key.append(int(connection.recv(1024).decode()))
        public_key.append(int(connection.recv(1024).decode()))
        key = (public_key[0], public_key[1])
        print(file_name, key)
        session_key = "".join([str(random.choice([0,1])) for _ in range(256)])
        self.rooms[file_name].append([connection, key, session_key])
        with open(self.folder_files + file_name) as f:
            text = f.read()
        pt = ''.join(format(ord(i), '08b') for i in text)
        ciphertext = _cfb_encrypt(pt, session_key) + '\n'
        print("plain text len: ", len(pt))
        print("Plaintext:", pt)
        encrypted_key = encrypt(str(session_key), key)
        enc_key_str = " ".join([str(i) for i in encrypted_key])
        enc_key_str += '\n'
        print("Key: {}| {}| {}".format(str(session_key), len(encrypted_key), enc_key_str))
        while True:
            try:
                connection.send(ciphertext.encode())
                connection.send(enc_key_str.encode())
            except Exception as e:
                print(repr(e))
                print("Client disconnected earlier")
                self.remove(connection, file_name)
                break


    def remove(self, connection, room_id):
        if connection in self.rooms[room_id]:
            self.rooms[room_id].remove(connection)


if __name__ == "__main__":
    ip_address = "127.0.0.1"
    port = 12345

    s = Server()
    s.accept_connections(ip_address, port)