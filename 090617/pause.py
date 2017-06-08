import time
import datetime





def pause(seconds):
    """разобраться как поставить на паузу через какоето время может быть получится завтра) """    
    def decorator(func):
        
        def wrapper(*args, **kwargs):
            print("pause on")
            time.sleep(seconds)
            print("pause off")
            result = func(*args, **kwargs)
           

            return result
        
        return wrapper

    return decorator

@pause(5)
def func():
    n=0

    while n < 100:
        print(n)
        n += 1
func()
