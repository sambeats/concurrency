import threading
import time
import functools

class Watchdog:
    def __init__(self, timeout=5):
        self.timeout = timeout
        self.last_activity = {}
        self.lock = threading.Lock()
        self.running = True
        self.monitor_thread = threading.Thread(target=self._monitor, daemon=True)
        self.monitor_thread.start()

    def ping(self, thread_id):
        with self.lock:
            self.last_activity[thread_id] = time.time()

    def _monitor(self):
        while self.running:
            time.sleep(1)
            now = time.time()
            with self.lock:
                for thread_id, last_time in self.last_activity.items():
                    if now - last_time > self.timeout:
                        print(f"[WATCHDOG] 🛑 Potential deadlock: {thread_id} has been inactive for {int(now - last_time)}s")

    def stop(self):
        self.running = False
        self.monitor_thread.join()


# Decorator that uses the watchdog
def deadlock_detector(watchdog):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            thread_id = threading.current_thread().name
            watchdog.ping(thread_id)  # ping before execution
            result = func(*args, **kwargs)
            watchdog.ping(thread_id)  # ping after execution
            return result
        return wrapper
    return decorator
