import socket
import time

MULTICAST_GROUP = '233.0.0.1'
PORT = 1502


def read_message():
    with open("weather.txt", "r", encoding="utf-8") as file:
        return file.read()


def start_server():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)

    while True:
        message = read_message()
        sock.sendto(message.encode('utf-8'), (MULTICAST_GROUP, PORT))
        print(f"Отправлено сообщение: {message}")
        time.sleep(3) 


if __name__ == "__main__":
    start_server()
