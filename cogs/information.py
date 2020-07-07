from discord.ext import commands
from datetime import datetime
from flegelapi import command
import discord
import os
import platform


class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.fmt = '{0:%Y/%m/%d - %H:%M:%S}'

    @commands.group()
    async def info(self, ctx):
        e=command.not_subcommand(ctx)
        await ctx.send(embed = e)

    @info.command(aliases = ["u"])
    async def user(self, ctx, user: discord.Member = None):
        """指定されたユーザーの情報を表示します。"""

        async with ctx.typing():
            if user is None:
                user = ctx.author
            status = str(user.status)

            if status == 'online':
                status = 'オンライン'
            elif status == 'offline':
                status = 'オフライン'
            elif status == 'idle':
                status = '退席中'
            elif status == 'dnd':
                status = '起こさないで'

            roles = [role.name for role in user.roles if role.name != '@everyone']
            roles = ', '.join(roles) if roles != [] else 'なし'

            embed = discord.Embed(
                description=f'ユーザー情報: {user.display_name}',
                colour=ctx.author.color
            )
            embed.set_author(name=user.name, icon_url=user.avatar_url)
            embed.set_thumbnail(url=user.avatar_url)

            embed.add_field(
                name='ステータス',
                value=status
            )
            embed.add_field(
                name='サーバー参加日時',
                value=self.fmt.format(user.joined_at)
            )
            embed.add_field(
                name='アカウント作成日時',
                value=self.fmt.format(user.created_at)
            )
            embed.add_field(
                name='役職',
                value=roles
            )
            embed.set_footer(
                text=f'ID: {user.id} | {self.fmt.format(datetime.now())} | requested by {ctx.author.name}'
            )

        await ctx.send(embed=embed)

    @info.command(aliases = ["s"])
    async def server(self, ctx):
        """サーバーの情報を表示します。"""
        async with ctx.typing():
            guild = ctx.guild

            bot = 0
            human = 0

            for member in guild.members:
                if member.bot:
                    bot += 1
                    continue
                human += 1

            embed = discord.Embed(colour=discord.Colour.purple())
            embed.set_author(name=guild.name, icon_url=guild.icon_url)
            embed.set_thumbnail(url=guild.icon_url)
            embed.add_field(
                name='サーバーオーナー',
                value=self.bot.get_user(guild.owner_id)
            )
            embed.add_field(
                name='サーバーリージョン',
                value=str(guild.region).capitalize()
            )
            embed.add_field(
                name='サーバー作成日時',
                value=self.fmt.format(guild.created_at)
            )
            embed.add_field(
                name='チャンネルカテゴリ数',
                value=len(guild.categories)
            )
            embed.add_field(
                name='テキストチャンネル数',
                value=len(guild.text_channels)
            )
            embed.add_field(
                name='ボイスチャンネル数',
                value=len(guild.voice_channels)
            )
            embed.add_field(
                name='メンバー数',
                value=guild.member_count
            )
            embed.add_field(
                name='Bot数',
                value=bot
            )
            embed.add_field(
                name='ユーザー数',
                value=human
            )
            embed.set_footer(
                text=f'ID: {guild.id} | {self.fmt.format(datetime.now())} | requested by {ctx.author.name}'
            )

        await ctx.send(embed=embed)

    @info.command()
    async def bot(self, ctx):
        """Botの情報を表示します。"""
        async with ctx.typing():
            
            _platform = platform.platform()
            servers = len(self.bot.guilds)
            members = 0
            for guild in self.bot.guilds:
                members += guild.member_count

            embed = discord.Embed(
                title=':information_source: **BOT情報**',
                colour=discord.Colour.purple()
            )
            embed.set_footer(
                text=f'{self.fmt.format(datetime.now())} | requested by {ctx.author.name}'
            )
            embed.set_thumbnail(url=self.bot.user.avatar_url)
            ten = ':black_small_square:'
            desc = (
                f'{ten} **Bot名**: {self.bot.user.name}\n'
                f'{ten} **ID**: {self.bot.user.id}\n'
                f'{ten} **プラットフォーム**: {_platform}\n'
                f'{ten} **APIラッパー**: discord.py - {discord.__version__}\n'
                f'{ten} **稼働中サーバー**: {servers}サーバー\n'
                f'{ten} **総メンバー**: {members}'
            )
            embed.description = desc

        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Information(bot))