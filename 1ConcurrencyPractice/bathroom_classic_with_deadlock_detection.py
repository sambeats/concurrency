import threading
import time
from collections import defaultdict

class Bathroom:
    def __init__(self):
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)

        self.current_gender = None
        self.inside_count = 0
        self.waiting = defaultdict(int)

    def enter(self, gender: str):
        with self.condition:
            self.waiting[gender] += 1
            while self.current_gender not in (None, gender):
                self.condition.wait()

            self.waiting[gender] -= 1
            self.current_gender = gender
            self.inside_count += 1
            print(f"{gender} entered. Inside count: {self.inside_count}")

    def leave(self, gender: str):
        with self.condition:
            self.inside_count -= 1
            print(f"{gender} left. Inside count: {self.inside_count}")

            if self.inside_count == 0:
                self.current_gender = None
                self.condition.notify_all()  # Allow other gender to proceed

# Create a watchdog thread to monitor the bathroom state and detect deadlocks
class DeadlockDetector(threading.Thread):
    def __init__(self, bathroom: Bathroom, timeout=5):
        super().__init__(daemon=True)
        self.bathroom = bathroom
        self.timeout = timeout
        self.last_change_time = time.time()
        self.prev_state = None

    def run(self):
        while True:
            time.sleep(self.timeout)
            with self.bathroom.lock:
                # Capture the current state
                current_state = (
                    self.bathroom.current_gender,
                    self.bathroom.inside_count,
                    dict(self.bathroom.waiting)
                )
                # Check if the state has not changed
                if current_state == self.prev_state:
                    print("[⚠️] Potential deadlock detected:")
                    print(f"    Current Gender: {self.bathroom.current_gender}")
                    print(f"    Inside Count: {self.bathroom.inside_count}")
                    print(f"    Waiting: {dict(self.bathroom.waiting)}")
                else:
                    self.prev_state = current_state

def person(bathroom: Bathroom, gender: str, wait_before=0):
    time.sleep(wait_before)
    bathroom.enter(gender)
    time.sleep(2)  # simulate bathroom use
    bathroom.leave(gender)

def main():
    bathroom = Bathroom()
    detector = DeadlockDetector(bathroom)
    detector.start()

    threads = []
    # Simulate mixed gender usage with potential for conflict
    for i in range(3):
        threads.append(threading.Thread(target=person, args=(bathroom, 'Male', i * 0.2)))
        threads.append(threading.Thread(target=person, args=(bathroom, 'Female', i * 0.3)))

    for t in threads:
        t.start()

    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
    print("Simulation complete.")
    print("Exiting main thread.")