from discord.ext import commands
import asyncpg
import traceback
from flegelapi.pg import default, server

prefix_table = '''
        prefix(
            id serial PRIMARY KEY,
            server_id interger NOT NULL,
            new_prefix character varying[] NOT NULL
            )'''
            
            
class Prefix(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pool= bot.pool
        
    @commands.command()
    async def add_prefix(self, ctx, new_prefix: str):
        if not (prefixes := await server.fetch('prefix', 'server_id', ctx.guild.id)):
            await default.insert('prefix', 'server_id', mes.guild.id, 'new_prefix', [])
            return await ctx.send(f'{new_prefix}を新プレフィックスとして登録しました')
            
        if new_prefix not in prefixes[0]['new_prefix']:
            
            await self.pool.execute('UPDATE prefix SET new_prefix = array_append(new_prefix, $1) WHERE server_id=$2', new_prefix, str(ctx.guild.id))
            return await ctx.send(f'{new_prefix}を新プレフィックスとして登録しました')
            
    
        
    @commands.command()
    async def remove_prefix(self, ctx, del_prefix:str):
        if not (prefixes := await server.fetch('prefix', 'server_id', ctx.guild.id)):
            return await ctx.send('このサーバーでカスタムプレフィックスを設定したデータがありません')
            
        if del_prefix in prefixes[0]['new_prefix']:
            await self.pool.execute('UPDATE prefix SET new_prefix = array_remove(new_prefix, $1) WHERE server_id=$2', del_prefix, str(ctx.guild.id))
            return await ctx.send(f'{del_prefix}をプレフィックスから削除しました')
        
        
    @commands.command()
    async def show_prefix(self, ctx):
        if (prefixes := await server.fetch('prefix', 'server_id', ctx.guild.id)):
            await ctx.send(prefixes[0]['new_prefix'])
def setup(bot):
    bot.add_cog(Prefix(bot))
    bot.add_table(prefix_table)
