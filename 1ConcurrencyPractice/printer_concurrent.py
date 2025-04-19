from threading import Thread,Condition
import time


def printer_thread_func():
    global prime_holder
    global found_prime

    while not exit_prog:

        cond_var.acquire()
        while not found_prime and not exit_prog:
            cond_var.wait()
        cond_var.release()

        if not exit_prog:
            print(prime_holder)

            prime_holder = None

            cond_var.acquire()
            found_prime = False
            cond_var.notify()
            cond_var.release()


def is_prime(num):
    if num == 2 or num == 3:
        return True

    div = 2

    while div <= num / 2:
        if num % div == 0:
            return False
        div += 1

    return True


def finder_thread_func():
    global prime_holder
    global found_prime

    i = 1

    while not exit_prog:

        while not is_prime(i):
            i += 1
            # Add a timer to slow down the thread
            # so that we can see the output
            time.sleep(.01)

        prime_holder = i

        cond_var.acquire()
        found_prime = True
        cond_var.notify()
        cond_var.release()

        cond_var.acquire()
        while found_prime and not exit_prog:
            cond_var.wait()
        cond_var.release()

        i += 1

if __name__ == "__main__":
    print("Starting the threads")
    cond_var = Condition()
    found_prime = False
    prime_holder = None
    exit_prog = False

    printerThread = Thread(target=printer_thread_func)
    printerThread.start()

    finderThread = Thread(target=finder_thread_func)
    finderThread.start()

    # Let the threads run for 3 seconds
    time.sleep(3)

    # Let the threads exit
    exit_prog = True

    cond_var.acquire()
    cond_var.notify_all()
    cond_var.release()

    printerThread.join()
    finderThread.join()
