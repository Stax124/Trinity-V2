import difflib
import shlex
import traceback

import discord
import DiscordUtils
from core.functions import confirm
from core.static import rarity
from discord.ext import commands
from discord.ext.commands.bot import AutoShardedBot
from discord.ext.commands.context import Context


class PlayerShop(commands.Cog):
    "Sell stuff, so you can pay your rent"

    def __init__(self, bot: AutoShardedBot):
        self.bot = bot

    @commands.command(name="player-shop", help="Show player shop")
    async def player_shop(self, ctx: Context, _user: discord.Member = None):
        try:
            user = ctx.author if _user == None else _user

            e_list = []
            index = 1
            last = len(self.bot.configs[ctx.guild.id]
                       ["players"][user.id]["player_shop"])
            for name in self.bot.configs[ctx.guild.id]["players"][user.id]["player_shop"]:
                item = self.bot.configs[ctx.guild.id]["players"][user.id]["inventory"][name]
                embed = discord.Embed(
                    title=name, description=item["description"], color=rarity.__dict__[item["rarity"]])
                embed.set_author(
                    name="Player shop" + f" ({index}/{last})", icon_url=self.bot.user.avatar_url)
                embed.add_field(
                    name="Price", value=self.bot.configs[ctx.guild.id]["players"][user.id]["player_shop"][name], inline=False)
                embed.add_field(
                    name="Rarity", value=item["rarity"], inline=True)
                embed.add_field(
                    name="Income", value=item["income"], inline=True) if item["income"] != 0 else None
                embed.add_field(
                    name="Income %", value=item["income_percent"], inline=True) if item["income_percent"] != 0 else None
                embed.add_field(
                    name="Discount", value=item["discount"], inline=True) if item["discount"] != 0 else None
                embed.add_field(
                    name="Discount %", value=item["discount_percent"], inline=True) if item["discount_percent"] != 0 else None
                e_list.append(embed)
                index += 1

            if e_list == []:
                embed = discord.Embed(title="Empty")
                embed.set_author(
                    name="Player shop" + f" ({index}/{last})", icon_url=self.bot.user.avatar_url)
                e_list.append(embed)
            paginator = DiscordUtils.Pagination.AutoEmbedPaginator(ctx)
            paginator.remove_reactions = True
            await paginator.run(e_list)
        except:
            print(traceback.format_exc())
            await ctx.send(traceback.format_exc())

    @commands.command(name="player-sell", help="Sell items")
    async def player_sell(self, ctx: Context, *, message):
        try:
            querry = shlex.split(message)

            try:
                price = int(querry[0])
                item = " ".join(querry[1:])

            except IndexError:
                embed = discord.Embed(
                    colour=0xff0000,
                    description=f"❌ Bad arguments"
                )
                embed.set_author(
                    name="Sell", icon_url=self.bot.user.avatar_url)
                await ctx.send(embed=embed)

            if not item in self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["inventory"]:
                _placeholder = difflib.get_close_matches(
                    item, self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["inventory"].keys())
                if await confirm(self.bot, ctx, f"Not found in shop - closest match: {_placeholder}"):
                    item = _placeholder[0] if _placeholder != [] else item

            if not item in self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["inventory"]:
                embed = discord.Embed(
                    colour=0xff0000,
                    description=f"❌ {item} not found in your inventory"
                )
                embed.set_author(
                    name="Sell", icon_url=self.bot.user.avatar_url)
                await ctx.send(embed=embed)
                return

            self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["player_shop"] = {
                **self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["player_shop"], **{item: price}}

            embed = discord.Embed(
                colour=0x00ff00,
                description=f"✅ Name: `{item}`\nPrice: {price}"
            )
            embed.set_author(name="Sell", icon_url=self.bot.user.avatar_url)
            await ctx.send(embed=embed)
        except:
            print(traceback.format_exc())
            await ctx.send(traceback.format_exc())

        self.bot.configs[ctx.guild.id].save()

    @commands.command(name="player-buy", help="Sell items")
    async def player_buy(self, ctx: Context, user: discord.Member, *, item: str):
        try:
            if ctx.author == user:
                embed = discord.Embed(
                    colour=0xff0000,
                    description="❌ Can't buy item from yourself"
                )
                embed.set_author(name="Player buy",
                                 icon_url=self.bot.user.avatar_url)
                await ctx.send(embed=embed)
                return

            if not item in self.bot.configs[ctx.guild.id]["players"][user.id]["player_shop"]:
                _placeholder = difflib.get_close_matches(
                    item, self.bot.configs[ctx.guild.id]["players"][user.id]["player_shop"].keys())
                if await confirm(self.bot, ctx, f"Not found in shop - closest match: {_placeholder}"):
                    item = _placeholder[0] if _placeholder != [] else item

            try:
                cost = self.bot.configs[ctx.guild.id]["players"][user.id]["player_shop"][item]
            except KeyError:
                embed = discord.Embed(
                    colour=0xff0000,
                    description="❌ Item not found"
                )
                embed.set_author(name="Player buy",
                                 icon_url=self.bot.user.avatar_url)
                await ctx.send(embed=embed)
                return

            if self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["balance"] >= cost - (cost * self.bot.configs[ctx.guild.id]['players'][ctx.author.id]['stats']['trading']*self.bot.configs[ctx.guild.id]['trading_rate']):
                self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["inventory"][
                    item] = self.bot.configs[ctx.guild.id]["players"][user.id]["inventory"][item]
                self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["balance"] -= cost - \
                    (cost * self.bot.configs[ctx.guild.id]['players'][ctx.author.id]
                     ['stats']['trading']*self.bot.configs[ctx.guild.id]['trading_rate'])
                self.bot.configs[ctx.guild.id]["players"][user.id]["balance"] += cost
                del self.bot.configs[ctx.guild.id]["players"][user.id]["player_shop"][item]
                del self.bot.configs[ctx.guild.id]["players"][user.id]["inventory"][item]

                embed = discord.Embed(
                    colour=0x00ff00,
                    description=f"✅ Bought {item} for {cost:,}{self.bot.configs[ctx.guild.id]['currency_symbol']} and item was added to your inventory\nTrading discount: `{self.bot.configs[ctx.guild.id]['players'][ctx.author.id]['stats']['trading']*self.bot.configs[ctx.guild.id]['trading_rate']*100}%`".replace(
                        ",", " ")
                )
                embed.set_author(name="Buy", icon_url=self.bot.user.avatar_url)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    colour=0xff0000,
                    description="❌ Not enought money"
                )
                embed.set_author(name="Player buy",
                                 icon_url=self.bot.user.avatar_url)
                await ctx.send(embed=embed)
        except:
            print(traceback.format_exc())
            await ctx.send(traceback.format_exc())

        self.bot.configs[ctx.guild.id].save()

    @commands.command(name="player-retrieve", help="Cancel shop listing of item")
    async def player_retrieve(self, ctx: Context, *, item: str):
        try:
            if not item in self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["player_shop"]:
                _placeholder = difflib.get_close_matches(
                    item, self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["player_shop"].keys())
                if await confirm(self.bot, ctx, f"Not found in shop - closest match: {_placeholder}"):
                    item = _placeholder[0] if _placeholder != [] else item

            try:
                self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["player_shop"][item]
            except KeyError:
                embed = discord.Embed(
                    colour=0xff0000,
                    description="❌ Item not found"
                )
                embed.set_author(name="Player retrieve",
                                 icon_url=self.bot.user.avatar_url)
                await ctx.send(embed=embed)
                return

            del self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["player_shop"][item]
            embed = discord.Embed(
                colour=0x00ff00,
                description="✅ Item retrieved from shop"
            )
            embed.set_author(name="Player retrieve",
                             icon_url=self.bot.user.avatar_url)
            await ctx.send(embed=embed)

        except:
            print(traceback.format_exc())
            await ctx.send(traceback.format_exc())

        self.bot.configs[ctx.guild.id].save()


def setup(bot):
    bot.add_cog(PlayerShop(bot))
