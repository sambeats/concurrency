from threading import Lock, Thread
from typing import Callable
import time
import random

class TrafficLight:
    def __init__(self):
        # Q0 ── Q1
        # │     │
        # Q3 ── Q2
        self.quadrants = [Lock() for _ in range(4)]

    def carArrived(
        self,
        carId: int,
        direction: int,        # 0=N, 1=E, 2=S, 3=W
        turnDirection: int,    # 0=straight, 1=left, 2=right
        carEnter: Callable[[], None],
        carExit: Callable[[], None]
    ) -> None:
        required_quadrants = self.get_quadrants(direction, turnDirection)

        # Lock in sorted order to prevent deadlock
        for q in sorted(required_quadrants):
            self.quadrants[q].acquire()

        carEnter()
        carExit()

        # Release in reverse order
        for q in sorted(required_quadrants, reverse=True):
            self.quadrants[q].release()

    def get_quadrants(self, direction: int, turn: int):
        if direction == 0:  # North
            if turn == 2: return [0]
            if turn == 0: return [0, 1]
            if turn == 1: return [0, 1, 2]
        elif direction == 1:  # East
            if turn == 2: return [1]
            if turn == 0: return [1, 2]
            if turn == 1: return [1, 2, 3]
        elif direction == 2:  # South
            if turn == 2: return [2]
            if turn == 0: return [2, 3]
            if turn == 1: return [2, 3, 0]
        elif direction == 3:  # West
            if turn == 2: return [3]
            if turn == 0: return [3, 0]
            if turn == 1: return [3, 0, 1]
        return []

# Simulate enter and exit
def make_car_enter_exit(carId, direction, turnDirection):
    def enter():
        print(f"Car {carId} entering from {direction_name(direction)} turning {turn_name(turnDirection)}")
    def exit():
        print(f"Car {carId} exiting")
    return enter, exit

def direction_name(d):
    return ["North", "East", "South", "West"][d]

def turn_name(t):
    return ["Straight", "Left", "Right"][t]

if __name__ == "__main__":
    traffic = TrafficLight()
    threads = []

    # Simulate 10 cars with random directions and turns
    for carId in range(1, 11):
        direction = random.randint(0, 3)
        turn = random.randint(0, 2)
        carEnter, carExit = make_car_enter_exit(carId, direction, turn)

        t = Thread(target=traffic.carArrived, args=(carId, direction, turn, carEnter, carExit))
        threads.append(t)
        t.start()
        time.sleep(random.uniform(0.05, 0.2))  # simulate staggered arrival

    for t in threads:
        t.join()
