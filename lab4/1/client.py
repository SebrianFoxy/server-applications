import socket
import tkinter as tk
import threading

TCP_SERVER = 'localhost'
TCP_PORT = 5050

SOCKET_TIMEOUT = 5


def get_messages():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(SOCKET_TIMEOUT)
        sock.connect((TCP_SERVER, TCP_PORT))
        messages = sock.recv(1024).decode('utf-8')
        sock.close()
        return messages.splitlines()
    except socket.timeout:
        return ["Ошибка: превышен тайм-аут подключения"]
    except Exception as e:
        return [f"Ошибка: {e}"]


def update_messages():
    messages = get_messages()
    message_list.delete(0, tk.END)
    for msg in messages:
        message_list.insert(tk.END, msg)


def refresh_messages():
    # Запускаем обновление в отдельном потоке, чтобы не блокировать UI
    threading.Thread(target=update_messages).start()


# GUI с помощью Tkinter
root = tk.Tk()
root.title("Последние сообщения")

message_list = tk.Listbox(root, width=50, height=10)
message_list.pack(pady=20)

refresh_button = tk.Button(root, text="Обновить", command=refresh_messages)
refresh_button.pack()

root.mainloop()
