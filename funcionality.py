from pipe import Pipe
import asyncio

async def to_async(iterable):
    for item in iterable:
        yield item

@Pipe
async def aWhere(iterable, aggregate='all', *filter_funcs):
    aggregate_func = all if aggregate == 'all' else any
    async for item in to_async(iterable):
        if aggregate_func(f(item) for f in filter_funcs):
            yield item


@Pipe
async def aSelect(iterable, *select_funcs):
    async for item in to_async(iterable):
        result = (f(item) for f in select_funcs)
        yield tuple(result) if len(select_funcs) > 1 else result[0]

@Pipe
async def aReduce(iterable, reduce_func, initial=None):
    it = to_async(iterable)
    if initial is None:
        try:
            initial = await it.__anext__()
        except StopAsyncIteration:
            raise TypeError("reduce() of empty sequence with no initial value")
    result = initial
    async for item in it:
        result = reduce_func(result, item)
    return result

@Pipe
async def aGroupby(iterable, key_func):
    groups = {}
    async for item in to_async(iterable):
        key = key_func(item)
        if key not in groups:
            groups[key] = []
        groups[key].append(item)
    for key, group in groups.items():
        yield key, to_async(group)



@Pipe
async def aMap(iterable, *map_funcs):
    # realize individual actions group  (func_map) for items selected into the iterable.
    async for item in to_async(iterable):
        result = await asyncio.gather(*[f(item) for f in map_funcs])
        yield tuple(result) if len(map_funcs) > 1 else result[0]


@Pipe
async def a_do(itemToiterable, *map_funcs):
    # realize individual actions group  (func_map) for one item selected into the iterable.
    result = await asyncio.gather(*[f(itemToiterable[0]) for f in map_funcs])
    yield result

'''
async def square(x):
    return x ** 2

async def cube(x):
    return x ** 3
'''
async def process_data(data):
    '''
    result = [item async for item in data | aSelect(lambda x: x['name'], lambda x: x['age'])]

    result = [item async for item in data | aWhere('all', lambda x: x['gender'] == 'male')
                                          | aSelect(lambda x: x['name'], lambda x: x['age'])
              ]
    result = await (data | Areduce(lambda x, y: x + y))
    result = [(key, [item async for item in group]) async for key, group in data | aGroupby(lambda x: x['gender'])]
    result = [item async for item in data | aMap(double)]
    print(result)
     '''


    result= [item async for item in data | map(square, cube)]
    
    print(result)



data = [1, 2, 3, 4]
asyncio.run(process_data(data))
