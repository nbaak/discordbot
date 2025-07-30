#!/usr/bin/env python3
import asyncio
import discord
import os
from pathlib import Path
from discord.ext import commands

import CONFIG

intents = discord.Intents.default()
intents = discord.Intents(messages=True, guilds=True, message_content=True)
# intents.message_content = True

client = commands.Bot(
    command_prefix=CONFIG.PREFIX,
    intents=intents,
)


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

    try:
        synced = await client.tree.sync()
        print('synced', len(synced), 'from main')
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
    
    
@client.command()
@commands.is_owner()
async def sync(ctx):
    # A Sync Functionm just in case..
    print("sync command")
    synced = await client.tree.sync()
    print(synced)
    await ctx.send(f'Command tree ({len(synced)}) synced.')


async def main():
    current_dir: Path = Path(__file__).resolve().parent
    print(f"Current dir path: {current_dir}")
    os.chdir(current_dir)

    for path_object in os.listdir('./cogs'):
        # load cog from folder
        if os.path.isdir(f'./cogs/{path_object}') and os.path.exists(f'./cogs/{path_object}/cog.py'):
            await client.load_extension(f'cogs.{path_object}.cog')
        
        # load cog from file
        if path_object.endswith('.py') and not path_object.startswith("_"):
            await client.load_extension(f'cogs.{path_object[:-3]}')

    async with client:
        # client.loop.create_task(background_task())
        await client.start(CONFIG.API_TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
