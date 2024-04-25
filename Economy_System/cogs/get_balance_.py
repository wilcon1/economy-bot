import discord,psycopg2,random,datetime
from discord import app_commands
from discord.ext import commands
import config


# **************Making cog_class **********************

class Economy_System(commands.Cog):
    def __init__(self,client):
        self.client = client

        
# ******* making get_balance fucition *************
    def get_balance(self,user_id,guild_id):
        db = psycopg2.connect(
        host=config.db_host,
        port=config.db_port,
        database=config.db_name,
        user=config.db_user,
        password=config.db_pass
    )
        cur = db.cursor()

        cur.execute("SELECT balance, timestamp FROM economy WHERE user_id = %s AND guild_id = %s", (user_id, guild_id))
        user_data = cur.fetchone()

        if user_data:
            return user_data[0],user_data[1]

        else:
           cur.execute("INSERT INTO economy (user_id, guild_id, balance, timestamp) VALUES (%s, %s, %s, %s)", (user_id, guild_id, 0, 0))

           db.commit()
           db.close()
           return 0,0








#************setup the bot *******************
async def setup(client):
    await client.add_cog(Economy_System(client))

