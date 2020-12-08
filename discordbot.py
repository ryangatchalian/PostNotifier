import settings
import post
import discord
import reddit
from discord.ext import commands
import os


is_running = False
search = settings.SUBREDDIT
KEYWORD = settings.REDDIT_KEYWORD

def scrape_sites(subname=search):
    data_list = reddit.reddit_scrape(subname, KEYWORD)
    print(data_list)
    # db = post.create_db_connection('localhost', 'root', settings.MYSQL_PASS, settings.DB_NAME)
    db = post.create_db_connection('us-cdbr-east-02.cleardb.com', 'b8b2fcd9b2a95d', 'dfdbcc4a', 'heroku_3f0223b7f1eb928')
    create_table_query = 'CREATE TABLE IF NOT EXISTS ' + subname + settings.TABLE_SETTINGS
    post.execute_query(db, create_table_query)
    get_row_count = "SELECT COUNT(*) FROM " + subname + " ORDER BY _id DESC LIMIT 1;"
    try:
        first_count = post.pull_data(db, get_row_count)[0][0]
    except:
        first_count = 0
    # Run scrape and store in database.
    if len(data_list) > 1:
        for data in data_list:
            # Since store_post checks if duplicate in database, only append output if not duplicate.
            task = post.store_post(db, subname, data)
    elif len(data_list) == 0:
        pass
    else:
        task = post.store_post(db, subname, data_list[0])
    latest_count = post.pull_data(db, get_row_count)[0][0]
    db.close()
    return first_count, latest_count

client = commands.Bot(command_prefix=".")
token = os.getenv("DISCORD_BOT_TOKEN")

@client.event
async def on_ready():
    await client.change_presence(status = discord.Status.idle, activity = discord.Game("Listening to .help"))
    print("Bot is ready.")

@client.command()
async def scrape(ctx):
    global is_running, search
    is_running = True
    while is_running:
        ids = scrape_sites(search)
        db = post.create_db_connection('us-cdbr-east-02.cleardb.com', 'b8b2fcd9b2a95d', 'dfdbcc4a', 'heroku_3f0223b7f1eb928')
        start, stop = ids
        print(start, stop)
        if stop - start < 1:
            pass
        else:
            output = post.latest_posts(db, search, start, stop)
            print(output)
            for row in output:
                await ctx.send(f'{row[1]} \n {row[2]} \n {row[3]}\n')
        db.close()

@client.command()
async def stop(ctx):
    global is_running
    is_running = False
    await ctx.send("Scraping stopped.")

@client.command()
async def newkey(ctx, keyval):
    global is_running, KEYWORD
    if is_running:
        await ctx.send("Please stop the scrape first!")
    else:
        KEYWORD = keyval
        await ctx.send("Keyword updated. Run the script when ready!")

@client.command()
async def newsub(ctx, keyval):
    global is_running, search
    if is_running:
        await ctx.send("Please stop the scrape first!")
    else:
        search = keyval
        await ctx.send("Keyword updated. Run the script when ready!")


client.run(token)
