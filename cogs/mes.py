from discord.ext import commands as c
from flegelapi import lvl
import discord
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
        mes = await ctx.send('このチャンネルにユーザーが送信したメッセージの数を数えています。')
        async for msg in ctx.channel.history(limit=None):
            if msg.author == ctx.author:
                counter += 1
        await mes.edit(f'貴方は過去にこのチャンネルに{counter}数のメッセージを送りました。')


    @c.command(aliases =["cm"])
    async def channel_message_count(self, ctx):
        counter = 0
        mes = await ctx.send('このチャンネルのメッセージ数を数えています。')
        async for msg in ctx.channel.history(limit=None):
            counter += 1
        
        await mes.edit(f'このチャンネルには{counter}数のメッセージが送られています。')

    
    @c.command(aliases =["sm"])
    async def server_message_count(self, ctx):
        counter = 0
        mes = await ctx.send('このサーバーのメッセージ数を数えています。')
        for channel in ctx.guild.channels:
            async for msg in channel.history(limit=None):
                counter += 1
        
        await mes.edit(f'このサーバーには{counter}数のメッセージが送られています。')
        
        
    @c.command()
    @c.has_permissions(manage_messages = True)
    async def purge(self, ctx, channel: discord.TextChannel=None):
        if channel is None:
            channel= ctx
            
        await channel.purge(limit = limit)