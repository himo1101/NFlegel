async def not_subcommand(ctx):
    member = ctx.author
        e = discord.Embed(
            title = 'サブコマンドが見つかりません。',
            color = member.color,
            timestamp = ctx.message.created_at
        )
        
        e.set_author(
            name = member.name, 
            icon_url = ctx.author.avatar_url
        )
        e.add_field(
            name = f'エラー名',
            value = 'サブコマンドが足りません。',
            inline = False
        )
        e.add_field(
            name = '入力方法',
            value = f'f/(Prefix){ctx.command}　サブコマンド',
            inline = False
        )
        
        return e