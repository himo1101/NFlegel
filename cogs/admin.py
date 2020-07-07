from discord.ext import commands, tasks
from contextlib import redirect_stdout
import os
import subprocess
import traceback
import discord
import traceback
import io
import textwrap



class Admin(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None


    def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        return content.strip('` \n')

    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.author)


    @commands.command()
    async def discord_py(self, ctx):
        await ctx.send(discord.__version__)

    @commands.command()
    async def load(self, ctx, module:str, opt:str = None):
        module = f'cogs.{module}'
        if opt is None:
            self.bot.load_extension(module)

        elif opt == 'un':
            self.bot.unload_extension(module)

        elif opt == 're':
            self.bot.reload_extension(module)

        else:
            return await ctx.message.add_reaction('\N{BLACK QUESTION MARK ORNAMENT}')
        
        await ctx.message.add_reaction('\N{WHITE HEAVY CHECK MARK}')

        
    @commands.command()
    async def restart(self, ctx):
        os.system('cals')
        subprocess.run("launc.py", shell=True)
        
    @commands.command()
    async def shutdown(self, ctx):
        await bot.logout()
       

    
    

    async def say_permissions(self, ctx, member):
        permissions = member.guild_permissions
        e = discord.Embed(colour=member.colour)
        avatar = member.avatar_url_as(static_format='png')
        e.set_author(name=str(member), url=avatar)
        allowed, denied = [], []
        for name, value in permissions:
            name = name.replace('_', ' ').replace('guild', 'server').title()
            if value:
                allowed.append(name)
            else:
                denied.append(name)

        e.add_field(name='Allowed', value='\n'.join(allowed))
        e.add_field(name='Denied', value='\n'.join(denied))
        await ctx.send(embed=e)

    @commands.command()
    async def cp(self, ctx):
        """Shows a member's permissions in a specific channel.
        If no channel is given then it uses the current one.
        You cannot use this in private messages. If no member is given then
        the info returned will be yours.
        """
        guild = self.bot.get_guild(619926767821652000)
        channel = self.bot.get_channel(650399901284565023)
        member = ctx.guild.me

        await self.say_permissions(ctx, member)

    @cp.error
    async def load_error(self, ctx, error):
        await ctx.send(f'```py\n{traceback.format_exc()}\n```')

    @commands.command(aliases = ['role_list'])
    async def _list(self, ctx):
        guild = self.bot.get_guild(619926767821652000)
        desc = '\n'.join(f'{role.name} - {role.id}' for role in reversed(guild.roles))
        embed = discord.Embed(title = '役職一覧', colour = ctx.author.colour, description = desc)
        await ctx.send(embed = embed)

    
    @commands.command(name='eval')
    async def _eval(self, ctx, *, body: str = None):
        """Evaluates a code"""
        if body is None:
            return await ctx.send('w')

        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result
        }

        env.update(globals())
        
        body = self.cleanup_code(body)
        stdout = io.StringIO()
        try:
            to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')
        func = env['func']
        
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                self._last_result = ret
                await ctx.send(f'```py\n{value}{ret}\n```')

    @commands.command()
    async def tes_(self, ctx, member):
        await ctx.send(type(member))
def setup(bot):
    bot.add_cog(Admin(bot))