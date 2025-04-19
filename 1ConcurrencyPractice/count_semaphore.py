from threading import Condition,Thread
import time
import random

class CountSemaphore():
    def __init__(self, permits):
        self.max_permits = permits
        self.given_out = 0
        self.cond_var = Condition()

    def acquire(self):
        with self.cond_var:
            while self.given_out == self.max_permits:
                self.cond_var.wait()

            self.given_out += 1
            self.cond_var.notifyAll()

    def release(self):
        with self.cond_var:
            while self.given_out == 0:
                self.cond_var.wait()

            self.given_out -= 1
            self.cond_var.notifyAll()
            
    def __enter__(self):
        self.acquire()
        return self  # optional, could be None

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

sema = CountSemaphore(3)

def download(thread_id):
    print(f"[{thread_id}] Waiting for permit")
    with sema:
        print(f"[{thread_id}] Got permit ✅ Downloading...")
        time.sleep(random.uniform(1, 3))  # Simulate download time
        print(f"[{thread_id}] Done, releasing permit")

# Start 6 threads but only 3 should run concurrently
threads = [Thread(target=download, args=(i,)) for i in range(6)]
for t in threads:
    t.start()
for t in threads:
    t.join()