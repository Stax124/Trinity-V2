import argparse
import json
import logging
import shlex
import traceback

import discord
from core.functions import confirm
from discord.activity import Activity
from discord.enums import ActivityType, Status
from discord.ext import commands
from discord.ext.commands.bot import AutoShardedBot
from discord.ext.commands.context import Context


class Settings(commands.Cog):
    "Settings"

    deltatime = 7200

    def __init__(self, bot: AutoShardedBot):
        self.bot = bot

    # region Default settings

    @commands.command(name="config", help="Dump config for your server")
    @commands.has_permissions(administrator=True)
    async def config(self, ctx: Context):
        await ctx.send(json.dumps(self.bot.configs[ctx.guild.id].config))

    @commands.command(name="version")
    @commands.has_permissions(administrator=True)
    async def config(self, ctx: Context):
        await ctx.send(self.bot.__version__)

    @commands.command(name="prefix")
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx: Context, prefix: str):
        if await confirm(self.bot, ctx, message=f"Set audit channel to {ctx.channel.mention} ?"):
            self.bot.configs[ctx.guild.id]["prefix"] = prefix
            self.bot.configs[ctx.guild.id].save()

    # endregion

    # region Triniy specific settings
    @commands.command(name="pause", help="Show the bot, whos da boss: shutdown", pass_context=True)
    @commands.is_owner()
    async def pause(self, ctx: Context):
        global paused

        confirmed = await confirm(self.bot, ctx, "Pause process ?")
        if not confirmed:
            return

        embed = discord.Embed(
            colour=discord.Colour.from_rgb(255, 255, 0),
            description="✅ Paused..."
        )
        embed.set_author(name="Pause", icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)
        self.bot.paused = True
        logging.info("Paused...")

        await self.bot.change_presence(activity=discord.Game(name=f"Paused"), status=Status.do_not_disturb)

    @commands.command(name="unpause", help="Show the bot, whos da boss: shutdown", pass_context=True)
    @commands.is_owner()
    async def unpause(self, ctx: Context):
        global paused

        confirmed = await confirm(self.bot, ctx, "Unpause process ?")
        if not confirmed:
            return

        embed = discord.Embed(
            colour=discord.Colour.from_rgb(255, 255, 0),
            description="✅ Unpaused..."
        )
        embed.set_author(name="Unpause", icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)
        self.bot.paused = False
        logging.info("Unpaused...")

        await self.bot.change_presence(activity=Activity(name=f"{len(self.bot.guilds)} servers", type=ActivityType.watching))

    @commands.command(name="add-item", pass_context=True, help="Add item to database: add-item [--maxupgrade MAXUPGRADE] [--income INCOME] [--manpower MANPOWER] [--require REQUIRE] name cost")
    @commands.has_permissions(administrator=True)
    async def add_item(self, ctx: Context, *querry):
        fparser = argparse.ArgumentParser()
        fparser.add_argument("name", type=str)
        fparser.add_argument("cost", type=int)
        fparser.add_argument("--maxupgrade", type=int, default=None)
        fparser.add_argument("--income", type=int, default=0)
        fparser.add_argument("--manpower", type=int, default=0)
        fparser.add_argument("--require", type=str, default=None)

        querry = shlex.split(" ".join(querry))

        try:
            fargs = fparser.parse_args(querry)
        except SystemExit:
            return

        for member in self.bot.configs[ctx.guild.id]["players"]:
            self.bot.configs[ctx.guild.id]["players"][member]["maxupgrade"] = {
                **self.bot.configs[ctx.guild.id]["players"][member]["maxupgrade"], **{fargs.name: fargs.maxupgrade}}
            self.bot.configs[ctx.guild.id]["players"][member]["upgrade"] = {
                **self.bot.configs[ctx.guild.id]["players"][member]["upgrade"], **{fargs.name: 0}}

        self.bot.configs[ctx.guild.id]["upgrade"] = {**self.bot.configs[ctx.guild.id]["upgrade"], **{fargs.name: {
            "cost": fargs.cost, "income": fargs.income, "manpower": fargs.manpower, "require": fargs.require}}}
        self.bot.configs[ctx.guild.id]["maxupgrade"] = {**self.bot.configs[ctx.guild.id]["maxupgrade"],
                                                        **{fargs.name: fargs.maxupgrade}}

        embed = discord.Embed(title=fargs.name, color=0xffff00)
        embed.set_author(name="Succesfully added to inventory",
                         icon_url=self.bot.user.avatar_url)
        embed.add_field(name="Cost", value=fargs.cost, inline=True)
        embed.add_field(name="Maximum", value=fargs.maxupgrade,
                        inline=True) if fargs.maxupgrade != None else None
        embed.add_field(name="Income", value=fargs.income,
                        inline=True) if fargs.income != 0 else None
        embed.add_field(name="Manpower", value=fargs.manpower,
                        inline=True) if fargs.manpower != 0 or fargs.manpower != None else None
        await ctx.send(embed=embed)

        self.bot.configs[ctx.guild.id].save()

    @commands.command(name="remove-item", pass_context=True, help="Remove item from database: remove-item <name: str>")
    @commands.has_permissions(administrator=True)
    async def remove_item(self, ctx: Context, item: str):
        try:
            try:
                item
            except:
                embed = discord.Embed(
                    colour=discord.Colour.from_rgb(255, 255, 0),
                    description=f"❌ No name specified"
                )
                embed.set_author(name="Remove item",
                                 icon_url=self.bot.user.avatar_url)
                await ctx.send(embed=embed)
                return

            confirmed = await confirm(self.bot, ctx, f"Remove {item} ?")
            if not confirmed:
                return

            for member in self.bot.configs[ctx.guild.id]["players"]:
                self.bot.configs[ctx.guild.id]["players"][member]["maxupgrade"].pop(
                    item)
                self.bot.configs[ctx.guild.id]["players"][member]["upgrade"].pop(
                    item)

            self.bot.configs[ctx.guild.id]["upgrade"].pop(item)
            self.bot.configs[ctx.guild.id]["maxupgrade"].pop(item)

            embed = discord.Embed(
                colour=discord.Colour.from_rgb(255, 255, 0),
                description=f"✅ Sucessfully removed `{item}`"
            )
            embed.set_author(name="Remove item",
                             icon_url=self.bot.user.avatar_url)
            await ctx.send(embed=embed)
            return
        except:
            print(traceback.format_exc())
            await ctx.send(traceback.format_exc())

        self.bot.configs[ctx.guild.id].save()

    @commands.command(name="deltatime", help="Sets time between allowed !work commands: deltatime <value: int>", pass_context=True)
    @commands.has_permissions(administrator=True)
    async def deltatime(self, ctx: Context, value: int = deltatime):
        try:
            self.bot.configs[ctx.guild.id]["deltatime"] = int(value)

            embed = discord.Embed(
                colour=discord.Colour.from_rgb(255, 255, 0),
                description=f"✅ Deltatime changed to {int(value)} seconds"
            )
            embed.set_author(name="Config", icon_url=self.bot.user.avatar_url)
            await ctx.send(embed=embed)

        except:
            print(traceback.format_exc())
            await ctx.send(traceback.format_exc())
            
        self.bot.configs[ctx.guild.id].save()

# endregion


def setup(bot):
    bot.add_cog(Settings(bot))
