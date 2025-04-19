import threading
import time
import random
from collections import deque, defaultdict

class Fork:
    def __init__(self, owner_id):
        self.owner = owner_id
        self.dirty = True

class Message:
    def __init__(self, sender_id, fork_id, type_):
        self.sender_id = sender_id
        self.fork_id = fork_id  # (min, max) pair
        self.type = type_       # 'request' or 'fork'

class Philosopher(threading.Thread):
    def __init__(self, id_, num_philosophers, mailboxes, forks):
        super().__init__(daemon=True)
        self.id = id_
        self.N = num_philosophers
        self.mailboxes = mailboxes  # shared between all
        self.forks = forks          # dict of fork_id -> Fork
        self.neighbors = [(id_ - 1) % self.N, (id_ + 1) % self.N]
        self.owned_forks = set()
        self.requested_forks = set()
        self.pending_requests = set()
        self.lock = threading.Lock()

    def run(self):
        while True:
            self.think()
            self.acquire_forks()
            self.eat()
            self.release_forks()

    def think(self):
        print(f"🧠 Philosopher {self.id} is thinking.")
        time.sleep(random.uniform(1, 2))

    def acquire_forks(self):
        # Request any fork not owned
        for neighbor in self.neighbors:
            fork_id = tuple(sorted((self.id, neighbor)))
            if fork_id not in self.owned_forks:
                self.send_request(fork_id, neighbor)
                self.requested_forks.add(fork_id)

        # Wait until we have both forks
        while not all(tuple(sorted((self.id, n))) in self.owned_forks for n in self.neighbors):
            self.process_incoming_messages()
            time.sleep(0.1)

    def send_request(self, fork_id, to):
        msg = Message(self.id, fork_id, 'request')
        self.mailboxes[to].append(msg)
        print(f"📩 Philosopher {self.id} requested fork {fork_id} from {to}")

    def process_incoming_messages(self):
        while self.mailboxes[self.id]:
            msg = self.mailboxes[self.id].popleft()
            if msg.type == 'request':
                self.handle_fork_request(msg)
            elif msg.type == 'fork':
                self.handle_fork_delivery(msg)

    def handle_fork_request(self, msg):
        fork_id = msg.fork_id
        if fork_id in self.owned_forks:
            fork = self.forks[fork_id]
            if fork.dirty:
                # Send the fork
                self.owned_forks.remove(fork_id)
                fork.owner = msg.sender_id
                fork.dirty = False
                self.mailboxes[msg.sender_id].append(Message(self.id, fork_id, 'fork'))
                print(f"🔁 Philosopher {self.id} sent fork {fork_id} to {msg.sender_id}")
            else:
                # Defer sending
                self.pending_requests.add((msg.sender_id, fork_id))
        else:
            # Don’t own it, can’t send
            pass

    def handle_fork_delivery(self, msg):
        fork_id = msg.fork_id
        self.owned_forks.add(fork_id)
        self.forks[fork_id].owner = self.id
        print(f"✅ Philosopher {self.id} received fork {fork_id}")

    def eat(self):
        print(f"🍝 Philosopher {self.id} is eating.")
        time.sleep(random.uniform(1, 2))

    def release_forks(self):
        # Mark all forks dirty
        for fork_id in self.owned_forks:
            self.forks[fork_id].dirty = True

        # Respond to pending requests
        for (sender_id, fork_id) in list(self.pending_requests):
            if fork_id in self.owned_forks:
                fork = self.forks[fork_id]
                fork.owner = sender_id
                fork.dirty = False
                self.owned_forks.remove(fork_id)
                self.mailboxes[sender_id].append(Message(self.id, fork_id, 'fork'))
                print(f"📤 Philosopher {self.id} released fork {fork_id} to {sender_id}")
                self.pending_requests.remove((sender_id, fork_id))
