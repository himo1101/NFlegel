import asyncpg

async def connect(user:str, pw:str, db:str, min_size: int=1, max_size: int=1):
    pool=await asyncpg.create_pool(
        user=user,
        password=pw,
        database=db,
        min_size=min_size,
        max_size=max_size
    )
    return pool
    
async def create(pool, table):
    await pool.execute(f'CREATE TABLE IF NOT  EXISTS {table}')
    
    
async def fetch(pool, table:str, clumn1: str, value1: str, clumn2: str=None,value2:str=None, clumn3:str=None, value3:str=None):

    if (clumn2 and clumn3) is None:
        content = pool.fetchrow('SELECT * FROM {table} WHERE {column1} = $1', value1)
    elif clumn2 is not None:
        conten= pool.fetchrow('SELECT * FROM {table} WHERE {column1} = $1 AND {column2} = $2', value1, value2)
        
    elif clumn3 is not None:
        content = pool.fetchrow('SELECT * FROM {table} WHERE {column1} = $1 AND {column2}= $2 AND {column3} = $3', value1, value2, value3)
        
    return content
            
async def insert(pool, table:str, clumn1: str, value1: str, clumn2: str=None,value2:str=None, clumn3:str=None, value3:str=None):

    if (clumn2 and clumn3) is None:
            upcontent = await pool.execute('INSERT INTO {table} ({column1}) VALUES ($1)', value1)
            
    elif clumn2 is not None:
        upcontent = await pool.execute('INSERT INTO {table} ({column1}, {clumn2}) VALUES ($1, $2)', value1, value2)
            
    elif clumn3 is not None:
        upcontent = await pool.execute('INSERT INTO {table} ({column1}, {clumn2}, {clumn3})VALUES ($1, $2, $3)', value1, value2, value3)

    return upcontent


async def update(pool, content: str, clumn1: str, value1, clumn2: str=None,value2:str=None, clumn3:str=None, value3:str=None):
    
    if (clumn2 and clumn3) is None:
        await pool.execute('UPDATE {content} SET {clumn}=$1', value1)
        
    elif clumn2 is not None:
        await pool.execute('UPDATE {content} SET {clumn}=$1 WHERE {clumn2}=$2', value1, value2)
    
    elif clumn3 is not None:
        await pool.execute('UPDATE {content} SET {clumn}=$1 WHERE {clumn2}=$2 AND {clumn3}=$3', value1, value2, value3)