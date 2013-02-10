def fninputs(f):
    """ Return names of input variables of a function

    >>> fninputs(lambda x, y: x + y)
    ('x', 'y')
    """
    return f.func_code.co_varnames[:f.func_code.co_argcount]

def run(dag, results, **inputs):
    """ Execute a computation

    >>> dag = {'a': lambda x, y: x + y,
    ...        'm': lambda x, y: x * y,
    ...        'z': lambda a, m: max(a, m)}
    >>> run(dag, ('m', 'z'), x=1, y=2})
    (2, 3)
    """
    knowns = inputs.copy()
    def compute(var):
        if var in knowns:
            return knowns[var]
        else:
            fn = dag[var]
            unknowns = filter(lambda x: x not in knowns, fninputs(fn))
            knowns.update(dict(zip(unknowns, map(compute, unknowns))))
            return fn(*[knowns[inp] for inp in fninputs(fn)])
    return tuple(map(compute, results))
