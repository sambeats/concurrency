from threading import Thread, Lock

class SingletonMeta(type):
    """
    Metaclass for thread-safe singleton.
    Controls creation via __call__ method.
    """
    _instance = None
    _lock = Lock()

    def __call__(cls, *args, **kwargs):
        # First check without acquiring the lock
        if cls._instance is None:
            with cls._lock:
                # Double-check to ensure only one instance is created
                if cls._instance is None:
                    cls._instance = super().__call__(*args, **kwargs)
        return cls._instance
    

class MySingleton(metaclass=SingletonMeta):
    """
    Example singleton class.
    """
    def __init__(self, value):
        print("Initializing singleton instance")
        self.config = {"some_key": value}

# Usage
def create_instance(id):
    instance = MySingleton(id)
    print(f"Instance {id} created with config: {instance.config}")


if __name__ == "__main__":
    # Create multiple threads to test singleton behavior
    threads = []
    for i in range(5):
        thread = Thread(target=create_instance, args=(i,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    # Check if all threads received the same instance
    print(f"All threads received the same instance: {MySingleton(0) is MySingleton(1)}")