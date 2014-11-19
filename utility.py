__author__ = 'madanrp'

def is_variable(x):
    if x[0].islower():
        return True
    else:
        return False

def is_constant(x):
    return not is_variable(x)