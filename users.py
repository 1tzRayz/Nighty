import nextcord
from datetime import datetime
from nextcord.ext import commands
bot_channel = 987889101606887425
prefix = '+'

class users(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def pic(self, ctx, *, member : nextcord.Member = None):
        member = ctx.author if not member else member
        em = nextcord.Embed(title = member.name + '#' + member.discriminator, color=0XFFFFFF)
        em.set_image(url=member.avatar.url)
        if ctx.channel.id == bot_channel:
            await ctx.send(embed=em)
    
    @commands.command()
    async def banner(self, ctx, *, member : nextcord.Member = None):
        member = ctx.author if not member else member
        req = await self.client.http.request(nextcord.http.Route("GET", "/users/{uid}", uid=member.id))
        banner_id = req["banner"]
        if banner_id:
          if banner_id.startswith("a_"):
            embed = nextcord.Embed(title= member.name + '#' + member.discriminator, color=0XFFFFFF)
            embed.set_image(url=f"https://cdn.discordapp.com/banners/{member.id}/{banner_id}.gif?size=1024")
          else:
            embed = nextcord.Embed(title= member.name + '#' + member.discriminator, color=0XFFFFFF)
            embed.set_image(url=f"https://cdn.discordapp.com/banners/{member.id}/{banner_id}?size=1024")
        if ctx.channel.id == bot_channel:
            await ctx.send(embed=embed)
            
    @commands.command()
    async def profil(self, ctx, *, member: nextcord.Member=None):
        member = ctx.author if not member else member
        create = datetime.strftime(member.created_at, "%d/%m/%Y")
        join = datetime.strftime(member.joined_at, "%d/%m/%Y")
        em = nextcord.Embed(title=f'Profil de {member.name}', color=0XFFFFFF)
        em.set_thumbnail(url=member.avatar.url)
        em.add_field(name="```Informations générales de ton compte :```", value=f'> **Mention** - <@{member.id}> \n > **Pseudonyme** - {member.name} \n > **Discriminant** - #{member.discriminator} \n > **Identifiant** - {member.id} \n > **Création du compte** - {create} ', inline=False)
        em.add_field(name="```Informations relatives au serveur :```", value=f'> **Surnom** - {member.display_name} \n > **Rôle le plus élevé** - <@&{member.top_role.id}> \n > **Arrivée sur le serveur** - {join} ', inline=False)
        req = await self.client.http.request(nextcord.http.Route("GET", "/users/{uid}", uid=member.id))
        banner_id = req["banner"]
  
        if banner_id:
            if banner_id.startswith("a_"):
                url = f'https://cdn.discordapp.com/banners/{member.id}/{banner_id}.gif?size=1024'
                em.set_image(url=url)
            else:
                url = f'https://cdn.discordapp.com/banners/{member.id}/{banner_id}?size=1024'
                em.set_image(url=url)
        if ctx.channel.id == bot_channel:
            await ctx.send(embed=em)
   
def setup(client):
    client.add_cog(users(client))
