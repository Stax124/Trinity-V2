import json
import logging
from discord.ext import commands
from discord.ext.commands.bot import AutoShardedBot


class Fallback(commands.Cog):
    "Fallback for config"

    def __init__(self, bot: AutoShardedBot):
        self.bot = bot
        self.bot.fallback = self._load_fallback()

    def _load_fallback(self) -> dict:
        logging.info("Loading fallback")
        return json.load(open("./core/fallback.json", "r"))

    @commands.command(name="fallback-load")
    @commands.is_owner()
    async def load_fallback(self, ctx: commands.Context):
        self.bot.fallback = self._load_fallback()
        await ctx.send("Fallback loaded")


def setup(bot):
    bot.add_cog(Fallback(bot))
