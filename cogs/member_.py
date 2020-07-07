from discord.ext import commands
from flegelapi import pg
from distutils.util import strtobool

member_table= """ member_(
    id serial PRIMARY KEY,
    server_id interger NOT NULL,
    role_ld interger,
    channel_id interger,
    custom_mes character varying DEFAULT が入出しました。,
    on_off boolean DEFAULT False)"""
    

class Member_(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.pool=bot.pool
        
    @commands.command()
    async def enable(self, ctx, enable:str='on'):
        try:
            result_enable=strtobool(enable)
        except ValueError:
            return await ctx.send(f'{enable}は正常な値ではありません')
        
        before_content=await pg.server.fetch(self.pool, 'member_', ctx.guild)
        
        await pg.default.update(self.pool, 'member_', 'on_off', result_enable, 'server_id', ctx.guild.id)
        
        await embed.default(ctx, 'enable change', f'{before_content} -> {"有効" if enable else "無効"}化')
        
        
    @commands.command()
    async def add_mrole(self, ctx, role: discord.Role=None):
        if role is None:
            return await ctx.send('役職が指定されていません')
        before_content= await pg.server.fetch(self.pool, 'member', ctx.guild)
        
        await pg.default.update(self.pool, 'member_', 'role_id', role.id, 'server_id', ctx.guild.id)
        
        await embed.default(ctx, 'role  change', f'{before_content} -> {role.name}')
        
    @commands.command()
    async def add_channel(self, ctx, channel:discord.TextChannel=None):
        if channel is None:
            return await ctx.send('チャンネルが指定されていません')
            
        before_content=await pg.server.fetch(self.pool, 'member_', ctx.guild)
        
        await pg.default.update(self.pool, 'member_', 'channel_id', channel, 'server_id', ctx.guild.id)
        
        await embed.default(ctx, 'channel  change', f'{before_content} -> {channel.mention}')
    
    @commands.command()
    async def add_mes(self, ctx, mes:str=None):
        if mes is None:
            return await ctx.send('メッセージが指定されていません')
            
        before_content=await pg.server.fetch(self.pool, 'member_', ctx.guild)
        
        await pg.default.update(self.pool, 'member_', 'custom_mes', mes, 'server_id', ctx.guild.id)
        
        await embed.default(ctx, 'custom message change', f'{before_content} -> {mes}')
        
        
    @commands.Cog.listener()
    async def on_member_join(self, member):
        
        server_date=await pg.server.fetch(self.pool, 'member_', ctx.guild)
        
        if server_date['on_off']== False:
            return
            
        role= member.guild.get_role(int(server_date['role_id']))
        await member.add_roles(role)
        
        status = str(member.status)

        if status == 'online':
            status = 'オンライン'
        elif status == 'offline':
            status = 'オフライン'
        elif status == 'idle':
            status = '退席中'
        elif status == 'dnd':
            status = '起こさないで'

        roles = [role.name for role in member.roles if role.name != '@everyone']
        roles = ', '.join(roles) if roles != [] else 'なし'

        e = discord.Embed(
            title = '新しい人が来ました。',
            description=f'ユーザー情報: {user.display_name}',
            colour=discord.Colour.purple()
        )
        e.set_author(name=member.name, icon_url=member.avatar_url)
        e.set_thumbnail(url=member.avatar_url)

        e.add_field(
            name='ステータス',
            value=status
        )
        e.add_field(
            name='サーバー参加日時',
            value=self.fmt.format(member.joined_at)
        )
        e.add_field(
            name='アカウント作成日時',
            value=self.fmt.format(member.created_at)
        )
        e.add_field(
            name='役職',
            value=roles
        )
        if server_date['custom_mes'] is not None:
            e.set_footer(
                text=f'ID: {user.id} '
            )
        else:
            e.set_footer(
                text= server_date['custom_mes']
            )
        
        channel= self.bot.get_channel(int(server_date['channel_id']))
        await channel.send(embed=e)
        
        
def setup(bot):
    bot.add_cog(Member_(bot))
    bot.add_table(member_table)
        