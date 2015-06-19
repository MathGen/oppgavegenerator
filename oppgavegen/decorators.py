def debug(fn):
    """Decorator for use in debugging, prints out function name, args and result"""
    def wrapper(*args):
        result = fn(*args)
        print('{0}{1} : {2}'.format(fn.__name__, args, result))
        return result

    return wrapper