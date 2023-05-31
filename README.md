# Asyncpipe
# Extención de la libreria pipe para generadores y filtros compatibles con asyncio 
async def square(x):
    return x ** 2

async def cube(x):
    return x ** 3

async def main(data):
    result = [item async for item in data | aSelect(lambda x: x['name'], lambda x: x['age'])]
    result = [item async for item in data | aWhere('all', lambda x: x['gender'] == 'male')
                                          | aSelect(lambda x: x['name'], lambda x: x['age'])
              ]
    result = await (data | Areduce(lambda x, y: x + y))
    result = [(key, [item async for item in group]) async for key, group in data | aGroupby(lambda x: x['gender'])]
    result = [item async for item in data | aMap(double)]
    print(result)


data = [1,2,3,4]
asyncio.run(main(data))

     
     
