from discord.ext import commands
import discord

notice= '''
    notice(
        id serial PRIMARY KEY,
        server_id character varying NOT NULL,
        channel_id character varying 
        )'''
class Server(commands.Cog):
    def __init__(self, bot):
        self.bot=bot
        self.pool=bot.pool
        
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        serverid = str(guild.id)
        
        e=discord.Embed(
            title='当botを導入していただきありがとうございます',
            description='このBOTが保存するデータは以下の通りです。同意する場合は下のリアクションを押してください'
        )
        e.add_field(name='prefix',
                            value='server_id',
                            inline=True)
                            
        mes=await guild.owner.send(embed=e)
        await mes.add_reaction('\U0001f44c')
    
        def check(reaction, user):
            return user == guild.owner and str(reaction.emoji) == '\U0001f44c'
        
        reaction, user= await self.bot.wait_for('reaction_add', check=check)
    
        e=discord.Embed(
        title='チャンネルを作成します',
        description='次にbotの通知を送信するチャンネルを作成します。そして下記のデータを保存します')
    
        e.add_field(name='notice',
                            value='server_id, channel_id',
                            inline=True)
                            
        mesn=await guild.owner.send(embed=e)
        def check(reaction, user):
            return user == guild.owner and str(reaction.emoji) == '\U0001f44c'
        
        reaction, user= await self.bot.wait_for('reaction_add', check=check)
        try:
            if not (pg_new_channel := await self.pool.fetch('SELECT * FROM notice WHERE server_id = $1', str(ctx.guild.id))):
                new_channel=await guild.create_text_channel('flegel_channel')
                await self.pool.execute('INSERT INTO notice (server_id, channel_id) VALUES ($1, $2)', str(ctx.guild.id), str(new_channel.id))
                await guild.owner.send('チャンネルの作成に成功しました')
    
        except discord.erros.Forbidden:
            await guild.owner.send('チャンネルの作成に失敗しました')


def setup(bot):
    bot.add_cog(Server(bot))
    bot.add_table(notice)