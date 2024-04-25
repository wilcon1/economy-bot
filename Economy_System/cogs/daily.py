from .get_balance_ import Economy_System
from discord.ext import commands
from discord import app_commands
import discord,config,datetime,random,psycopg2
class dialy_(commands.Cog):
    def __init__(self,client): 
     self.client = client
#   *****************daily button**********************************


    class dailybutton(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)


        @discord.ui.button(label="daily",emoji="💸",style=discord.ButtonStyle.success)
        async def daily(self,interaction:discord.Interaction,Button : discord.ui.Button):
           user_balance,timestamp = Economy_System.get_balance(self,interaction.user.id,interaction.guild.id)
           hours = int((datetime.datetime.utcnow().timestamp() - timestamp) / 3600) 
           minutes = int((datetime.datetime.utcnow().timestamp() - timestamp) / 60) % 60
           seconds = int(datetime.datetime.utcnow().timestamp() - timestamp) % 60

           if not timestamp == 0:
             if int(datetime.datetime.utcnow().timestamp() - timestamp) / 3600 < 24:
                embd = discord.Embed(title="Sorry!",description=f"You can't use this command after {hours}h, {minutes}m, and {seconds}s")
                return await interaction.response.send_message(embed=embd)


           random_value = random.randint(1000,3000)

           user_balance += random_value

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
            SET balance = %s, timestamp = %s
             WHERE user_id = %s AND guild_id = %s
              """, (user_balance, datetime.datetime.utcnow().timestamp(), interaction.user.id, interaction.guild.id))

           db.commit()
           db.close()
           em = discord.Embed(title="daily cliaming",description=f"Added {random_value} To Your Account , You Now Have {user_balance}")
           await interaction.response.send_message(embed=em)
    #*******************daily slash_command**************************


    @app_commands.command(name="daily",description="get random balance")
    async def _daily(self,interaction:discord.Interaction):
     emb = discord.Embed(title="claim your daily coins",description="tap the button to cliam your coins")
     view = dialy_.dailybutton()
     await interaction.response.send_message(view=view,embed=emb)

           
async def setup(client):
    await client.add_cog(dialy_(client))