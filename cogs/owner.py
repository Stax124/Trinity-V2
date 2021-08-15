import logging
import os
import sys

import discord
from core.functions import confirm
from discord.enums import Status
from discord.ext import commands
from discord.ext.commands.bot import AutoShardedBot
from discord.ext.commands.context import Context


class Owner(commands.Cog):
    "Owner commands"

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
            colour=discord.Colour.from_rgb(255, 255, 0),
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
        await ctx.send(eval(message))

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


def setup(bot):
    bot.add_cog(Owner(bot))
