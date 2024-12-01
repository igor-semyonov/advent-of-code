import collections
from timeit import timeit

N = 10_000


def do(i):
    return i > 5


def _gen_expr_comp(data):
    return (i > 5 for i in data)


def _gen_expr_func(data):
    return (do(i) for i in data)


def _map(data):
    return map(do, data)


def _for_comp(data):
    for i in data:
        yield i > 5


def _for_func(data):
    for i in data:
        yield do(i)


def exhaust(iterator):
    # consume iterator at C speed
    collections.deque(iterator, maxlen=0)


print('generators comparison:')
for approach in (
    '_for_comp',
    '_gen_expr_comp',
    '_map',
    '_gen_expr_func',
    '_for_func',
):
    print(f'{approach:<20}', timeit(f'exhaust({approach}(range(1000)))', number=N, globals=locals()))


def _listcomp_comp(data):
    return [i < 5 for i in data]


def _listcomp_func(data):
    return [do(i) for i in data]


def _list_map(data):
    return list(map(do, data))


def _for_append_comp(data):
    result = []
    for i in data:
        result.append(i > 5)
    return result


def _for_append_func(data):
    result = []
    for i in data:
        result.append(do(i))
    return result


print('\nlist creation comparison:')
for approach in (
    '_listcomp_comp',
    '_for_append_comp',
    '_list_map',
    '_listcomp_func',
    '_for_append_func',
):
    print(f'{approach:<20}', timeit(
        f'{approach}(range(1000))', number=N, globals=locals()))
