from discord import Embed

async def default(channel, title:str, desc:str):
    e=Embed(
        title=title,
        description=desc)
     
     emes= await channel.send(embed=e)
    return emes