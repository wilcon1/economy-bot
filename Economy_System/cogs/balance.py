from .get_balance_ import Economy_System
from discord.ext import commands
from discord import app_commands
import discord


class balance_(commands.Cog):
    def __init__(self,client):
        self.client = client


    @app_commands.command(name="balance", description="Show Your Balance")
    async def _balance(self, interaction: discord.Interaction, member: discord.Member = None):
     member_id = member.id if member else interaction.user.id

     if member and member.bot:
        embed = discord.Embed(title="Sorry!", description="Bot doesn't have money")
        return await interaction.response.send_message(embed=embed, ephemeral=True)

     balance, timestamp = Economy_System.get_balance(self,member_id, interaction.guild.id)
     mention = member.mention if member else interaction.user.mention
     embd = discord.Embed(title="Your balance", description=f"{mention} has {balance} in your account")
     await interaction.response.send_message(embed=embd)







async def setup(client):
     await client.add_cog(balance_(client))