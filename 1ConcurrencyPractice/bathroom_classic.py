import threading
import time

class Bathroom:
    def __init__(self):
        self.lock = threading.Lock()
        self.men_inside = 0
        self.women_inside = 0
        self.condition = threading.Condition(self.lock)

    def enter_male(self, id):
        with self.condition:
            while self.women_inside > 0:
                self.condition.wait()
            self.men_inside += 1
            print(f"Man {id} entered. Men inside: {self.men_inside}")

    def leave_male(self, id):
        with self.condition:
            self.men_inside -= 1
            print(f"Man {id} left. Men inside: {self.men_inside}")
            if self.men_inside == 0:
                self.condition.notify_all()

    def enter_female(self, id):
        with self.condition:
            while self.men_inside > 0:
                self.condition.wait()
            self.women_inside += 1
            print(f"Woman {id} entered. Women inside: {self.women_inside}")

    def leave_female(self, id):
        with self.condition:
            self.women_inside -= 1
            print(f"Woman {id} left. Women inside: {self.women_inside}")
            if self.women_inside == 0:
                self.condition.notify_all()

class PersonThread(threading.Thread):
    def __init__(self, bathroom, gender, id, delay=0.1):
        super().__init__()
        self.bathroom = bathroom
        self.gender = gender
        self.id = id
        self.delay = delay

    def run(self):
        if self.gender == "male":
            self.bathroom.enter_male(self.id)
            time.sleep(self.delay)  # simulate time inside the bathroom
            self.bathroom.leave_male(self.id)
        elif self.gender == "female":
            self.bathroom.enter_female(self.id)
            time.sleep(self.delay)  # simulate time inside the bathroom
            self.bathroom.leave_female(self.id)

def test_bathroom_problem():
    bathroom = Bathroom()
    threads = []

    # Simulate 3 males and 3 females arriving in alternating order
    for i in range(3):
        threads.append(PersonThread(bathroom, "male", i))
        threads.append(PersonThread(bathroom, "female", i))

    # Start all threads with a slight delay to simulate concurrency
    for thread in threads:
        thread.start()
        time.sleep(0.05)

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    test_bathroom_problem()
