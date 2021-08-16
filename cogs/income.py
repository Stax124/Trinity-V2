import logging
import traceback

import discord
import DiscordUtils
from discord.ext import commands
from discord.ext.commands.bot import AutoShardedBot
from discord.ext.commands.context import Context
from discord.utils import get


class Income(commands.Cog):
    "Income commands"

    def __init__(self, bot: AutoShardedBot):
        self.bot = bot

    @commands.command(name="income-calc", help="Calculate income: income <populace>")
    async def income_calc(self, ctx: Context, population: int = 0):
        logging.debug(
            f"{ctx.author.display_name} requested income calc of {population}")
        try:
            embed = discord.Embed(
                colour=0x00ff00,
                description=f"Income: {int((int(population) * 0.01 * 0.4 / 6)):,}{self.bot.configs[ctx.guild.id]['currency_symbol']}".replace(
                    ",", " ")
            )
            embed.set_author(name="Income calculator",
                             icon_url=self.bot.user.avatar_url)
            await ctx.send(embed=embed)
        except:
            print(traceback.format_exc())
            await ctx.send(traceback.format_exc())

    @commands.command(name="income", help="Shows your income: income")
    async def income(self, ctx: Context):
        logging.debug(f"Displaying income of {ctx.author.display_name}")
        try:
            income = 0
            for role in ctx.author.roles:
                try:
                    if self.bot.configs[ctx.guild.id]["income"][role.id] != 0:
                        income += self.bot.configs[ctx.guild.id]["income"][role.id]
                    else:
                        logging.debug(f"Excluding: {role.name}")
                except:
                    embed = discord.Embed(
                        colour=0xff0000,
                        description=f"❌ {role.name} not found in config"
                    )
                    embed.set_author(
                        name="Income", icon_url=self.bot.user.avatar_url)
                    await ctx.send(embed=embed)

            income_multiplier = 1
            for item in self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["equiped"]:
                item = self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["equiped"][item]
                income_multiplier = income_multiplier * \
                    (item["income_percent"] / 100)

            income_boost = 0
            for item in self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["equiped"]:
                item = self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["equiped"][item]
                income_boost += item["income"]

            stewardship_bonus = round(
                self.bot.configs[ctx.guild.id]['players'][ctx.author.id]['stats']['stewardship']*income*self.bot.configs[ctx.guild.id]['stewardship_rate'], 5)

            income = (income*income_multiplier)+income_boost+(
                stewardship_bonus)

            embed = discord.Embed(
                colour=0x00ff00,
                description=f"Income: `{income:,}{self.bot.configs[ctx.guild.id]['currency_symbol']}`\nIncome boosted: `{income_boost:,}{self.bot.configs[ctx.guild.id]['currency_symbol']}`\nIncome multiplier `{income_multiplier}`\nStewardship bonus `{self.bot.configs[ctx.guild.id]['players'][ctx.author.id]['stats']['stewardship'] * self.bot.configs[ctx.guild.id]['stewardship_rate'] * 100}%`".replace(
                    ",", " ")
            )
            embed.set_author(name="Income", icon_url=self.bot.user.avatar_url)
            await ctx.send(embed=embed)
        except:
            print(traceback.format_exc())
            await ctx.send(traceback.format_exc())

    @commands.command(name="add-income", pass_context=True, help="Add income: add-income <role: discord.Role> <value: integer>")
    @commands.has_permissions(administrator=True)
    async def add_income(self, ctx: Context, role: discord.Role, value: int):
        logging.debug(f"Adding {value} to income of {role}")
        try:
            if value > 0:
                self.bot.configs[ctx.guild.id]["income"][role.id] += value

                embed = discord.Embed(
                    colour=0x00ff00,
                    description=f"✅ Added: `{value:,}{self.bot.configs[ctx.guild.id]['currency_symbol']}` to income of {role.mention}".replace(
                        ",", " ")
                )
                embed.set_author(name="Add income",
                                 icon_url=self.bot.user.avatar_url)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    colour=0xff0000,
                    description=f"❌ Nothing to add"
                )
                embed.set_author(
                    name="Income", icon_url=self.bot.user.avatar_url)
                await ctx.send(embed=embed)

        except:
            print(traceback.format_exc())
            await ctx.send(traceback.format_exc())

        self.bot.configs[ctx.guild.id].save()

    @commands.command(name="remove-income", pass_context=True, help="Remove income: remove-income <role: discord.Role> <value: integer>")
    @commands.has_permissions(administrator=True)
    async def remove_income(self, ctx: Context, role: discord.Role, value: int):
        logging.debug(f"Removing {value} from income of {role}")
        try:
            if value > 0:
                self.bot.configs[ctx.guild.id]["income"][role.id] -= value

                embed = discord.Embed(
                    colour=0x00ff00,
                    description=f"✅ Removed: `{value:,}{self.bot.configs[ctx.guild.id]['currency_symbol']}` from income of {role.mention}".replace(
                        ",", " ")
                )
                embed.set_author(
                    name="Income", icon_url=self.bot.user.avatar_url)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    colour=0xff0000,
                    description=f"❌ Invalid value"
                )
                embed.set_author(
                    name="Income", icon_url=self.bot.user.avatar_url)
                await ctx.send(embed=embed)
        except:
            print(traceback.format_exc())
            await ctx.send(traceback.format_exc())

        self.bot.configs[ctx.guild.id].save()

    @commands.command(name="income-lb", help="Show da income leaderboard: l, lb, leaderboard")
    async def income_lb(self, ctx: Context):
        logging.debug("Displaying income leaderboard")
        try:
            roles = self.bot.configs[ctx.guild.id]["income"]
            _sorted = {k: v for k, v in sorted(
                roles.items(), key=lambda item: item[1], reverse=True)}

            e_list = []
            msg = ""
            index = 1
            for _id in _sorted:
                try:
                    role = get(self.bot.guilds[0].roles, id=_id).mention
                except:
                    pass
                msg += f"{index}. {role} `{_sorted[_id]:,}{self.bot.configs[ctx.guild.id]['currency_symbol']}`\n".replace(
                    ",", " ")
                if index == 30:
                    embed = discord.Embed(
                        colour=0x00ff00,
                        description=msg
                    )
                    embed.set_author(name="Income Leaderboard",
                                     icon_url=self.bot.user.avatar_url)
                    e_list.append(embed)
                    msg = ""
                    index = 1
                else:
                    index += 1

            embed = discord.Embed(
                colour=0x00ff00,
                description=msg
            )
            embed.set_author(name="Leaderboard",
                             icon_url=self.bot.user.avatar_url)
            e_list.append(embed)

            paginator = DiscordUtils.Pagination.AutoEmbedPaginator(ctx)
            paginator.remove_reactions = True
            await paginator.run(e_list)
        except:
            print(traceback.format_exc())
            await ctx.send(traceback.format_exc())


def setup(bot):
    bot.add_cog(Income(bot))
