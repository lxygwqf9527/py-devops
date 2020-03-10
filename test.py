def tracer(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        print(result,func.__name__,args)
        print('%s(%r,%r)->%r'%(func.__name__,args,kwargs,result))
        return result
    return wrapper

@tracer
def fibonacci(n):
    if n in (0,1):
        return n
    return (fibonacci(n-1)+fibonacci(n-2))


fibonacci(3)
help(fibonacci)