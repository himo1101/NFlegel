from flegelapi.pg import default, server
import discord


class User_lvl:
    def __init__(self, pool):
        self.pool=pool
        
        
    async def check_save_date(self, mes: discord.Message):
        
        return await default.fetch(self.pool, 'lvl', 'server_id', mes.guild.id, 'user_id', mes.author.id)
        
        
    async def date_insert(self, mes:discord.Message=None, default_xp:int=0, default_lvl:int=0):
    
        if (server_date:= await self.check_save_date(mes) is None):
            return await pool.execute('INSERT INTO lvl (server_id, user_id, xp, lvl)VALUES ($1, $2, $3, $4)', mes.guild.id, mes.author.id, default_xp,  default_lvl)
     
        
    async def up_xp(self, mes:discord.Message=None, xp:int=1):
        server_date=await self.date_insert(mes)
        
        return await default.update(self.pool, 'lvl', 'xp', server_date['xp']+ xp, 'guild_id', mes.guild.id, 'user_id', mes.author.id)
        
        
        
        
    async def up_lvl(self mes):
        user= await self.check_save_date(mes)
        
        cur_xp=user['xp']
        cur_lvl=user['lvl']
        
        if cur_xp >= round((20 * (cur_lvl ** 9)) / 2):
            await default.update(self.pool, 'lvl', 'lvl', server_date['lvl']+1, 'guild_id', mes.guild.id, 'user_id', mes.author.id)
            user_= self.check_save_date(mes)
            return await embed.default(mes.channel, f'{mes.author.mention}のレベル', 'レベル: {user_["lvl"]} \n 経験値: {user_["xp"]}')
            
        
            
    async def show_lvl(self, ctx, user:discord.Member=None):
        if user is None:
            user=ctx.author
        user_= self.check_save_date(ctx)
        return await embed.default(ctx, f'{user.mention}のレベル', 'レベル: {user_["lvl"]} \n 経験値: {user_["xp"]}')
        