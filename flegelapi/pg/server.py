import discord
async def fetch(pool, table:str, server: discord.Guild=None):
    if not (content := pool.fetchrow(f'SELECT * FROM {table} WHERE server_id= $1', server.id)):
        await pool.execute('INSERT INTO {table} (server_id) VALUES ($1)', str(server.id))
    
    return content
    
