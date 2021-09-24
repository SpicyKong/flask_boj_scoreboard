from functools import wraps

    
def deco(func):
    def deco_func(*args, **kwargs):
        print('@@@decorated!')
        return func(*args, **kwargs)
    return deco_func

@deco
def return_hi(something):
    return something

print(return_hi('helo'))