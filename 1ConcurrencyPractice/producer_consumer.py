import threading
import time
import random

class BoundedBuffer:
    def __init__(self, capacity):
        self.buffer = []
        self.capacity = capacity
        self.lock = threading.Lock()
        self.not_full = threading.Condition(self.lock)
        self.not_empty = threading.Condition(self.lock)

    def produce(self, item, producer_id):
        with self.not_full:
            while len(self.buffer) == self.capacity:
                print(f"Producer {producer_id}: Buffer full, waiting.")
                self.not_full.wait()

            self.buffer.append(item)
            print(f"Producer {producer_id}: Produced {item}. Buffer: {self.buffer}")

            self.not_empty.notify()

    def consume(self, consumer_id):
        with self.not_empty:
            while not self.buffer:
                print(f"Consumer {consumer_id}: Buffer empty, waiting.")
                self.not_empty.wait()

            item = self.buffer.pop(0)
            print(f"Consumer {consumer_id}: Consumed {item}. Buffer: {self.buffer}")

            self.not_full.notify()
            return item

class ProducerThread(threading.Thread):
    def __init__(self, buffer, producer_id, num_items=5):
        super().__init__()
        self.buffer = buffer
        self.producer_id = producer_id
        self.num_items = num_items

    def run(self):
        for _ in range(self.num_items):
            item = random.randint(1, 100)
            self.buffer.produce(item, self.producer_id)
            time.sleep(random.uniform(0.1, 0.5))

class ConsumerThread(threading.Thread):
    def __init__(self, buffer, consumer_id, num_items=5):
        super().__init__()
        self.buffer = buffer
        self.consumer_id = consumer_id
        self.num_items = num_items

    def run(self):
        for _ in range(self.num_items):
            self.buffer.consume(self.consumer_id)
            time.sleep(random.uniform(0.1, 0.5))

def test_producer_consumer():
    buffer = BoundedBuffer(capacity=5)
    producers = [ProducerThread(buffer, producer_id=i, num_items=5) for i in range(2)]
    consumers = [ConsumerThread(buffer, consumer_id=i, num_items=5) for i in range(2)]

    for p in producers: p.start()
    for c in consumers: c.start()

    for p in producers: p.join()
    for c in consumers: c.join()

if __name__ == "__main__":
    test_producer_consumer()
