import nextcord
from nextcord.ext import commands
bot_channel = 987889101606887425
prefix = '+'

class utils(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['aide'])
    async def help(self, ctx):
        em = nextcord.Embed(title="Commandes d'Elisabeth",color=0x880808)
        em.add_field(name="```-pic [membre]```", value="Permet de récupérer la photo de profil de quelqu'un.", inline=False)
        em.add_field(name="```-banner [membre]```", value="Permet de récupérer la bannière de quelqu'un.", inline=False)
        em.add_field(name="```-level [membre]```", value="Permet d'afficher des informations sur l'XP de quelqu'un.", inline=False)
        em.add_field(name="```-profil [membre]```", value="Donne le profil de quelqu'un.", inline=False)
        em.add_field(name="```-leaderboard / -lb```", value="Permet d'afficher le classement d'XP du serveur.", inline=False)
        em.add_field(name="```-whos```", value="Demande qui est le meilleur joueur sur <champion de LoL>.", inline=False)
        if ctx.channel.id == bot_channel:
          await ctx.send(embed=em)
      
   
def setup(client):
    client.add_cog(utils(client))
