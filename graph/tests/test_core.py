from core import *

def test_fninputs():
    def f(x, y):
        return x + y
    assert fninputs(f) == ('x', 'y')

def test_run():
    dag = {'a': lambda x, y: x + y,
           'm': lambda x, y: x * y,
           'result': lambda a, m: max(a, m),
           'not_run': lambda m, x, result: 1/0}

    ins = {'x': 1,  'y': 2}

    assert run(dag, ins, ('result',)) == (3,)
    assert run(dag, ins, ('a', 'm', 'result')) == (3, 2, 3)
