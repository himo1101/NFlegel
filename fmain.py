from discord.ext import commands
from flegelapi.pg import default, server
from flegelapi.key import get_id
import info
import asyncpg
import asyncio
import traceback

ID=get_id()

cogs = [
    'admin',
    'dManage',
    'information',
    'member_',
    'mes',
    'server',
    'prefix',
    'err'
]

class Flegel_Main(commands.Bot):
     def __init__(self):
         super().__init__(
             command_prefix=self.guild_prefix,
             description=info.desc,
             help_attrs=dict(hidden=True))
             
         self.pg_table = []
         
     async def guild_prefix(self, bot, mes):
         if not (prefixess := await server.fetch('prefix', mes.guild.id)):
             await default.insert('prefix', 'server_id', mes.guild.id, 'new_prefix', [])
             
             await self.pool.execute('UPDATE prefix SET new_prefix = array_append(new_prefix, $1) WHERE server_id=$2', 'f/', str(mes.guild.id))
         if prefixess is None:
             return 'f/'
         
         return prefixess['new_prefix']
             
         
     async def on_ready(self):
        error_channel = self.get_channel(ID.channel.err)
        for cog in cogs:
            try:
                self.load_extension(f"cogs.{cog}")
            except commands.ExtensionAlreadyLoaded:
                pass

            except Exception:
                msg=traceback.format_exc()
                for i in range(0, len(msg), 1092):
                    await error_channel.send(f'```py\n{msg[i:i+1092]}\n```')
        print('起動が完了しました!')
        
        for table in self.pg_table:
             await default.create(self.pool, table)
         
     async def create_db_pool(self):
        self.pool = await default.connect(info.user, info.pw, info.db)
      
     def add_table(self, table):
        self.pg_table.append(table)
       
        
     async def start(self):
        await super().start(info.token)

     def main(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.create_db_pool())
        loop.run_until_complete(self.start())
        loop.close()
        
        
if __name__ == "__main__":
    bot= Flegel_Main()
    bot.main()