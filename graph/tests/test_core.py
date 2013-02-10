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
