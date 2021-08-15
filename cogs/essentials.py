import datetime
import random
import traceback
from typing import Union

import discord
import DiscordUtils
from discord.ext.commands.bot import AutoShardedBot
import pytz
from core.functions import confirm
from discord.ext import commands
from discord.ext.commands.context import Context


class Essentials(commands.Cog):
    "Esential functions"

    def __init__(self, bot: AutoShardedBot):
        self.bot = bot

    # region Default

    @commands.command(name="purge", help="Delete messages from channel")
    @commands.has_permissions(administrator=True)
    async def purge(self, ctx: Context, messages: int = 100):
        if await confirm(self.bot, ctx, message=f"Clean {messages} messages ?"):
            await ctx.channel.purge(limit=messages)

    @commands.command(name="autorole", help="Set default role after member joins")
    @commands.has_permissions(administrator=True)
    async def autorole(self, ctx: Context, role: Union[discord.Role, None]):
        if role == None:
            self.bot.configs[ctx.guild.id]["autorole"] = None
        else:
            _id = role.id
            self.bot.configs[ctx.guild.id]["autorole"] = _id

        self.bot.configs[ctx.guild.id].save()

        embed = discord.Embed(
            color=0xffff00, description=f"Auto-role set to {role.mention if role != None else 'None'}")
        embed.set_author(name="Auto-role", icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)

    # endregion

    # region Trinity specific
    @commands.command(name="members", help="Show all members: members")
    async def members(self, ctx: Context):
        try:
            e_list = []
            msg = ""
            index = 1
            for user in ctx.guild.members:
                msg += f"{index}. {user.mention} `{user.id}`\n"
                if index == 30:
                    embed = discord.Embed(
                        colour=discord.Colour.from_rgb(255, 255, 0),
                        description=msg
                    )
                    embed.set_author(
                        name="Members", icon_url=self.bot.user.avatar_url)
                    e_list.append(embed)
                    msg = ""
                    index = 1
                else:
                    index += 1

            embed = discord.Embed(
                colour=discord.Colour.from_rgb(255, 255, 0),
                description=msg
            )
            embed.set_author(name="Members", icon_url=self.bot.user.avatar_url)
            e_list.append(embed)

            paginator = DiscordUtils.Pagination.AutoEmbedPaginator(ctx)
            paginator.remove_reactions = True
            await paginator.run(e_list)
        except:
            print(traceback.format_exc())
            await ctx.send(traceback.format_exc())

    @commands.command(name="roles", help="Show all roles: roles")
    async def roles(self, ctx: Context):
        try:
            e_list = []
            msg = ""
            index = 1
            for role in ctx.guild.roles:
                msg += f"{index}. {role.mention}\n"
                if index == 30:
                    embed = discord.Embed(
                        colour=discord.Colour.from_rgb(255, 255, 0),
                        description=msg
                    )
                    embed.set_author(
                        name="Roles", icon_url=self.bot.user.avatar_url)
                    e_list.append(embed)
                    msg = ""
                    index = 1
                else:
                    index += 1

            embed = discord.Embed(
                colour=discord.Colour.from_rgb(255, 255, 0),
                description=msg
            )
            embed.set_author(name="Roles", icon_url=self.bot.user.avatar_url)
            e_list.append(embed)

            paginator = DiscordUtils.Pagination.AutoEmbedPaginator(ctx)
            paginator.remove_reactions = True
            await paginator.run(e_list)
        except:
            print(traceback.format_exc())
            await ctx.send(traceback.format_exc())

    @commands.command(name="roll", help="Roll the dice of x sides: roll <maximal-value: integer>")
    async def roll(self, ctx: Context, value: int):
        try:
            embed = discord.Embed(
                colour=discord.Colour.from_rgb(255, 255, 0),
                description="✅ " + str(random.randint(0, int(value)))
            )
            embed.set_author(name="Roll", icon_url=self.bot.user.avatar_url)
            await ctx.send(embed=embed)
        except:
            print(traceback.format_exc())
            await ctx.send(traceback.format_exc())

    @commands.command(name="time", help="Shows formated time: time")
    async def time(self, ctx: Context):
        try:
            embed = discord.Embed(
                colour=discord.Colour.from_rgb(255, 255, 0),
                description="✅ " +
                datetime.datetime.now(tz=pytz.timezone(
                    'Europe/Prague')).strftime(r"%H:%M:%S, %d/%m/%Y")
            )
            embed.set_author(name="Time", icon_url=self.bot.user.avatar_url)
            await ctx.send(embed=embed)
        except:
            print(traceback.format_exc())
            await ctx.send(traceback.format_exc())

    @commands.command(name="limits", help="Shows upgrade limits for your account: limits")
    async def limits(self, ctx: Context):
        try:
            embed = discord.Embed(
                colour=discord.Colour.from_rgb(255, 255, 0),
                description=f"Limits is deprecated, use {self.bot.configs[ctx.guild.id]['prefix']}shop instead"
            )
            embed.set_author(name="Limits", icon_url=self.bot.user.avatar_url)
            await ctx.send(embed=embed)
        except:
            print(traceback.format_exc())
            await ctx.send(traceback.format_exc())

    @commands.command(name="upgrades", help="Shows the current number of upgrades bought: upgrades")
    async def upgrades(self, ctx: Context):
        try:
            embed = discord.Embed(
                colour=discord.Colour.from_rgb(255, 255, 0),
                description=f"Upgrades is deprecated, use {self.bot.configs[ctx.guild.id]['prefix']}shop instead"
            )
            embed.set_author(
                name="Upgrades", icon_url=self.bot.user.avatar_url)
            await ctx.send(embed=embed)
        except:
            print(traceback.format_exc())
            await ctx.send(traceback.format_exc())

    @commands.command(name="role", help="Your roles: role")
    async def role(self, ctx: Context):
        try:
            msg = ""
            index = 1
            for name in ctx.author.roles:
                msg += f"{name.mention} `{name.id}`\n"
                index += 1
            embed = discord.Embed(
                colour=discord.Colour.from_rgb(255, 255, 0),
                description=msg
            )
            embed.set_author(name="Role", icon_url=self.bot.user.avatar_url)
            await ctx.send(embed=embed)
        except:
            print(traceback.format_exc())
            await ctx.send(traceback.format_exc())

    # endregion


def setup(bot):
    bot.add_cog(Essentials(bot))
