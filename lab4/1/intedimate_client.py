import socket
import struct
import threading

MULTICAST_GROUP = '233.0.0.1'
PORT = 1502
TCP_PORT = 5050

filtered_messages = []


def udp_listener():
    global filtered_messages
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', PORT))

    mreq = struct.pack("4sl", socket.inet_aton(
        MULTICAST_GROUP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    last_message = ""

    while True:
        message, _ = sock.recvfrom(1024)
        message = message.decode('utf-8')

        if message != last_message:
            print(f"Новое сообщение: {message}")
            last_message = message
            filtered_messages.append(message)

            if len(filtered_messages) > 5:
                filtered_messages.pop(0)


def tcp_server():
    global filtered_messages
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(('127.0.0.1', TCP_PORT))
    server_sock.listen(5)

    while True:
        conn, addr = server_sock.accept()
        print(f"Клиент подключен: {addr}")
        for message in filtered_messages:
            conn.sendall(f"{message}\n".encode('utf-8'))
        conn.close()


if __name__ == "__main__":
    udp_thread = threading.Thread(target=udp_listener)
    tcp_thread = threading.Thread(target=tcp_server)

    udp_thread.start()
    tcp_thread.start()

    udp_thread.join()
    tcp_thread.join()
