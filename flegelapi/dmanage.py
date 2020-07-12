import discord
class Channel_:
    def __init__(self, name:str=None, category:discord.CategoryChannel=None, channel=None)
        self.name=name
        self.category=category
        self.channel=channel
    async def text(self, ctx):
        if self.category is None:
            new_text=await ctx.guild.create_text_channel(self.name)
        else:
            new_text=await category.create_text_channel(self.name)
        
        return new_text
        
    async def voice(self,ctx):
        if self.category is None:
            new_voice=await ctx.guild.create_voie_channel(self.name)
        else:
            new_voice=await category.create_voice_channel(self.name)
            
        return new_voice
        
    async def delete(self):
        await self.channel.delete()
        
class Role_:
    del __init__(self, name:str=None, role:discord.Role=None):
        self.name=name
        self.role=role
        
    async def create(self, guild):
        
        role = await guild.create_role(name = self.name)
        return role
        
    async def delete(self, guild):
        await self.role.delete() 
        
    async def add(self, member):
        role=await member.add_roles(self.role)
        return role
        
        
    async def remove(self, member):
        role=await member.remove_role(self.role)
        return role
        
        
    async def get_list(self, guild):
        desc = '\n'.join(f'{role.mention}' for role in reversed(guild.roles) if not role.managed)
        embed = discord.Embed(title = '役職一覧', colour = ctx.author.colour, description = desc)
        return embed
    
    async def get_id(self, guild=None):
        if guild is None:
            e= discord.Embed(
                title='役職のID',
                description=f'{self.role.name}:{self.role.id}'
            )
            return e
            
        elif self.role is None:
            e=discord.Embed(
                title='役職ID',
                description=[f'{role.mention}:{role.id}' for role in guild.roles]
                
            return e
            