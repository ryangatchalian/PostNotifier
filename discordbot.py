import settings
import post
import discord
import asyncio
import reddit


channel_name = ''
channel_id = ''
is_running = False
search = settings.SUBREDDIT
KEYWORD = settings.REDDIT_KEYWORD

def scrape_sites(subname=search):
    data_list = reddit.reddit_scrape(subname, KEYWORD)
    print(data_list)
    # Connect to server, and create database connection. Create tables and databases if not exist.
    # serverconn = post.create_server_connection('localhost', 'root', settings.MYSQL_PASS)
    # post.create_database(serverconn, settings.DB_NAME)
    # USING HEROKU
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


TOKEN = 'Nzc1NjUwMDU4NTM5NjMwNjMy.X6paaA.pbALCiGjFi2TZN0Qn54uyJeCd9U'

client = discord.Client()

@client.event
async def on_ready():
    print("Bot is ready.")

@client.event
async def on_message(message):
    global channel_name, channel_id, is_running, KEYWORD, search
    if message.author == client.user:
        return

    if 'run here' == message.content:
        channel_name = message.channel
        channel_id = message.channel.id
        print(channel_name)
        await message.channel.send("Posts will be added to this channel. Thanks!")

    if message.content == 'stop scrape':
        is_running = False
        await message.channel.send("Scraping stopped.")

    if message.content == 'start scrape':
        is_running = True
        await message.channel.send("Starting scrape!")
        await start_scrape(message.channel)

    if "key" in message.content:
        msg = message.content
        if is_running:
            await message.channel.send("Please stop the scrape first!")
        else:
            KEYWORD = msg.replace('key ', '')
            print(KEYWORD)
            await message.channel.send("Keyword updated. Run the script when ready!")

    if "-subreddit" in message.content:
        msg = message.content
        if is_running:
            await message.channel.send("Please stop the scrape first!")
        else:
            search = msg.replace('-subreddit ', '')
            await message.channel.send("Subreddit updated. Run the script when ready!")

async def start_scrape(channel):
    global is_running, search
    while is_running:
        ids = scrape_sites(search)
        # db = post.create_db_connection('localhost', 'root', settings.MYSQL_PASS, settings.DB_NAME)
        # USING HEROKU
        db = post.create_db_connection('us-cdbr-east-02.cleardb.com', 'b8b2fcd9b2a95d', 'dfdbcc4a', 'heroku_3f0223b7f1eb928')
        start, stop = ids
        print(start, stop)
        if stop - start < 1:
            pass
        else:
            output = post.latest_posts(db, search, start, stop)
            print(output)
            for row in output:
                await channel.send(f'{row[1]} \n {row[2]} \n {row[3]}\n')
        db.close()
        await asyncio.sleep(300)

client.run(TOKEN)
