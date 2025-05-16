import threading
import time
import random

class Bathroom:
    def __init__(self):
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)
        self.men_inside = 0
        self.women_inside = 0
        self.waiting_men = 0
        self.waiting_women = 0
        self.current_gender = None  # "male" or "female"
        self.turn = "female"  # Gives turn to alternate if both waiting

    def enter_male(self, id):
        with self.condition:
            self.waiting_men += 1
            while (self.current_gender == "female" and self.women_inside > 0) or \
                  (self.turn == "female" and self.waiting_women > 0):
                self.condition.wait()
            self.waiting_men -= 1
            self.men_inside += 1
            self.current_gender = "male"
            print(f"Man {id} entered. Men inside: {self.men_inside}")

    def leave_male(self, id):
        with self.condition:
            self.men_inside -= 1
            print(f"Man {id} left. Men inside: {self.men_inside}")
            if self.men_inside == 0:
                self.current_gender = None
                if self.waiting_women > 0:
                    self.turn = "female"
                else:
                    self.turn = "male"
                self.condition.notify_all()

    def enter_female(self, id):
        with self.condition:
            self.waiting_women += 1
            while (self.current_gender == "male" and self.men_inside > 0) or \
                  (self.turn == "male" and self.waiting_men > 0):
                self.condition.wait()
            self.waiting_women -= 1
            self.women_inside += 1
            self.current_gender = "female"
            print(f"Woman {id} entered. Women inside: {self.women_inside}")

    def leave_female(self, id):
        with self.condition:
            self.women_inside -= 1
            print(f"Woman {id} left. Women inside: {self.women_inside}")
            if self.women_inside == 0:
                self.current_gender = None
                if self.waiting_men > 0:
                    self.turn = "male"
                else:
                    self.turn = "female"
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
            time.sleep(self.delay)
            self.bathroom.leave_male(self.id)
        elif self.gender == "female":
            self.bathroom.enter_female(self.id)
            time.sleep(self.delay)
            self.bathroom.leave_female(self.id)

def test_bathroom_problem():
    bathroom = Bathroom()
    threads = []

    # Simulate 5 males and 5 females arriving randomly
    for i in range(5):
        threads.append(PersonThread(bathroom, "male", i))
        threads.append(PersonThread(bathroom, "female", i))

    # Start all threads with slight delays
    for thread in threads:
        thread.start()
        time.sleep(0.03)

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    test_bathroom_problem()
    print("All threads have finished")
    