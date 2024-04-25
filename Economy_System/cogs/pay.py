from .get_balance_ import Economy_System
from discord.ext import commands
from discord import app_commands
import discord,psycopg2,config

class pay__(commands.Cog):
    def __init__(self,client):
        self.client = client



    #********************** making pay slash_command ******************************
    @app_commands.command(name="pay", description="give user some money from your balance")
    async def _pay(self, interaction: discord.Interaction, member: discord.Member, amount: int):
        balance1, timestamp1 = Economy_System.get_balance(self,interaction.user.id, interaction.guild.id)
        balance2, timestamp2 = Economy_System.get_balance(self,member.id, interaction.guild.id)

        if member.bot:
            embed = discord.Embed(title="Sorry!",description="Bot doesn't have money")
            return await interaction.response.send_message(embed=embed, ephemeral=True)


        if member.id == interaction.user.id:
            embed = discord.Embed(title="Sorry!",description="You Can't Give Money To Yourself")
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        if amount > balance1:
            embed = discord.Embed(title="Sorry!",description="You Need More Money For This Transfer")
            return await interaction.response.send_message(embed=embed, ephemeral=True)

        db = psycopg2.connect(
        host=config.db_host,
        port=config.db_port,
        database=config.db_name,
        user=config.db_user,
        password=config.db_pass
        )
        cur = db.cursor()


        cur.execute("""
        UPDATE economy
       SET balance = balance - %s
       WHERE user_id = %s AND guild_id = %s
      """, (amount, interaction.user.id, interaction.guild.id))


        cur.execute("""
      UPDATE economy
     SET balance = balance + %s
      WHERE user_id = %s AND guild_id = %s
      """, (amount, member.id, interaction.guild.id))


        db.commit()
        db.close()
        embed = discord.Embed(title="",description=f"{member.mention} now has {balance2 + amount} in their account")
        await interaction.response.send_message(embed=embed)

async def setup(client):
    await client.add_cog(pay__(client))