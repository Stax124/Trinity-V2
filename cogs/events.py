import logging

import discord
from core.config import Configuration
from discord.activity import Activity
from discord.enums import ActivityType
from discord.errors import NotFound
from discord.ext import commands
from discord.ext.commands import AutoShardedBot
from discord.ext.commands.errors import (CommandNotFound,
                                         MissingRequiredArgument)


class Events(commands.Cog):

    def __init__(self, bot: AutoShardedBot):
        @bot.event
        async def on_message(message):
            if not message.author == bot.user:
                if not bot.paused or "unpause" in message.content:
                    await bot.process_commands(message)
                else:
                    await message.channel.send("❌ Paused")

        @bot.event
        async def on_command_error(ctx, error):
            logging.debug(f"Error occured: {error}")
            if isinstance(error, CommandNotFound):
                embed = discord.Embed(
                    colour=0xff0000,
                    description=f'❌ Command not found'
                )
                embed.set_author(name="Status", icon_url=bot.user.avatar_url)
                await ctx.send(embed=embed)
            elif isinstance(error, NotFound):
                logging.debug("Error 404, passing")
                pass
            elif isinstance(error, MissingRequiredArgument):
                logging.debug(error)
                embed = discord.Embed(
                    colour=0xff0000,
                    description=f'❌ Missing required argument(s)'
                )
                embed.set_author(name="Status", icon_url=bot.user.avatar_url)
                await ctx.send(embed=embed)
                pass
            else:
                logging.debug("Error not catched, raising")
                raise error

        @bot.event
        async def on_guild_role_create(role):
            bot.configs[role.guild.id]["income"][role.id] = 0
            logging.info(f"New role added: {role.name}")
            bot.configs[role.guild.id].save()

        @bot.event
        async def on_guild_role_delete(role):
            del bot.configs[role.guild.id]["income"][role.id]
            logging.info(f"Role removed: {role.name}")
            bot.configs[role.guild.id].save()

        @bot.event
        async def on_ready():
            for guild in bot.guilds:
                config = Configuration(guild.id, bot)
                config.load()
                bot.configs[guild.id] = config

            await bot.change_presence(activity=Activity(name=f"{len(bot.guilds)} servers", type=ActivityType.watching))

            for guild in bot.guilds:
                try:
                    bot.configs[guild.id]["loot-table"]
                except:
                    bot.configs[guild.id]["loot-table"] = {}

                for member in guild.members:
                    if not member.id in bot.configs[guild.id]["players"]:
                        logging.info(
                            f"Added {member.display_name} as {member.id}")
                        logging.debug(
                            f"Initializing config files for {member.display_name}")
                        bot.configs[guild.id]["players"][member.id] = {}
                        bot.configs[guild.id]["players"][member.id]["balance"] = bot.configs[guild.id]["default_balance"]
                        bot.configs[guild.id]["players"][member.id]["last-work"] = 0
                        bot.configs[guild.id]["players"][member.id]["xp"] = 0
                        bot.configs[guild.id]["players"][member.id]["level"] = 1
                        bot.configs[guild.id]["players"][member.id]["manpower"] = 0
                        bot.configs[guild.id]["players"][member.id]["upgrade"] = {}
                        bot.configs[guild.id]["players"][member.id]["maxupgrade"] = {}
                        bot.configs[guild.id]["players"][member.id]["player_shop"] = {
                        }
                        bot.configs[guild.id]["players"][member.id]["stats"] = {
                            "diplomacy": 0,
                            "warlord": 0,
                            "intrique": 0,
                            "stewardship": 0,
                            "trading": 0,
                            "bartering": 0,
                            "learning": 0
                        }
                        logging.debug(
                            f"Config files for {member.display_name} initialized")

                        for item in list(bot.configs[guild.id]["upgrade"].keys()):
                            logging.info(
                                f"Added {item} to {member.display_name}")
                            bot.configs[guild.id]["players"][member.id]["upgrade"][item] = 0
                            bot.configs[guild.id]["players"][member.id]["maxupgrade"][item] = bot.configs[guild.id]["maxupgrade"][item]

                    try:
                        bot.configs[guild.id]["players"][member.id]["balance"]
                    except:
                        bot.configs[guild.id]["players"][member.id]["balance"] = bot.configs[guild.id]["default_balance"]
                        logging.info(
                            f"Config: balance => {member.name}({member.id})")

                    try:
                        bot.configs[guild.id]["missions"]
                    except:
                        bot.configs[guild.id]["missions"] = {}
                        logging.info(f"Config: missions => config")

                    try:
                        bot.configs[guild.id]["players"][member.id]["last-work"]
                    except:
                        bot.configs[guild.id]["players"][member.id]["last-work"] = 0
                        logging.info(
                            f"Config: last-work => {member.name}({member.id})")

                    try:
                        bot.configs[guild.id]["players"][member.id]["manpower"]
                    except:
                        bot.configs[guild.id]["players"][member.id]["manpower"] = 0
                        logging.info(
                            f"Config: manpower => {member.name}({member.id})")

                    try:
                        bot.configs[guild.id]["players"][member.id]["xp"]
                    except:
                        bot.configs[guild.id]["players"][member.id]["xp"] = 0
                        logging.info(
                            f"Config: xp => {member.name}({member.id})")

                    try:
                        bot.configs[guild.id]["players"][member.id]["skillpoints"]
                    except:
                        bot.configs[guild.id]["players"][member.id]["skillpoints"] = 0
                        logging.info(
                            f"Config: skillpoints => {member.name}({member.id})")

                    try:
                        bot.configs[guild.id]["players"][member.id]["level"]
                    except:
                        bot.configs[guild.id]["players"][member.id]["level"] = 1
                        logging.info(
                            f"Config: level => {member.name}({member.id})")

                    try:
                        bot.configs[guild.id]["players"][member.id]["upgrade"]
                    except:
                        bot.configs[guild.id]["players"][member.id]["upgrade"] = {}
                        logging.info(
                            f"Config: upgrade => {member.name}({member.id})")

                    try:
                        bot.configs[guild.id]["players"][member.id]["maxupgrade"]
                    except:
                        bot.configs[guild.id]["players"][member.id]["maxupgrade"] = {}
                        logging.info(
                            f"Config: maxupgrade => {member.name}({member.id})")

                    try:
                        bot.configs[guild.id]["players"][member.id]["player_shop"]
                    except:
                        bot.configs[guild.id]["players"][member.id]["player_shop"] = {
                        }
                        logging.info(
                            f"Config: player_shop => {member.name}({member.id})")

                    try:
                        bot.configs[guild.id]["players"][member.id]["inventory"]
                    except:
                        bot.configs[guild.id]["players"][member.id]["inventory"] = {}
                        logging.info(
                            f"Config: inventory => {member.name}({member.id})")

                    try:
                        bot.configs[guild.id]["players"][member.id]["equiped"]
                    except:
                        bot.configs[guild.id]["players"][member.id]["equiped"] = {}
                        logging.info(
                            f"Config: equiped => {member.name}({member.id})")

                    try:
                        bot.configs[guild.id]["players"][member.id]["stats"]
                    except:
                        bot.configs[guild.id]["players"][member.id]["stats"] = {
                            "diplomacy": 0,
                            "warlord": 0,
                            "intrique": 0,
                            "stewardship": 0,
                            "trading": 0,
                            "bartering": 0,
                            "learning": 0
                        }
                        logging.info(
                            f"Config: stats => {member.name}({member.id})")

                for role in guild.roles:
                    if not (role.id in bot.configs[guild.id]["income"]):
                        logging.info(f"{role} added to config")
                        bot.configs[guild.id]["income"][role.id] = 0

                for i in bot.configs:
                    bot.configs[i].save()

        @bot.event
        async def on_member_join(member: discord.Member):
            if not member.id in bot.configs[member.guild.id]["players"]:
                logging.info(
                    f"Added {member.display_name} as {member.id}")

                bot.configs[member.guild.id]["players"][member.id] = {}
                bot.configs[member.guild.id]["players"][member.id]["balance"] = bot.configs[member.guild.id]["default_balance"]
                bot.configs[member.guild.id]["players"][member.id]["last-work"] = 0
                bot.configs[member.guild.id]["players"][member.id]["manpower"] = 0
                bot.configs[member.guild.id]["players"][member.id]["skillpoints"] = 0
                bot.configs[member.guild.id]["players"][member.id]["level"] = 1
                bot.configs[member.guild.id]["players"][member.id]["xp"] = 0
                bot.configs[member.guild.id]["players"][member.id]["upgrade"] = {}
                bot.configs[member.guild.id]["players"][member.id]["maxupgrade"] = {}
                bot.configs[member.guild.id]["players"][member.id]["player_shop"] = {}
                bot.configs[member.guild.id]["players"][member.id]["inventory"] = {}
                bot.configs[member.guild.id]["players"][member.id]["equiped"] = {}
                bot.configs[member.guild.id]["players"][member.id]["stats"] = {
                    "diplomacy": 0,
                    "warlord": 0,
                    "intrique": 0,
                    "stewardship": 0,
                    "trading": 0,
                    "bartering": 0,
                    "learning": 0
                }

                for item in bot.configs[member.guild.id]["upgrade"].keys():
                    logging.info(
                        f"Added {item} to {member.display_name}")
                    bot.configs[member.guild.id]["players"][member.id]["upgrade"][item] = 0
                    bot.configs[member.guild.id]["players"][member.id]["maxupgrade"][item] = bot.configs[member.guild.id]["maxupgrade"][item]
            logging.info(
                f"{member.display_name} ■ {member.id} joined")

            bot.configs[member.guild.id].save()


def setup(bot: AutoShardedBot):
    bot.add_cog(Events(bot))
