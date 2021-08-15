import discord
from discord.ext import commands
from discord.ext.commands.bot import AutoShardedBot
from discord.ext.commands.context import Context


class Example(commands.Cog):
    "Example structure, feel free to remove/replace/extend it"

    def __init__(self, bot: AutoShardedBot):
        self.bot = bot

    @commands.command(name="kick")
    @commands.has_permissions(administrator=True)
    async def kick_member(self, ctx: Context, member: discord.Member, *,  reason: str = ""):
        await member.kick(reason=reason)
        embed = discord.Embed(
            color=self.bot.configs[ctx.guild.id]["color"], description=f"{member.mention} was kicked\nReason: `{reason if reason else 'Unknown'}`")
        embed.set_author(name="Kick", icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(name="ban")
    @commands.has_permissions(administrator=True)
    async def ban_member(self, ctx: Context, member: discord.Member, *, reason: str = ""):
        await member.ban(reason=reason)
        embed = discord.Embed(
            color=self.bot.configs[ctx.guild.id]["color"], description=f"{member.mention} was banned\nReason: `{reason if reason else 'Unknown'}`")
        embed.set_author(name="Ban", icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Example(bot))
