import threading
import time
import random

class Playground:
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.lock = threading.Lock()
        self.cond = threading.Condition(self.lock)

        self.current_team = None         # Team currently inside
        self.players_inside = 0          # Number of players inside
        self.waiting_teams = []          # Teams waiting in order
        self.team_waiting_counts = {}    # Players waiting per team

    def enter(self, team_name: str):
        with self.lock:
            # If this team is not current or waiting, add to queue
            if team_name != self.current_team and team_name not in self.waiting_teams:
                self.waiting_teams.append(team_name)
                self.team_waiting_counts[team_name] = 0

            # Track this player's arrival to waiting count
            self.team_waiting_counts[team_name] += 1

            while True:
                can_enter_team = (
                    (self.current_team is None and self.waiting_teams[0] == team_name) or
                    (self.current_team == team_name)
                )
                has_capacity = self.players_inside < self.capacity

                if can_enter_team and has_capacity:
                    # Player allowed inside
                    if self.current_team is None:
                        self.current_team = team_name
                    self.players_inside += 1
                    self.team_waiting_counts[team_name] -= 1
                    # Remove from waiting if no players left waiting
                    if self.team_waiting_counts[team_name] == 0:
                        del self.team_waiting_counts[team_name]
                        if team_name in self.waiting_teams:
                            self.waiting_teams.remove(team_name)
                    # Debug print
                    print(f"[ENTER] Team {team_name} Player enters. Inside: {self.players_inside}")
                    return
                # Otherwise wait
                self.cond.wait()

    def leave(self, team_name: str):
        with self.lock:
            self.players_inside -= 1
            print(f"[LEAVE] Team {team_name} Player leaves. Inside: {self.players_inside}")
            if self.players_inside == 0:
                # Team leaving playground, free it
                print(f"Team {team_name} leaves playground.")
                self.current_team = None
                # Notify all waiting players so next team can enter
                self.cond.notify_all()
            else:
                # Notify waiting players from the same team if capacity allows
                self.cond.notify_all()


def player(playground: Playground, team_name: str, player_id: int):
    print(f"Player {player_id} from Team {team_name} trying to enter playground.")
    playground.enter(team_name)
    # Simulate play time
    time.sleep(random.uniform(0.1, 0.5))
    playground.leave(team_name)
    print(f"Player {player_id} from Team {team_name} done playing.")


if __name__ == "__main__":
    playground = Playground(capacity=10)

    teams = ['Red', 'Blue', 'Green']
    threads = []

    # Spawn multiple players from different teams
    for i in range(30):
        team = random.choice(teams)
        t = threading.Thread(target=player, args=(playground, team, i))
        threads.append(t)
        t.start()
        time.sleep(random.uniform(0.01, 0.05))  # Slight stagger to simulate real concurrency

    # Wait for all players to finish
    for t in threads:
        t.join()

    print("All players done.")
