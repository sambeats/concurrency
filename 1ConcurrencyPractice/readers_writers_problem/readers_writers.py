"""
✅ Readers-Writers Variants
First Readers Preference (Reader-biased):
Readers don’t wait if there’s already an ongoing read. Writers might starve.

Writers Preference (Writer-biased):
Readers wait if a writer is waiting. Reduces writer starvation.

Fair Version:
Readers and writers are served in arrival order using a queue or semaphore.

We'll start with Readers Preference, and then can evolve it to writer/fair version as needed.
"""
import threading
import time
import random

class SharedResource:
    def __init__(self):
        self.data = 0
    
    def read(self,reader_id):
        print(f"Reader {reader_id} is reading data: {self.data}")
        time.sleep(random.uniform(0.1, 0.5))
        print(f"Reader {reader_id} finished reading.") # Simulate time taken to read data
    
    def write(self, writer_id, value):
        print(f"Writer {writer_id} is writing data: {value}")
        self.data = value
        time.sleep(random.uniform(0.2, 0.6))
        print(f"Writer {writer_id} finished writing.") # Simulate time taken to write data


class ReadersWriters:
    def __init__(self,resource):
        self.resource = resource
        self.read_count = 0
        self.read_count_lock = threading.Lock()
        self.resource_lock = threading.Lock()

    def reader(self,reader_id):
        while True:
            with self.read_count_lock:
                self.read_count += 1
                if self.read_count == 1:
                    self.resource_lock.acquire()
            self.resource.read(reader_id)

            with self.read_count_lock:
                self.read_count -= 1
                if self.read_count == 0:
                    self.resource_lock.release()
            time.sleep(random.uniform(0.1, 0.5))
        
    def writer(self,writer_id,value):
        with self.resource_lock:
            self.resource.write(writer_id, value)
        value += 1
        # Simulate time taken to write data
        time.sleep(random.uniform(0.1, 0.5))