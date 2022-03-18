import discord
from discord.ext import commands
from discord.ext.commands.bot import AutoShardedBot
from discord.ext.commands.context import Context


class Management(commands.Cog):
    "Show them who's the boss"

    def __init__(self, bot: AutoShardedBot):
        self.bot = bot

    @commands.command(name="kick", help="Kick a user")
    @commands.has_permissions(administrator=True)
    async def kick_member(self, ctx: Context, member: discord.Member, *,  reason: str = ""):
        await member.kick(reason=reason)
        embed = discord.Embed(
            color=0x00ff00, description=f"{member.mention} was kicked\nReason: `{reason if reason else 'Unknown'}`")
        embed.set_author(name="Kick", icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="ban", help="Ban a user")
    @commands.has_permissions(administrator=True)
    async def ban_member(self, ctx: Context, member: discord.Member, *, reason: str = ""):
        await member.ban(reason=reason)
        embed = discord.Embed(
            color=0x00ff00, description=f"{member.mention} was banned\nReason: `{reason if reason else 'Unknown'}`")
        embed.set_author(name="Ban", icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Management(bot))
