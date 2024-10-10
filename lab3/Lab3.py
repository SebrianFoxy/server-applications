import os
import platform
import threading
import time
from threading import RLock


def increment():
    global counter
    for _ in range(100000):
        with lock:
            local_counter = counter
            local_counter += 1
            counter = local_counter


def decrement():
    global counter
    for _ in range(100000):
        with lock:
            local_counter = counter
            local_counter -= 1
            counter = local_counter


def measure_performance(n, m):
    global counter, lock
    counter = 0
    lock = RLock()

    threads = []

    start_time = time.time()

    for _ in range(n):
        thread = threading.Thread(target=increment)
        threads.append(thread)
        thread.start()

    for _ in range(m):
        thread = threading.Thread(target=decrement)
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time = time.time()
    return end_time - start_time

def get_system_info():
    return {
        "Processor": platform.processor(),
        "System": platform.system(),
        "Version": platform.version(),
        "Memory": f"{os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES') / (1024. ** 3):.2f} GB"
    }

# Измеряем время для каждого набора потоков


def run_experiments():
    results = []
    thread_counts = [1, 2, 4, 8]
    for count in thread_counts:
        time_taken = measure_performance(count, count)
        results.append((count, time_taken))

    system_info = get_system_info()

    with open('Lab3.txt', 'w') as f:
        f.write("Threads | Time (seconds)\n")
        f.write("------------------------\n")
        for count, time_taken in results:
            f.write(f"{count}       | {time_taken:.4f}\n")

        f.write("\nSystem Specifications:\n")
        for key, value in system_info.items():
            f.write(f"{key}: {value}\n")


if __name__ == "__main__":
    run_experiments()
