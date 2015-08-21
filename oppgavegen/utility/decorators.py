### This file should be used for holding various decorators used in the project ###

class Debugger(object):
    """A debugger decorator, will print args in and out of every function with the decorator"""
    enabled = False  # Set this to True to enable the decorator.
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



