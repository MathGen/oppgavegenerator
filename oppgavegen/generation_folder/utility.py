from oppgavegen.decorators import Debugger

@Debugger
def after_equal_sign(s):
    """Returns everything after the last '=' sign of a string."""
    if '=' in s:
        s = s.split("=")
        s = s[len(s)-1]
    return s