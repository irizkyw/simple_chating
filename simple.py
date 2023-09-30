import socket
# Buat socket server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0", 12345))  # Ganti alamat dan port sesuai kebutuhan
server_socket.listen(5)  # Maksimal 5 koneksi dalam antrian
print("Server siap menerima koneksi...")

# Buat socket klien
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Terima koneksi dari klien
client_socket, client_address = server_socket.accept()
print(f"Terhubung ke {client_address}")
while True:
    # Terima pesan dari klien
    received_message = client_socket.recv(1024).decode("utf-8")
    print(f"Pesan dari klien: {received_message}")

    # Kirim balasan ke klien
    message_to_send = input("Pesan untuk klien: ")
    client_socket.send(message_to_send.encode("utf-8"))
client_socket.close()
server_socket.close()