from discord.ext import commands
from discord.ext.commands.bot import AutoShardedBot
from discord.ext.commands.context import Context

class Test(commands.Cog):
    
    def __init__(self, bot: AutoShardedBot) -> None:
        self.bot = bot
        
    @commands.command(name="test")
    @commands.is_owner()
    async def test(self, ctx: Context):
        await ctx.send(type(list(self.bot.configs[ctx.guild.id]["players"].keys())[0]))
        
def setup(bot):
    bot.add_cog(Test(bot))
