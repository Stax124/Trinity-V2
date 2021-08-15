from discord.ext import commands
from discord.ext.commands.bot import AutoShardedBot


class Tasks(commands.Cog):
    "Tasks"

    def __init__(self, bot: AutoShardedBot):
        self.bot = bot

    # TODO - Port all reconnect logic and tasks


def setup(bot):
    bot.add_cog(Tasks(bot))
