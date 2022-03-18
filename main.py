import argparse
import logging
import os

import discord
from discord.ext import commands
from discord.ext.commands import AutoShardedBot
from discord.ext.commands.context import Context
from discord.ext.commands.errors import (ExtensionAlreadyLoaded,
                                         ExtensionNotFound, ExtensionNotLoaded)
from pretty_help import PrettyHelp

from core.config import Configuration

import rich.traceback
import coloredlogs

rich.traceback.install()

# region Parser
parser = argparse.ArgumentParser(
    prog="Trinity", description="Economy discord bot made in python")
parser.add_argument("-l", "--logging",  default="INFO",
                    choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], help="Choose level of logging")
parser.add_argument("-f", "--file", type=str, help="Filename for logging")
parser.add_argument("--token", default=os.environ["TRINITY"], type=str,
                    help="Discord API token: Get yours at https://discord.com/developers/applications")
args = parser.parse_args()
# endregion


# region Logging
loglevels = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL:": logging.CRITICAL
}

coloredlogs.install(
    level=loglevels[args.logging], fmt='%(levelname)s | %(asctime)s | %(name)s |->| %(message)s', datefmt=r"%H:%M:%S"
)

if args.file:
    logging.info("Logging to file: {}".format(args.file))
    logger = logging.getLogger()
    fh = logging.FileHandler(filename=args.file, mode="w", encoding='utf-8')
    fh.setFormatter(logging.Formatter(
        fmt='%(levelname)s | %(asctime)s | %(name)s |->| %(message)s'))
    fh.setLevel(loglevels[args.logging])
    logger.addHandler(fh)
# endregion

default_extensions = ["cogs."+i.replace(".py", "")
                      for i in os.listdir("cogs") if i.endswith(".py")]

if not os.path.exists("config"):
    os.makedirs("config")


def get_prefix(bot, msg):
    return commands.when_mentioned_or(bot.configs[msg.guild.id]["prefix"])(bot, msg)


class Bot(AutoShardedBot):
    def __init__(self):
        super().__init__(
            command_prefix=get_prefix,
            help_command=PrettyHelp(
                color=0xffff00, show_index=True, sort_commands=True),
            intents=discord.Intents.all()
        )
        self.paused = False
        self.configs = {}
        self.asyncs_on_hold = []
        self.__version__ = "0.0.1alpha"


bot = Bot()


@bot.command(name="reload", help="Reloads an extension")
@commands.is_owner()
async def reload_extension(ctx: Context, extension: str):
    try:
        bot.reload_extension("cogs."+extension)
        logging.info(f"{extension} reloaded")
        embed = discord.Embed(
            color=0x00ff00, description=f"{extension} reloaded")
        embed.set_author(name="Reload", icon_url=bot.user.avatar_url)
    except ExtensionNotFound:
        logging.error(f"{extension} not found")
        embed = discord.Embed(
            color=0xff0000, description=f"{extension} not found")
        embed.set_author(name="Reload", icon_url=bot.user.avatar_url)

    await ctx.send(embed=embed)


@bot.command(name="load", help="Loads an extension")
@commands.is_owner()
async def load_extension(ctx: Context, extension: str):
    try:
        bot.load_extension("cogs."+extension)
        logging.info(f"{extension} loaded")
        embed = discord.Embed(
            color=0x00ff00, description=f"{extension} loaded")
        embed.set_author(name="Load", icon_url=bot.user.avatar_url)
    except ExtensionAlreadyLoaded:
        logging.warn(f"{extension} already loaded")
        embed = discord.Embed(
            color=0xff0000, description=f"{extension} already loaded")
        embed.set_author(name="Load", icon_url=bot.user.avatar_url)
    except ExtensionNotFound:
        logging.error(f"{extension} not found")
        embed = discord.Embed(
            color=0xff0000, description=f"{extension} not found")
        embed.set_author(name="Load", icon_url=bot.user.avatar_url)

    await ctx.send(embed=embed)


@bot.command(name="unload", help="Unloads an extension")
@commands.is_owner()
async def unload_extension(ctx: Context, extension: str):
    try:
        bot.unload_extension("cogs."+extension)
        logging.info(f"{extension} unloaded")
        embed = discord.Embed(
            color=0x00ff00, description=f"{extension} unloaded")
        embed.set_author(name="Unload", icon_url=bot.user.avatar_url)
    except ExtensionNotFound:
        logging.error(f"{extension} not found")
        embed = discord.Embed(
            color=0xff0000, description=f"{extension} not found")
        embed.set_author(name="Unload", icon_url=bot.user.avatar_url)
    except ExtensionNotLoaded:
        logging.error(f"{extension} not found")
        embed = discord.Embed(
            color=0xff0000, description=f"{extension} exists, but is not loaded")
        embed.set_author(name="Unload", icon_url=bot.user.avatar_url)

    await ctx.send(embed=embed)


@bot.command(name="reload-all", help="Reloads all extensions")
@commands.is_owner()
async def reload_all_extensions(ctx: Context):
    all_extensions = ["cogs."+i.replace(".py", "")
                      for i in os.listdir("cogs") if i.endswith(".py")]

    ok = True

    for extension in all_extensions:
        try:
            bot.reload_extension(extension)
            logging.info(f"{extension} reloaded")
        except ExtensionNotFound:
            ok = False
            logging.error(f"{extension} not found")
            embed = discord.Embed(
                color=0xff0000, description=f"{extension} not found")
            embed.set_author(name="Reload All", icon_url=bot.user.avatar_url)

    if ok:
        embed = discord.Embed(
            color=0x00ff00, description=f"All extensions reloaded")
        embed.set_author(name="Reload All", icon_url=bot.user.avatar_url)

    await ctx.send(embed=embed)

if __name__ == "__main__":
    for extension in default_extensions:
        bot.load_extension(extension)
        logging.info(f"{extension} loaded")

    bot.run(os.environ["TRINITY"], reconnect=True)
