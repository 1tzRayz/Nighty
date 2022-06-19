import nextcord
import os
import asyncio
from nextcord.ext import commands
from pymongo import MongoClient

 
bot_channel = 987889101606887425
talk_channels = [987889101384601629,987889101606887424,987889101606887425,987889101606887426,987889101606887427,987889101606887432,987889101892091969,987889101892091970,987889101892091971,987889101892091972]
 
cluster = MongoClient("mongodb+srv://ray:admin@nightydb.gs4gli4.mongodb.net/?retryWrites=true&w=majority")
 
collection_name = cluster["niquetamere"]["ptdr"] 
 
class levels(commands.Cog):
    def __init__(self, client):
        self.client = client
 
    @commands.Cog.listener()
    async def on_ready(self):
      print("Online!")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id in talk_channels:
            stats = collection_name.find_one({"id":message.author.id})
            if not message.author.bot:
                if stats is None:
                    newuser = {"id" : message.author.id, "xp" : 0}
                    collection_name.insert_one(newuser)
                else:
                    xp = stats["xp"] + 1
                    collection_name.update_one({"id":message.author.id}, {"$set":{"xp":xp}}) 
                    lvl = 0
                    while True:
                        if xp < ((50*(lvl**2))+(50*lvl)):
                            break
                        lvl += 1
                    xp -= ((50*((lvl-1)**2))+(50*(lvl-1)))
                    if xp == 0:
                        await message.reply(f"Bravo, tu viens de passer au niveau {lvl} !")
                              
    @commands.command(aliases=['xp', 'level', 'Rank'])
    async def rank(self, ctx, member : nextcord.User = None):
      member = ctx.author if not member else member
      if ctx.channel.id in bot_channel:
            stats = collection_name.find_one({"id" : member.id})
            if stats is None:
                embed = nextcord.Embed(color=0XFFFFFF,description="Tu n'as envoyé aucun message, tu ne possèdes donc pas d'XP !")
                await ctx.channel.send(embed=embed)
            else:
                xp = stats["xp"]
                lvl = 0
                rank = 0
                while True:
                        if xp < ((50*(lvl**2))+(50*lvl)):
                            break
                        lvl += 1
                xp -= ((50*((lvl-1)**2))+(50*(lvl-1)))
                boxes = int((xp/(200*((1/2) * lvl)))*20)
                rankings = collection_name.find().sort("xp",-1) 
                for x in rankings:
                    rank += 1
                    if stats["id"] == x["id"]:
                        break
                embed = nextcord.Embed(color=0XFFFFFF,title="Information sur l'XP de {}".format(member.name))
                embed.add_field(name="Pseudonyme", value=member.mention, inline=True)
                embed.add_field(name="XP", value=f"{xp}/{int(200*((1/2)*lvl))}", inline=True)
                embed.add_field(name="Niveau", value=f"{lvl}", inline=True)
                embed.add_field(name="Barre de progression :", value=boxes * ":blue_square:" + (20-boxes) * ":white_large_square:", inline=False)
                embed.set_thumbnail(url=member.avatar.url)
                await ctx.channel.send(embed=embed)

    @commands.command(aliases=['lb', 'classement', 'Lb', 'Leaderboard'])
    async def leaderboard(self, ctx):
      rankings = collection_name.find().sort("xp",-1) 
      i = 1
      embed = nextcord.Embed(color=0XFFFFFF,title="Classement du serveur :")
      for x in rankings:
        try:
          temp = ctx.guild.get_member(x["id"])
          tempxp = x["xp"]
          embed.add_field(name=f"``⭐ {i} :`` {temp.name}", value=f"*XP Total :* {tempxp}", inline=False)
          i += 1
        except:
          pass
        if i == 11:
          break
        if ctx.channel.id == bot_channel:
          await ctx.channel.send(embed=embed)


def setup(client):
    client.add_cog(levels(client))
