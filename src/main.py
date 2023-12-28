#!/usr/bin/env python3
import asyncio
import discord
import os
from discord.ext import commands

import CONFIG

intents = discord.Intents.default()
intents = discord.Intents(messages=True, guilds=True)
intents.message_content = True

client = commands.Bot(
    command_prefix=CONFIG.PREFIX,
    intents=intents
)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

    try:
        synced = await client.tree.sync()
        print('synced', len(synced))
    except Exception as e:
        print(e)


@client.command()
@commands.is_owner()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')


@client.command()
@commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')


@client.command()
@commands.is_owner()
async def reload(ctx, extension):
    client.reload_extension(f'cogs.{extension}')


async def main():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.{filename[:-3]}')

    async with client:
        # client.loop.create_task(background_task())
        await client.start(CONFIG.API_TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
