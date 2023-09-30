import socket
import threading

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.username = None

    def connect_to_server(self):
        self.client_socket.connect((self.host, self.port))
        self.username = input("Masukkan nama pengguna: ")
        print(f"Terhubung ke {self.host}:{self.port} sebagai {self.username}")
        self.client_socket.send(self.username.encode())

    def receive_messages(self):
        while True:
            try:
                # cek pesan sesuai nama sender
                message = self.client_socket.recv(1024).decode()
                if message:
                    print(message)
                    
            except Exception as x:
                print(x)
                break

    def send_message(self):
        while True:
            recipient = input()
            if recipient == 'list':
                self.request_user_list()
                continue
            self.client_socket.send(recipient.encode())

    def request_user_list(self):
        self.client_socket.send("list_users".encode())

if __name__ == "__main__":
    HOST = '192.168.1.102'
    PORT = 8000
    client = Client(HOST, PORT)
    client.connect_to_server()
    print("===============================================")
    print("Ketik 'list' untuk melihat daftar pengguna yang online")
    print("target: pesan")
    print("all: pesan untuk semua pengguna")
    print("===============================================")
    # Thread untuk menerima pesan
    thread_receive = threading.Thread(target=client.receive_messages)
    thread_receive.start()

    # Thread untuk mengirim pesan
    thread_send = threading.Thread(target=client.send_message)
    thread_send.start()