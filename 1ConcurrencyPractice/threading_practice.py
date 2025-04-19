from threading import Thread,current_thread

def thread_task(a,b,c,key1,key2):
    print ("{0} received the arguments: {1}, {2}, {3}, {4}, {5}".format(current_thread().getName(),a,b,c,key1,key2))

myThread = Thread(target=thread_task, name="demoThread", args=(1,2,3), kwargs={'key1': 777, 'key2': 111},daemon=None)
myThread.start()
myThread.join()

class MyTask(Thread):
    def __init__(self):
        Thread.__init__(self,name="MyTaskThread", args=(1,2,3))
    def run(self):
        print ("{0} received the arguments: {1}, {2}, {3}".format(current_thread().getName(),1,2,3))

myTask = MyTask()
myTask.start()
myTask.join()
print("Main thread finished")