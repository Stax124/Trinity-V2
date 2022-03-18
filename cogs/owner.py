import logging
import os
import sys
import traceback

import discord
from core.functions import confirm
from discord.activity import Activity
from discord.enums import ActivityType, Status
from discord.ext import commands
from discord.ext.commands.bot import AutoShardedBot
from discord.ext.commands.context import Context


class Owner(commands.Cog):
    "Just for sigma males"

    def __init__(self, bot: AutoShardedBot):
        self.bot = bot

    @commands.command(name="shutdown", help="Terminate the process", pass_context=True)
    @commands.is_owner()
    async def shutdown(self, ctx: Context):
        confirmed = await confirm(self.bot, ctx, "Terminate process ?")
        if not confirmed:
            return

        logging.warning("Shutting down bot")
        embed = discord.Embed(
            colour=0x00ff00,
            description="✅ Shutting down..."
        )
        embed.set_author(name="Shutdown", icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)
        logging.info("Shutting down...")

        await self.bot.change_presence(activity=discord.Game(name=f"Shutting down..."), status=Status.offline)
        sys.exit()

    @commands.command(name="eval", help="Evaluate string", pass_context=True)
    @commands.is_owner()
    async def eval(self, ctx: Context, *, message: str):
        try:
            await ctx.send(eval(message))
        except:
            print(traceback.format_exc())
            await ctx.send(traceback.format_exc())

    @commands.command(name="exec", help="Execute string", pass_context=True)
    @commands.is_owner()
    async def exec(self, ctx: Context, *, message: str):
        await ctx.send(exec(message))

    @commands.command(name="tclear", help="Clear terminal screen", pass_context=True)
    @commands.is_owner()
    async def tclear(self, ctx: Context):
        os.system("cls")

    @commands.command(name="asyncs-on-hold", help="Show active async jobs", pass_context=True)
    @commands.is_owner()
    async def asyncs_on_hold(self, ctx: Context):
        await ctx.send(self.bot.asyncs_on_hold)

    @commands.command(name="update", help="Update the bot", pass_context=True)
    @commands.is_owner()
    async def update_bot(self, ctx: Context):
        if os.system("git pull") == 0:
            await ctx.send("Update successful")
        else:
            await ctx.send("Update failed")

    @commands.command(name="pause", help="Pauses all commands until unpause command is executed", pass_context=True)
    @commands.is_owner()
    async def pause(self, ctx: Context):
        global paused

        confirmed = await confirm(self.bot, ctx, "Pause process ?")
        if not confirmed:
            return

        embed = discord.Embed(
            colour=0x00ff00,
            description="✅ Paused..."
        )
        embed.set_author(name="Pause", icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)
        self.bot.paused = True
        logging.info("Paused...")

        await self.bot.change_presence(activity=discord.Game(name=f"Paused"), status=Status.do_not_disturb)

    @commands.command(name="unpause", help="Unpauses the bot", pass_context=True)
    @commands.is_owner()
    async def unpause(self, ctx: Context):
        global paused

        confirmed = await confirm(self.bot, ctx, "Unpause process ?")
        if not confirmed:
            return

        embed = discord.Embed(
            colour=0x00ff00,
            description="✅ Unpaused..."
        )
        embed.set_author(name="Unpause", icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)
        self.bot.paused = False
        logging.info("Unpaused...")

        await self.bot.change_presence(activity=Activity(name=f"{len(self.bot.guilds)} servers", type=ActivityType.watching))


def setup(bot):
    bot.add_cog(Owner(bot))
