import threading
import time

counter = 0
lock = threading.Lock()


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


def main(n, m):
    global counter
    counter = 0
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
    print(f"Final counter value: {counter}")
    print(f"Execution time: {end_time - start_time} seconds")


if __name__ == "__main__":
    n = int(input("Enter number of incrementing threads: "))
    m = int(input("Enter number of decrementing threads: "))
    main(n, m)
