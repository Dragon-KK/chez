from time import sleep
from threading import Thread, Event

class Signal(Event):pass

def asyncdef(name, daemon=True, main_delay=0):
    def decorator(f):
        def wrapper(*args, **kwargs):
            Thread(target=f, args=args, kwargs=kwargs, name=name, daemon=daemon).start()
            sleep(main_delay)
        return wrapper
    return decorator
