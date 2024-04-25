import discord,os,config
from discord.ext import commands
import psycopg2


client = commands.Bot(command_prefix="!",intents=discord.Intents.all())

tree = client.tree

@client.event
async def setup_hook():
    try:
        for fn in os.listdir("./cogs"):
            if fn.endswith(".py"):
                await client.load_extension(f"cogs.{fn[:-3]}")

    except Exception as error:
        print(error)

@client.event
async def on_ready():
    db = psycopg2.connect(
        host=config.db_host,
        port=config.db_port,
        database=config.db_name,
        user=config.db_user,
        password=config.db_pass
    )
    cur = db.cursor()

    cur.execute("CREATE TABLE IF NOT EXISTS economy(user_id BIGINT , guild_id BIGINT, balance BIGINT,timestamp BIGINT)")

    db.commit()
    db.close()

    synced = await tree.sync()
    print(f"Bot Is Collecting Data...\nCommands {len(synced)} synced\nConnected to the database")








client.run(config.TOKEN)