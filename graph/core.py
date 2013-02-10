def fninputs(f):
    """ Return names of input variables of a function

    >>> fninputs(lambda x, y: x + y)
    ('x', 'y')
    """
    return f.func_code.co_varnames[:f.func_code.co_argcount]

def run(dag, inputs, results):
    """ Execute a computation

    >>> dag = {'a': lambda x, y: x + y,
    ...        'm': lambda x, y: x * y,
    ...        'z': lambda a, m: max(a, m)}
    >>> run(dag, {'x', 1, 'y': 2}, ('m', 'z'))
    (2, 3)
    """
    knowns = inputs.copy()
    def compute(var):
        if var in knowns:
            return knowns[var]
        fn = dag[var]
        for inp in fninputs(fn):
            if inp not in knowns:
                knowns[inp] = compute(inp)
        knowns[var] = fn(*[knowns[inp] for inp in fninputs(fn)])
        return knowns[var]
    return tuple(map(compute, results))
