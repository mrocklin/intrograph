from graph.core import *

def test_fninputs():
    def f(x, y):
        return x + y
    assert fninputs(f) == ('x', 'y')

    def f(x, y):
        z = x + y
        return z
    assert fninputs(f) == ('x', 'y')

def test_run():
    dag = {'a': lambda x, y: x + y,
           'm': lambda x, y: x * y,
           'result': lambda a, m: max(a, m),
           'not_run': lambda m, x, result: 1/0}

    assert run(dag, ('result',), x=1, y=2) == (3,)

    ins = {'x': 1,  'y': 2}
    assert run(dag, ('result',), **ins) == (3,)

    assert run(dag, ('a', 'm', 'result'), **ins) == (3, 2, 3)

def test_stats():
    dag = {'n': lambda xs: len(xs),
           'm': lambda xs, n: sum(xs) / n,
           'm2': lambda xs, n: sum([x**2 for x in xs]) / n,
           'v': lambda m, m2: m2 - m**2}

    assert run(dag, ('m', 'm2', 'v'), xs=[1, 2, 3, 6]) == (3, 12, 3)

def test_compile():
    dag = {'a': lambda x, y: x + y,
           'm': lambda x, y: x * y,
           'result': lambda a, m: max(a, m),
           'not_run': lambda m, x, result: 1/0}
    ins = ('x', 'y')
    outs = ('m', 'result')

    fn = compile(dag, ins, outs)
    assert fn(1, 2) == (2, 3)

def test_edges():
    assert set(edges({'a': lambda b: b + 1})) == set([('b', 'a')])
    dag = {'n': lambda xs: len(xs),
           'm': lambda xs, n: sum(xs) / n,
           'm2': lambda xs, n: sum([x**2 for x in xs]) / n,
           'v': lambda m, m2: m2 - m**2}
    assert set(edges(dag)) == set([('xs', 'n'), ('xs', 'm'), ('n', 'm'),
        ('xs', 'm2'), ('n', 'm2'), ('m', 'v'), ('m2', 'v')])

def test_transform():
    dag = {'n': lambda xs: len(xs),
           'm': lambda xs, n: sum(xs) / n,
           'm2': lambda xs, n: sum([x**2 for x in xs]) / n,
           'v': lambda m, m2: m2 - m**2}

    order = list()
    def getfn(dag, var):
        """ Record order of computed variables """
        rawfn = dag[var]
        def newfn(*inputs):
            order.append(var)
            return rawfn(*inputs)
        return newfn
    run(dag, ('v',), xs=[1,2,3], getfn=getfn)

    assert list(order)[0] == 'n'
    assert list(order)[-1] == 'v'

    times = dict()
    import time
    def profile(dag, var):
        rawfn = dag[var]
        def newfn(*inputs):
            start = time.time()
            output = rawfn(*inputs)
            end = time.time()
            times[var] = end - start
            return output
        return newfn

    run(dag, ('v',), xs=[1,2,3], getfn=profile)
    assert set(times.keys()) == set(['n', 'm', 'm2', 'v'])
    assert all(isinstance(v, float) for v in times.values())
