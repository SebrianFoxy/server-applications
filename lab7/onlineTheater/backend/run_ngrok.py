import subprocess
import requests
import time

file_path = "ngrok_url.txt"

def get_ngrok_url():
    try:
        response = requests.get("http://127.0.0.1:4040/api/tunnels")
        data = response.json()
        for tunnel in data['tunnels']:
            if tunnel['public_url'].startswith("https"):
                print(tunnel['public_url'])
                return tunnel['public_url']
    except Exception as e:
        print("Не удалось получить URL из Ngrok:", e)
    return None


def write_url_to_file(url):
    with open(file_path, "w") as file:
        file.write(url)


def start_ngrok():
    command = ["ngrok", "http", "8000"]
    process = subprocess.Popen(command)
    return process


def run_ngrok():
    ngrok_process = start_ngrok()
    time.sleep(5)
    url = None
    while not url:
        url = get_ngrok_url()
        if url:
            write_url_to_file(url)
            print(f"Текущий URL Ngrok: {url} (сохранён в {file_path})")
            return ngrok_process
        else:
            print("Ожидание запуска Ngrok...")
            time.sleep(2)

run_ngrok()
