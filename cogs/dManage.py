from discord.ext import commands
from flegelapi import command
from flegelapi.dmanage import Channel_, Role_
import discord
import typing
class Channel(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
        
    @commands.group(invoke_without_command=True)
    @commands.has_permissions(manage_channels = True)
    async def channel(self, ctx):
        e=command.not_subcommand(ctx)
        await ctx.send(embed = e)
            
    @channel.command()
    async def text(self, ctx, text:str, category:discord.CategoryChannel=None):
        new_text=await Channel_(name=text, category=category).text(ctx)
            
        await ctx.send(new_text.mention)
        
        
        
    @channel.command()
    async def voice(self, ctx, voice:str, category:discord.CategoryChannel=None):
         new_voice= await Channel_(name=voice, category=category).voice(ctx)
         await ctx.send(new_voice.mention)
        
    @channel.command()
    async def delete(self, ctx, channel: typing.Union[discord.TextChannel, discord.VoiceChannel, discord.CategoryChannel]=None):
        await Channel_(channel=channel).delete()
        
        await ctx.send(f"削除しました")


class Role(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
        
    @commands.group()
    async def role(self, ctx):
        e=command.not_subcommand(ctx)
        await ctx.send(embed = e)    
        
    @role.command()
    async def create(self, ctx, role:str):
        new_role=await Role_(role).create(guild)
        await ctx.send(new_role.mention)
        
    @role.command()
    async def delet(self, ctx, role:discord.Role):
        await Role_(role=role).delete(guild)
        await ctx.send("削除しました")
        
    @role.command()
    async def add(self, ctx, role:discord.Role, member:discord.Member=None):
        if member is None:
            member=ctx.author
            
        await Role_(role=role).add(member)
        await ctx.send('役職を付与しました')
        
    @role.command()
    async def remove(self, ctx, role:discord.Role, member:discord.Member=None):
        if member is None:
            member=ctx.author
            
        await Role_(role=role).remove(member)
        await ctx.send('役職を剥奪しました')
        
    @role.command()
    async def get_list(self, ctx, role:discord.Role):
        e=await Role_(role=role).get_list(ctx.guild)
        await ctx.send(embed=e)
        
    @role.command()
    async def get_id(self, ctx, Role:discord.Role=None):
        e=await Role_(role=role).get_id(guild)
        await ctx.send(embed=e)
        

def setup(bot):
    bot.add_cog(Channel(bot))
    bot.add_cog(Role(bot))