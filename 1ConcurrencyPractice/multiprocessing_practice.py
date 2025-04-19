from multiprocessing import Process
from multiprocessing import current_process
import os
import multiprocessing

# Set fork to be the default method for process creation
# This is the default on Unix-like systems, but on Windows, it uses spawn by default.
# import multiprocessing
multiprocessing.set_start_method('fork', force=True)

def process_task():
    print(f"Process {current_process().name} (PID: {os.getpid()}) is running")

"""
Here note that if we do not use the __name__ == "__main__" guard, the child processes will try to import the main module again,
 which can lead to infinite recursion or other unexpected behavior.
This is because the child processes will execute the same code as the main process, including creating new child processes.

Note the difference between how Windows and Unix-like systems handle process creation. On Windows, the entire Python interpreter is reloaded in the child process,
while on Unix-like systems, the child process is a clone of the parent process. This can lead to different behavior if not handled properly.
"""
if __name__ == "__main__":
    print(f"Main process (PID: {os.getpid()}) started")

    # Create and start 3 processes
    process = [0] * 3

    for i in range(3):
        process[i] = Process(target=process_task, name=f"Process-{i+1}")
        process[i].start()

    for i in range(3):
        process[i].join()

    print(f"Main process (PID: {os.getpid()}) finished")
    # This code demonstrates the use of multiprocessing in Python.