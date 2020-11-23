import random
import settings
import post
import discord
import reddit
from discord.ext import commands
import mysql.connector
from mysql.connector import Error


def scrape_sites(website: str, site=settings.REDDIT):
    # Connect to server, and create database connection. Create tables and databases if not exist.
    serverconn = post.create_server_connection('localhost', 'root', settings.MYSQL_PASS)
    post.create_database(serverconn, settings.DB_NAME)
    db = post.create_db_connection('localhost', 'root', settings.MYSQL_PASS, settings.DB_NAME)
    create_table_query = 'CREATE TABLE IF NOT EXISTS ' + site + settings.TABLE_SETTINGS
    post.execute_query(db, create_table_query)

    # Run scrape and store in database. Store
    data_list = reddit.reddit_scrape()
    output_list = []
    if len(data_list) > 1:
        for data in data_list:
            # Since store_post checks if duplicate in database, only append output if not duplicate.
            task = post.store_post(db, site, data)
            if task:
                output_list.append(data)
            else:
                pass
    else:
        task = post.store_post(db, site, data_list[0])
        if task:
            output_list.append(data_list[0])
        else:
            pass
    return output_list
    # print(post.pull_data(db, 'SELECT * FROM ' + site + ' WHERE _id>' + str(last_id)))


def test_function(hi: str):
    output = 'Hello, did you say {}?'.format(hi)
    return output

TOKEN = 'Nzc1NjUwMDU4NTM5NjMwNjMy.X6paaA.pbALCiGjFi2TZN0Qn54uyJeCd9U'

client = discord.Client()


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    brooklyn_99_quotes = [
        'I\'m the human form of the 💯 emoji.',
        'Bingpot!',
        (
            'Cool. Cool cool cool cool cool cool cool, '
            'no doubt no doubt no doubt no doubt.'
        ),
    ]

    if message.content == '99!':
        response = random.choice(brooklyn_99_quotes)
        await message.channel.send(response)

    if message.content == 'hello?':
        # response = test_function('hello?')
        taskscrape_sites('reddit', settings.REDDIT)
        if
        await message.channel.send(response)

async def scraping():
    await client.wait_until_ready()
    task = scrape_sites('reddit', settings.REDDIT)
    if 0 < len(task) < 2:
        message



client.run(TOKEN)
