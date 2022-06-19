import nextcord
import os
import levels
import utils
import users

from nextcord.ext import commands
from webserver import keep_alive


token = os.environ['TOKEN']
cogs = [levels, utils, users]
prefix = '+'


client = commands.AutoShardedBot(command_prefix=prefix, intents = nextcord.Intents.all(), activity = nextcord.Activity(name=f'{prefix}help pour de l\'aide', type=5))

client.remove_command("help")


@client.event
async def on_member_join(member):
  channel = client.get_channel(987889101384601629)
  embed=nextcord.Embed(color=0XFFFFFF, description=f"— Bienvenue {member.mention}!")
  embed.set_author("Nouveau membre",url=member.avatar.url)
  await channel.send(embed=embed)

client.sniped_messages = {}
@client.event
async def on_message_delete(message):
    if message.attachments:
        bob = message.attachments[0]
        client.sniped_messages[message.guild.id] = (bob.proxy_url, message.content, message.author, message.channel.name, message.created_at)
    else:
        client.sniped_messages[message.guild.id] = (message.content,message.author, message.channel.name, message.created_at)

@client.command()
async def snipe(ctx):
    try:
        bob_proxy_url, contents,author, channel_name, time = client.sniped_messages[ctx.guild.id]
    except:
        contents,author, channel_name, time = client.sniped_messages[ctx.guild.id]
    try:
        embed = nextcord.Embed(description=contents , color=0XFFFFFF, timestamp=time)
        embed.set_image(url=bob_proxy_url)
        embed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar.url)
        embed.set_footer(text=f"Supprimé dans : #{channel_name}")
        await ctx.channel.send(embed=embed)
    except:
        embed = nextcord.Embed(description=contents , color=0XFFFFFF, timestamp=time)
        embed.set_author(name=f"{author.name}#{author.discriminator}", icon_url=author.avatar.url)
        embed.set_footer(text=f"Supprimé dans : #{channel_name}")
        await ctx.channel.send(embed=embed)

@client.command(name = 'clear')
@commands.has_permissions(manage_messages = True)
async def clear(ctx , amount=5):
  await ctx.channel.purge(limit=amount + 1)

for i in range(len(cogs)):
    cogs[i].setup(client)
    print('Setup successful.')
    
keep_alive()
client.run(token)
