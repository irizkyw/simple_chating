import socket
import threading

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket = self.setup(self.socket)
        self.clients = {}  # Menyimpan daftar klien dan nama mereka

    def setup(self, socket):
        socket.bind((self.host, self.port))
        socket.listen(2)  # Hanya menerima dua koneksi
        return socket

    def accept(self):
        while True:
            client, address = self.socket.accept()
            self.authenticate_client(client)

    def authenticate_client(self, client):
        try:
            username = client.recv(1024).decode()
            self.clients[username] = client
            print(f"{username} terhubung dari {client.getpeername()}")
            thread_client = threading.Thread(target=self.handle_client, args=[username])
            thread_client.start()
        except Exception as x:
            print(x)

    def handle_client(self, username):
        client = self.clients[username] # Ambil klien dari daftar klien
        while True:
            try:
                data = client.recv(1024)
                if data.decode() == 'list_users':
                    client.send(str(list(self.clients.keys())).encode())
                
                if data:
                    message = data.decode()
                    recipient, message = message.split(":")
                    if recipient == 'all':
                        for client in self.clients.values():
                            client.send(f"{username}:{message}".encode())
                    else:
                        self.clients[recipient].send(f"{username}:{message}".encode())

            except Exception as x:
                print(f"{username} terputus")
                del self.clients[username]
                break

            
if __name__ == "__main__":
    HOST = 'sister.cyclic.cloud'
    PORT = 8000
    print("Server started")
    server = Server(HOST, PORT)
    print("Waiting for clients")
    thread_ac = threading.Thread(target=server.accept)
    thread_ac.start()
