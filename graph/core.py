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
    transforms = inputs.get('transforms', [])
    knowns = inputs.copy()
    def compute(var):
        if var in knowns:
            return knowns[var]
        else:
            fn = dag[var]
            unknowns = filter(lambda x: x not in knowns, fninputs(fn))
            knowns.update(dict(zip(unknowns, map(compute, unknowns))))
            newfn = fn
            for transform in transforms:
                newfn = transform(newfn, dag, var)
            return newfn(*[knowns[inp] for inp in fninputs(fn)])
    return tuple(map(compute, results))

def compile(dag, inputs, outputs, transforms=[]):
    """ Build a callable function from a DAG

    >>> dag = {'a': lambda x, y: x + y,
    ...        'm': lambda x, y: x * y,
    ...        'z': lambda a, m: max(a, m)}

    >>> fn = compile(dag, ('x', 'y'), ('m', 'z'))
    >>> fn(1, 2)
    (2, 3)
    """
    return lambda *args: run(dag, outputs, transforms=transforms,
                             **dict(zip(inputs, args)))

def edges(dag):
    """ Variable dependencies within a dag

    returns set of (a, b) where b depends on a
    >>> dag = {'b': lambda a: a + 1,
    ...        'c': lambda a, b: a + b + 1}
    >>> edges(dag)
    {(a, b), (a, c), (b, c)}
    """
    return set((inp, out) for (out, fn) in dag.items() for inp in fninputs(fn))
