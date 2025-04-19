"""
There are N savage threads who eat from a shared pot.
A cook thread fills the pot when it's empty.
Each time a savage wants to eat, they must:

Acquire a serving from the pot

If the pot is empty, one savage must wake up the cook

Wait until the pot is refilled
"""
from threading import Lock, Condition, Thread
import time
import random

class DiningPot:
    def __init__(self, capacity):
        self.capacity = capacity
        self.servings = 0
        self.pot_lock = Lock()
        self.cook_needed = Condition(self.pot_lock)
        self.servings_available = Condition(self.pot_lock)

    def get_serving(self, savage_id):
        with self.pot_lock:
            while self.servings == 0:
                print(f"🦸‍♂️ Savage {savage_id} is waiting for the cook to refill the pot.")
                self.cook_needed.notify()
                self.servings_available.wait()
            self.servings -= 1
            print(f"🍽️ Savage {savage_id} took a serving. Servings left: {self.servings}")

    def refill_pot(self, cook_id):
        with self.pot_lock:
            if self.servings < self.capacity:
                self.servings = self.capacity
                print(f"👨‍🍳 Cook {cook_id} refilled the pot. Servings available: {self.servings}")
                self.servings_available.notify_all()
            else:
                print(f"👨‍🍳 Cook {cook_id} found the pot already full. No refill needed.")


def cook(pot:DiningPot):
    while True:
        pot.refill_pot(cook_id=0)
        time.sleep(random.uniform(1, 3))

def savage(pot:DiningPot, savage_id:int):
    while True:
        pot.get_serving(savage_id=savage_id)
        print(f"🍽️ Savage {savage_id} is eating.")
        time.sleep(random.uniform(1, 2))  # Simulate eating time


if __name__ == "__main__":
    pot = DiningPot(capacity=3)
    cook_thread = Thread(target=cook, args=(pot,), daemon=True)
    cook_thread.start()

    for i in range(5):
        savage_thread = Thread(target=savage, args=(pot, i), daemon=True)
        savage_thread.start()

    time.sleep(10)  # Let the simulation run for a while