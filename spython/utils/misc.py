import os

def setEnvVar(name, value):
    """Set or unset an environment variable"""
    if value is None:
        if name in os.environ:
            del os.environ[name]
    else:
        os.environ[name] = value

class ScopedEnvVar(object):
    """Temporarly change an environment variable

    Usage:
        with ScopedEnvVar("FOO", "bar"):
            print(os.environ["FOO"]) # "bar"
        print(os.environ["FOO"]) # <oldvalue>
    """
    
    def __init__(self, name, value):
        self.name = name
        self.value = value
        self.oldValue = None
    
    def __enter__(self):
        self.oldValue = os.environ.get(self.name)
        setEnvVar(self.name, self.value)
        return self
    
    def __exit__(self, ex_type, ex_value, traceback):
        setEnvVar(self.name, self.oldValue)
