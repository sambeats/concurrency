import threading
import heapq
import random
import time

class ThreadSafePriorityQueue:
    def __init__(self):
        self.lock = threading.Lock()
        self.heap = []

    def push(self, task):
        with self.lock:
            heapq.heappush(self.heap, task)

    def pop(self):
        with self.lock:
            if self.heap:
                return heapq.heappop(self.heap)
            return None

    def get_all_tasks(self):
        with self.lock:
            tasks = self.heap[:]
            self.heap.clear()
            return tasks

    def is_empty(self):
        with self.lock:
            return not self.heap

    def __str__(self):
        with self.lock:
            return str(sorted(self.heap))

class DistributedTaskManager:
    def __init__(self, num_nodes):
        self.num_nodes = num_nodes
        self.nodes = [ThreadSafePriorityQueue() for _ in range(num_nodes)]
        self.node_locks = [threading.Lock() for _ in range(num_nodes)]

    def addTask(self, task: int):
        node_index = random.randint(0, self.num_nodes - 1)
        self.nodes[node_index].push(task)
        print(f"[addTask] Task {task} added to Node {node_index}")

    def isTaskFinished(self, task: int):
        time.sleep(0.1)  # simulate work
        return True

    def runTask(self):
        def worker(node_id, queue: ThreadSafePriorityQueue):
            while not queue.is_empty():
                task = queue.pop()
                if task is None:
                    return
                print(f"[runTask] Node {node_id} running Task {task}")
                while not self.isTaskFinished(task):
                    pass
                print(f"[runTask] Node {node_id} finished Task {task}")

        threads = []
        for i in range(self.num_nodes):
            t = threading.Thread(target=worker, args=(i, self.nodes[i]))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

    def printTaskQueue(self):
        node_index = random.randint(0, self.num_nodes - 1)
        print(f"[printTaskQueue] Node {node_index}: {self.nodes[node_index]}")

    def rebalanceTask(self):
        print("[rebalanceTask] Rebalancing started...")
        all_tasks = []
        for queue in self.nodes:
            all_tasks.extend(queue.get_all_tasks())

        all_tasks.sort()
        for i, task in enumerate(all_tasks):
            self.nodes[i % self.num_nodes].push(task)
        print("[rebalanceTask] Rebalancing complete.")
