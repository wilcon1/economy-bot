from .get_balance_ import Economy_System
from discord.ext import commands
from discord import app_commands
import discord,psycopg2,config

class leaders(commands.Cog):
    def __init__(self,client):
        self.client = client
    

    #************************ making list of leadrs*****************************
    @app_commands.command(name="leadrslist", description="Show top Users")
    async def _top(self, interaction: discord.Interaction):
      try:  
        embed = discord.Embed(title="top_users"
        ,description="",color=discord.Color.dark_purple())

        embed.set_footer(text=f"requested_by:{interaction.user.display_name}",icon_url=interaction.user.display_avatar.url)

        db = psycopg2.connect(
        host=config.db_host,
        port=config.db_port,
        database=config.db_name,
        user=config.db_user,
        password=config.db_pass
    )
        cur = db.cursor()

        cur.execute("""
      SELECT user_id, balance
      FROM economy
       WHERE guild_id = %s
       ORDER BY balance DESC
       """, (interaction.guild_id,))



        ordried_data = cur.fetchall()

        if len(ordried_data) > 10:
            ordried_data = ordried_data[:10]


         
        db.close()


        if len(ordried_data) == 0:
            embed = discord.Embed(title="Sorry!",description="there is not data")
            return await interaction.response.send_message(embed=embed,ephemeral=True)




        for index,(user_id,balance) in enumerate(ordried_data,start=1):
            embed.add_field(name = f"{index}-{interaction.guild.get_member(user_id).display_name}",value=f"Balance:{balance}")


        await interaction.response.send_message(embed=embed)

      except Exception as e:
        print(e)


async def setup(client):
  await  client.add_cog(leaders(client))