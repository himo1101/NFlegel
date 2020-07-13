from discord.ext import commands as c
from flegelapi import lvl, embed
import discord

mes_table = """lvl(
    server_id character varying NOT NULL,
    user_id character varying NOT NULL,
    xp integer,
    lvl integer)"""
class Mes(c.Cog):
    def __init__(self, ctx):
        self.bot=bot
        self.pool=bot.pool
        self.lvl= User_lvl(self.pool)
    @c.Cog.listener()
    async def on_message(self, mes):
        await self.lvl.up_xp(mes)
        
        await self.lvl.up_lvl(mes)
        
    @c.command()
    async def show_lvl(self, ctx, user: discord.Member=None):
        await self.lvl.show_lvl(ctx, user)
        
    @c.command(aliases =["um"])
    async def user_message_count(self, ctx):
        counter = 0
        e= discord.Embed(
            description='計算中・・・')
        mes = await ctx.send(embed=e)
        async for msg in ctx.channel.history(limit=None):
            if msg.author == ctx.author:
                counter += 1
        e=discord.Embed(
            title='あなたが過去にこのチャンネルにメッセージを送った数',
            description=counter)
        await mes.edit(embed=e)


    @c.command(aliases =["cm"])
    async def channel_message_count(self, ctx):
        counter = 0
        e= discord.Embed(
            description='計算中・・・')
        mes = await ctx.send(embed=e)
        async for msg in ctx.channel.history(limit=None):
            counter += 1
        
        e=discord.Embed(
            title='このチャンネルにメンバーがメッセージを送った数',
            description=counter)
        await mes.edit(embed=e)
    
    @c.command(aliases =["sm"])
    async def server_message_count(self, ctx):
        counter = 0
        e= discord.Embed(
            description='計算中・・・')
        mes = await ctx.send(embed=e)
        for channel in ctx.guild.channels:
            async for msg in channel.history(limit=None):
                counter += 1
        
        e=discord.Embed(
            title='このサーバーにメンバーがメッセージを送った数',
            description=counter)
        await mes.edit(embed=e)
        
        
    @c.command()
    @c.has_permissions(manage_messages = True)
    async def purge(self, ctx, channel: discord.TextChannel=None):
        if channel is None:
            channel= ctx
            
        await channel.purge(limit = limit)
        
def setup(bot):
    bot.add_cog(Mes(bot))
    bot.add_table(mes_table)