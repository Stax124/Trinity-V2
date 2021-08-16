import logging
import re
import traceback

import discord
from core.functions import confirm, levelup_check
from discord.ext import commands
from discord.ext.commands.bot import AutoShardedBot
from discord.ext.commands.context import Context


class Config(commands.Cog):
    "Owner commands"

    def __init__(self, bot: AutoShardedBot):
        self.bot = bot

    @commands.command(name="config-save", help="Save configuration file: config-save", pass_context=True)
    @commands.has_permissions(administrator=True)
    async def config_save(self, ctx: Context):
        try:
            embed = discord.Embed(
                colour=discord.Colour.from_rgb(255, 255, 0),
                description="✅ Config saved"
            )
            embed.set_author(name="Config", icon_url=self.bot.user.avatar_url)
            await ctx.send(embed=embed)
        except:
            print(traceback.format_exc())
            await ctx.send(traceback.format_exc())

        self.bot.configs[ctx.guild.id].save()

    @commands.command(name="config-load", help="Load configuration file for current server: config-load", pass_context=True)
    @commands.has_permissions(administrator=True)
    async def config_load(self, ctx: Context):
        try:
            self.bot.configs[ctx.guild.id].load()

            embed = discord.Embed(
                colour=discord.Colour.from_rgb(255, 255, 0),
                description="✅ Config loaded"
            )
            embed.set_author(name="Config", icon_url=self.bot.user.avatar_url)
            await ctx.send(embed=embed)
        except:
            print(traceback.format_exc())
            await ctx.send(traceback.format_exc())

    @commands.command(name="config", help="Output config directory: config <path> [path]...", pass_context=True)
    @commands.has_permissions(administrator=True)
    async def config_(self, ctx: Context, *message):
        logging.debug(f"{ctx.author.display_name} requested config")
        try:
            message = list(message)
            for i in range(len(message)):
                if re.findall(re.compile(r"[<][@][!][0-9]+[>]"), message[i]) != []:
                    pattern = re.compile(r'[0-9]+')
                    _users = ctx.guild.members
                    _id = int(re.findall(pattern, message[i])[0])
                    for _user in _users:
                        if _user.id == _id:
                            logging.info(
                                f"{message[i]} was replaced by {_user.id}")
                            message[i] = _user.id
                    break

                if re.findall(re.compile(r"[<][@][0-9]+[>]"), message[i]) != []:
                    pattern = re.compile(r'[0-9]+')
                    _users = ctx.guild.members
                    _id = int(re.findall(pattern, message[i])[0])
                    for _user in _users:
                        if _user.id == _id:
                            logging.info(
                                f"{message[i]} was replaced by {_user.id}")
                            message[i] = _user.id
                    break

                if re.findall(re.compile(r"[<][@][&][0-9]+[>]"), message[i]) != []:
                    pattern = re.compile(r'[0-9]+')
                    _roles = ctx.guild.roles
                    _id = int(re.findall(pattern, message[i])[0])
                    for _role in _roles:
                        if _role.id == _id:
                            logging.info(
                                f"{message[i]} was replaced by {_role.id}")
                            message[i] = _role.id
                    break

            msg = ""
            if message == []:
                for item in self.bot.configs[ctx.guild.id].config:
                    msg += f"`{item}`\n"
                embed = discord.Embed(
                    colour=discord.Colour.from_rgb(255, 255, 0),
                    description=msg
                )
                embed.set_author(
                    name="Config", icon_url=self.bot.user.avatar_url)
                await ctx.send(embed=embed)
            else:
                current = self.bot.configs[ctx.guild.id].config
                if type(message) == str:
                    last = message
                else:
                    last = message[-1]
                for word in message:
                    if word == last:
                        try:
                            current = current[last]
                        except KeyError:
                            embed = discord.Embed(
                                colour=discord.Colour.from_rgb(255, 255, 0),
                                description="Not found"
                            )
                            embed.set_author(
                                name="Config", icon_url=self.bot.user.avatar_url)
                            await ctx.send(embed=embed)
                            break
                        try:
                            for name in current:
                                msg += f"`{name}`\n"
                        except:
                            msg += f"`{current}`"
                        embed = discord.Embed(
                            colour=discord.Colour.from_rgb(255, 255, 0),
                            description=msg
                        )
                        embed.set_author(
                            name="Config", icon_url=self.bot.user.avatar_url)
                        await ctx.send(embed=embed)
                        break
                    else:
                        current = current[word]

        except:
            print(traceback.format_exc())
            await ctx.send(traceback.format_exc())

    @commands.command(name="set", help="Change values in config. You rather know what ya doin!: set <path> [path]... { = | < | > } <value>", pass_context=True)
    @commands.has_permissions(administrator=True)
    async def set(self, ctx: Context, *message):
        logging.debug(
            f"{ctx.author.display_name} is setting something in config: {message}")
        try:
            message = list(message)
            for i in range(len(message)):
                if re.findall(re.compile(r"[<][@][!][0-9]+[>]"), message[i]) != []:
                    pattern = re.compile(r'[0-9]+')
                    _users = ctx.guild.members
                    _id = int(re.findall(pattern, message[i])[0])
                    for _user in _users:
                        if _user.id == _id:
                            logging.debug(
                                f"{message[i]} was replaced by {_user.id}")
                            message[i] = _user.id
                    break

                if re.findall(re.compile(r"[<][@][0-9]+[>]"), message[i]) != []:
                    pattern = re.compile(r'[0-9]+')
                    _users = ctx.guild.members
                    _id = int(re.findall(pattern, message[i])[0])
                    for _user in _users:
                        if _user.id == _id:
                            logging.debug(
                                f"{message[i]} was replaced by {_user.id}")
                            message[i] = _user.id
                    break

                if re.findall(re.compile(r"[<][@][&][0-9]+[>]"), message[i]) != []:
                    pattern = re.compile(r'[0-9]+')
                    _roles = ctx.guild.roles
                    _id = int(re.findall(pattern, message[i])[0])
                    for _role in _roles:
                        if _role.id == _id:
                            logging.debug(
                                f"{message[i]} was replaced by {_role.id}")
                            message[i] = _role.id
                    break

            current = self.bot.configs[ctx.guild.id]
            mode = None
            try:
                last = message[message.index("=") - 1]
                mode = "set"
            except:
                try:
                    last = message[message.index(">") - 1]
                    mode = "add"
                except:
                    last = message[message.index("<") - 1]
                    mode = "remove"
            for word in message:
                if word == last:
                    try:
                        if mode == "set":
                            if last in current.keys():
                                current[last] = int(message[-1])
                            else:
                                confirmed = await confirm(self.bot, ctx, f"Not found in config: Create new entry ?")
                                if confirmed:
                                    current[last] = int(message[-1])
                                else:
                                    return
                        elif mode == "add":
                            current[last] += int(message[-1])
                        else:
                            current[last] -= int(message[-1])
                    except:
                        try:
                            if mode == "set":
                                if last in current.keys():
                                    current[last] = float(message[-1])
                                else:
                                    confirmed = await confirm(self.bot, ctx, f"Not found in config: Create new entry ?")
                                    if confirmed:
                                        current[last] = float(message[-1])
                                    else:
                                        return

                            elif mode == "add":
                                current[last] += float(message[-1])
                            else:
                                current[last] -= float(message[-1])
                        except:
                            if last in current.keys():
                                current[last] = message[-1]
                            else:
                                confirmed = await confirm(self.bot, ctx, f"Not found in config: Create new entry ?")
                                if confirmed:
                                    current[last] = message[-1]
                                else:
                                    return

                        finally:
                            mode = None
                    embed = discord.Embed(
                        colour=discord.Colour.from_rgb(255, 255, 0),
                        description="Success"
                    )
                    embed.set_author(
                        name="Set", icon_url=self.bot.user.avatar_url)
                    await ctx.send(embed=embed)
                    break
                else:
                    current = current[word]
            await levelup_check(self.bot, ctx)

        except:
            print(traceback.format_exc())
            await ctx.send(traceback.format_exc())

        self.bot.configs[ctx.guild.id].save()


def setup(bot):
    bot.add_cog(Config(bot))
