class Debugger(object):
    enabled = False
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        if self.enabled:
            print('Entering', self.func.__name__)
            print('    args:', args, kwargs)
            print('Exiting', self.func.__name__)
            print('    result:', self.func(*args, **kwargs))
        return self.func(*args, **kwargs)

Debugger.enabled = False



