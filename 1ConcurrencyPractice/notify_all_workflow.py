from threading import Thread,Condition,current_thread
import time

flag = False

cond_var = Condition()

def child_task():
    global flag
    name = current_thread().getName()

    cond_var.acquire()
    if not flag:
        cond_var.wait()
        print(f"{name} received the signal")
    
    cond_var.release()
    print(f"{name} finished")


if __name__ == "__main__":
    thread1 = Thread(target=child_task, name="ChildThread1")
    thread2 = Thread(target=child_task, name="ChildThread2")
    thread3 = Thread(target=child_task, name="ChildThread3")

    thread1.start()
    thread2.start()
    thread3.start()

    cond_var.acquire()
    cond_var.notify_all()
    cond_var.release()

    thread1.join()
    thread2.join()
    thread3.join()

    print("Main thread finished")
# This code demonstrates the use of threading and condition variables in Python.