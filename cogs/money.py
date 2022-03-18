import difflib
import logging
import re
import traceback

import discord
import DiscordUtils
from core.functions import confirm
from discord.ext import commands
from discord.ext.commands.bot import AutoShardedBot
from discord.ext.commands.context import Context
from discord.utils import get


class Money(commands.Cog):
    "No need to look here, we both know that you don't have any"

    def __init__(self, bot: AutoShardedBot):
        self.bot = bot

    @commands.command(name="leaderboard", help="Show the leaderboard", aliases=["lb", "l"])
    async def leaderboard(self, ctx: Context):
        try:
            players = {}
            for player in self.bot.configs[ctx.guild.id]["players"]:
                players[player] = self.bot.configs[ctx.guild.id]["players"][player]["balance"]
            _sorted = {k: v for k, v in sorted(
                players.items(), key=lambda item: item[1], reverse=True)}
            e_list = []
            msg = ""
            index = 1
            for _id in _sorted:
                try:
                    username = get(ctx.guild.members, id=_id).mention
                except:
                    continue
                msg += f"{index}. {username} `{_sorted[_id]:,}{self.bot.configs[ctx.guild.id]['currency_symbol']}`\n".replace(
                    ",", " ")
                if index == 30:
                    embed = discord.Embed(
                        colour=0x00ff00,
                        description=msg
                    )
                    embed.set_author(name="Leaderboard",
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

    @commands.command(name="reset-money", help="Reset balance of target", pass_context=True)
    @commands.has_permissions(administrator=True)
    async def reset_money(self, ctx: Context, member: discord.Member):
        logging.debug(f"Resetting balance of {member.display_name}")
        try:
            if member in ctx.guild.members:
                self.bot.configs[ctx.guild.id]["players"][member.id]["balance"] = 0
                logging.debug(f"Resetting {member}'s balance")
                embed = discord.Embed(
                    colour=0x00ff00,
                    description=f"✅ Resetting {member.mention}'s balance"
                )
                embed.set_author(name="Reset money",
                                 icon_url=self.bot.user.avatar_url)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    colour=0xff0000,
                    description="❌ Member not found"
                )
                embed.set_author(name="Reset money",
                                 icon_url=self.bot.user.avatar_url)
                await ctx.send(embed=embed)
                logging.debug("Member not found")
        except:
            print(traceback.format_exc())
            await ctx.send(traceback.format_exc())

        self.bot.configs[member.guild.id].save()

    @commands.command(name="remove-money", help="Remove money from target: remove-money", pass_context=True)
    @commands.has_permissions(administrator=True)
    async def remove_money(self, ctx: Context, member: discord.Member, balance: int):
        logging.debug(f"Removing {balance} from {member.display_name}")
        try:
            if member in ctx.guild.members:
                self.bot.configs[ctx.guild.id]["players"][member.id]["balance"] -= abs(
                    int(balance))
                logging.info(
                    f"Removing {int(balance)} from {member}")
                embed = discord.Embed(
                    colour=0x00ff00,
                    description=f"✅ Removing {balance}{self.bot.configs[ctx.guild.id]['currency_symbol']} from <@{member.id}>"
                )
                embed.set_author(name="Remove money",
                                 icon_url=self.bot.user.avatar_url)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    colour=0xff0000,
                    description="❌ Member not found"
                )
                embed.set_author(name="Remove money",
                                 icon_url=self.bot.user.avatar_url)
                await ctx.send(embed=embed)
                logging.info("Member not found")

        except:
            print(traceback.format_exc())
            await ctx.send(traceback.format_exc())

        self.bot.configs[ctx.guild.id].save()

    @commands.command(name="add-money", help="Add money to target", pass_context=True)
    @commands.has_permissions(administrator=True)
    async def add_money(self, ctx: Context, *message):
        try:
            if message[0] == "everyone":
                money = message[1]
                for _member in self.bot.configs[ctx.guild.id]["players"]:
                    self.bot.configs[ctx.guild.id]["players"][_member]["balance"] += int(
                        money)

                embed = discord.Embed(
                    colour=0x00ff00,
                    description=f"✅ Adding {int(money)}{self.bot.configs[ctx.guild.id]['currency_symbol']} to @everyone"
                )
                embed.set_author(name="Add money",
                                 icon_url=self.bot.user.avatar_url)
                await ctx.send(embed=embed)
                return

            pattern = re.compile(r'[0-9]+')
            _users = self.bot.guilds[0].members
            _id = int(re.findall(pattern, message[0])[0])
            for _user in _users:
                if _user.id == _id:
                    member = get(ctx.guild.members, id=_user.id)
            balance = float(message[1])

            logging.debug(f"Adding {balance} to {member}")

            if member in ctx.guild.members:
                self.bot.configs[ctx.guild.id]["players"][member.id]["balance"] += abs(
                    int(balance))
                embed = discord.Embed(
                    colour=0x00ff00,
                    description=f"✅ Adding {int(balance)}{self.bot.configs[ctx.guild.id]['currency_symbol']} to <@{_id}>"
                )
                embed.set_author(name="Add money",
                                 icon_url=self.bot.user.avatar_url)
                await ctx.send(embed=embed)
                logging.info(f"Adding {balance} to {member}")
            else:
                embed = discord.Embed(
                    colour=0xff0000,
                    description="❌ Member not found"
                )
                embed.set_author(name="Add money",
                                 icon_url=self.bot.user.avatar_url)
                await ctx.send(embed=embed)
                logging.info("Member not found")
        except:
            print(traceback.format_exc())
            await ctx.send(traceback.format_exc())

        self.bot.configs[ctx.guild.id].save()

    @commands.command(name="buy", help="Spend money to make more money")
    async def buy_upgrade(self, ctx: Context, type: str, value: int = 1):
        logging.debug(f"{ctx.author.display_name} is buying {type} * {value}")
        try:
            if type in self.bot.configs[ctx.guild.id]["upgrade"].keys():
                pass
            else:
                _placeholder = difflib.get_close_matches(
                    type, self.bot.configs[ctx.guild.id]["upgrade"].keys())
                if await confirm(self.bot, ctx, f"Not found in shop - closest match: {_placeholder}"):
                    type = _placeholder[0] if _placeholder != [] else type

            if type in self.bot.configs[ctx.guild.id]["upgrade"].keys():
                if self.bot.configs[ctx.guild.id]["upgrade"][type]["require"] != None:
                    required = self.bot.configs[ctx.guild.id]["upgrade"][type]["require"]
                    player_own_required = True if self.bot.configs[ctx.guild.id]["players"][
                        ctx.author.id]["upgrade"][required] > 0 else False
                else:
                    required = None

                if required == None or player_own_required:
                    try:
                        call = self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["upgrade"][type] + \
                            int(
                                value) <= self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["maxupgrade"][type]
                    except:
                        call = True
                    if self.bot.configs[ctx.guild.id]["upgrade"][type] == None or call:
                        discount = 0
                        for item in self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["equiped"]:
                            item = self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["equiped"][item]
                            if item["discount"] != None:
                                if type == item["discount"]:
                                    discount += item["discount_percent"]

                        if discount > 100:
                            discount = 100

                        discount = round(
                            (discount * 0.01) + (self.bot.configs[ctx.guild.id]['players'][ctx.author.id]['stats']['bartering']*self.bot.configs[ctx.guild.id]['bartering_rate']), 5)

                        cost = (self.bot.configs[ctx.guild.id]["upgrade"][type]["cost"] -
                                self.bot.configs[ctx.guild.id]["upgrade"][type]["cost"] * discount) * int(value)
                        if self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["balance"] >= cost:
                            role_list = []
                            for role in ctx.author.roles:
                                if not role.name in self.bot.configs[ctx.guild.id]["disabled_roles"] or not "spokojenost" in role.name.lower():
                                    try:
                                        if self.bot.configs[ctx.guild.id]["income"][role.id] != 0:
                                            role_list.append(role.id)
                                    except:
                                        embed = discord.Embed(
                                            colour=0xff0000,
                                            description=f"❌ {role.name} not found in config"
                                        )
                                        embed.set_author(
                                            name="Buy", icon_url=self.bot.user.avatar_url)
                                        await ctx.send(embed=embed)
                                        return
                            if len(role_list) > 1:
                                embed = discord.Embed(
                                    colour=0xff0000,
                                    description=f"❌ Multiple roles to add income to: `{role_list}`"
                                )
                                embed.set_author(
                                    name="Buy", icon_url=self.bot.user.avatar_url)
                                await ctx.send(embed=embed)
                                return
                            elif len(role_list) == 0 and self.bot.configs[ctx.guild.id]["upgrade"][type]["income"] != 0:
                                embed = discord.Embed(
                                    colour=0xff0000,
                                    description="❌ No role to add income to"
                                )
                                embed.set_author(
                                    name="Buy", icon_url=self.bot.user.avatar_url)
                                await ctx.send(embed=embed)

                            else:
                                if self.bot.configs[ctx.guild.id]["upgrade"][type]["income"] != 0:
                                    self.bot.configs[ctx.guild.id]["income"][role_list[0]
                                                                             ] += self.bot.configs[ctx.guild.id]["upgrade"][type]["income"] * int(value)

                                self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["upgrade"][type] += int(
                                    value)

                                self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["balance"] -= cost
                                self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["manpower"] += int(value) * (
                                    self.bot.configs[ctx.guild.id]["upgrade"][type]["manpower"] if "manpower" in self.bot.configs[ctx.guild.id]["upgrade"][type] else 0)
                                if self.bot.configs[ctx.guild.id]["upgrade"][type]["income"] != 0:
                                    embed = discord.Embed(
                                        colour=0x00ff00,
                                        description=f"✅ Bought {value}x {type} for {cost:,}{self.bot.configs[ctx.guild.id]['currency_symbol']} and your income is now {self.bot.configs[ctx.guild.id]['income'][role_list[0]]:,}{self.bot.configs[ctx.guild.id]['currency_symbol']}\nDiscount: `{discount*100}%`\nBartering discount included in discount: `{self.bot.configs[ctx.guild.id]['players'][ctx.author.id]['stats']['bartering']*self.bot.configs[ctx.guild.id]['bartering_rate']*100}%`".replace(
                                            ",", " ")
                                    )
                                    embed.set_author(
                                        name="Buy", icon_url=self.bot.user.avatar_url)
                                    await ctx.send(embed=embed)
                                else:
                                    embed = discord.Embed(
                                        colour=0x00ff00,
                                        description=f"✅ Bought {value}x {type} for `{cost:,}{self.bot.configs[ctx.guild.id]['currency_symbol']}`\nDiscount: `{discount*100}%`\nBartering discount included in discount: `{self.bot.configs[ctx.guild.id]['players'][ctx.author.id]['stats']['bartering']*self.bot.configs[ctx.guild.id]['bartering_rate']*100}%`".replace(
                                            ",", " ")
                                    )
                                    embed.set_author(
                                        name="Buy", icon_url=self.bot.user.avatar_url)
                                    await ctx.send(embed=embed)

                        else:
                            embed = discord.Embed(
                                colour=0xff0000,
                                description="❌ Not enought money"
                            )
                            embed.set_author(
                                name="Buy", icon_url=self.bot.user.avatar_url)
                            await ctx.send(embed=embed)
                    else:
                        embed = discord.Embed(
                            colour=0xff0000,
                            description="❌ You cannot purchase more items of this type"
                        )
                        embed.set_author(
                            name="Buy", icon_url=self.bot.user.avatar_url)
                        await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(
                        colour=0xff0000,
                        description=f"❌ Required item not bought: {required}"
                    )
                    embed.set_author(
                        name="Buy", icon_url=self.bot.user.avatar_url)
                    await ctx.send(embed=embed)
            else:
                logging.info(f"Invalid type or value")
                embed = discord.Embed(
                    colour=0xff0000,
                    description="❌ Invalid type or value"
                )
                embed.set_author(name="Buy", icon_url=self.bot.user.avatar_url)
                await ctx.send(embed=embed)
        except:
            print(traceback.format_exc())
            await ctx.send(traceback.format_exc())

        self.bot.configs[ctx.guild.id].save()

    @commands.command(name="pay", help="Send money to target")
    async def user_pay(self, ctx: Context, member: discord.Member, balance: int):
        logging.debug(
            f"Transfering {balance} from {ctx.author.display_name} to {member.display_name}")
        try:
            if balance < 1:
                embed = discord.Embed(
                    colour=0xff0000,
                    description=f"❌ Invalid value"
                )
                embed.set_author(name="Pay", icon_url=self.bot.user.avatar_url)
                await ctx.send(embed=embed)
            else:
                if self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["balance"] >= balance:
                    if member in ctx.guild.members:
                        self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["balance"] -= int(
                            balance)
                        self.bot.configs[ctx.guild.id]["players"][member.id]["balance"] += int(
                            balance)
                        logging.info(f"Paid {balance} to {member}")
                        embed = discord.Embed(
                            colour=0x00ff00,
                            description=f"✅ Paid {balance:,}{self.bot.configs[ctx.guild.id]['currency_symbol']} to <@{member.id}>".replace(
                                ",", " ")
                        )
                        embed.set_author(
                            name="Pay", icon_url=self.bot.user.avatar_url)
                        await ctx.send(embed=embed)
                    else:
                        embed = discord.Embed(
                            colour=0xff0000,
                            description="❌ Member not found"
                        )
                        embed.set_author(
                            name="Pay", icon_url=self.bot.user.avatar_url)
                        await ctx.send(embed=embed)
                        logging.info("Member not found")
                else:
                    embed = discord.Embed(
                        colour=0xff0000,
                        description="❌ You don't have enough money"
                    )
                    embed.set_author(
                        name="Pay", icon_url=self.bot.user.avatar_url)
                    await ctx.send(embed=embed)

        except:
            print(traceback.format_exc())
            await ctx.send(traceback.format_exc())

        self.bot.configs[ctx.guild.id].save()

    @commands.command(name="balance", help="Show your balance or more likely, empty pocket", aliases=["bal", "b", "money"])
    async def bal(self, ctx: Context):
        logging.debug(f"Displaying balance of {ctx.author.display_name}")
        try:
            embed = discord.Embed(
                colour=0x00ff00,
                description=f"<@{ctx.author.id}> has {self.bot.configs[ctx.guild.id]['players'][ctx.author.id]['balance']:,}{self.bot.configs[ctx.guild.id]['currency_symbol']}".replace(
                    ",", " ")
            )
            embed.set_author(name="Balance", icon_url=self.bot.user.avatar_url)
            await ctx.send(embed=embed)
        except:
            print(traceback.format_exc())
            await ctx.send(traceback.format_exc())

    @commands.command(name="shop", help="Shows shop")
    async def shop(self, ctx: Context):
        try:
            e_list = []
            index = 1
            msg = ""
            _sorted_keys = list(
                self.bot.configs[ctx.guild.id]["upgrade"].keys())
            _sorted_keys.sort(key=str.lower)

            _sorted = {}

            for item in _sorted_keys:
                _sorted[item] = self.bot.configs[ctx.guild.id]["upgrade"][item]

            for item in _sorted:
                if "manpower" in self.bot.configs[ctx.guild.id]["upgrade"][item]:
                    if self.bot.configs[ctx.guild.id]["upgrade"][item]["manpower"] != 0:
                        manpower = f'`Manpower:` {self.bot.configs[ctx.guild.id]["upgrade"][item]["manpower"]}'
                    else:
                        manpower = ""
                else:
                    manpower = ""
                stock = f'{self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["upgrade"][item]}/{self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["maxupgrade"][item]}' if self.bot.configs[ctx.guild.id][
                    "players"][ctx.author.id]["maxupgrade"][item] != None else f'{self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["upgrade"][item]}/Not limited'
                msg += f'`{item}` {stock} `Cost:` {self.bot.configs[ctx.guild.id]["upgrade"][item]["cost"]:,}{self.bot.configs[ctx.guild.id]["currency_symbol"]} {manpower}\n'.replace(
                    ",", " ")
                if index == 30:
                    embed = discord.Embed(
                        colour=0x00ff00,
                        description=msg
                    )
                    embed.set_author(
                        name="Shop", icon_url=self.bot.user.avatar_url)
                    e_list.append(embed)
                    msg = ""
                    index = 1
                else:
                    index += 1
            embed = discord.Embed(
                colour=0x00ff00,
                description=msg
            )
            embed.set_author(name="Shop", icon_url=self.bot.user.avatar_url)
            e_list.append(embed)

            paginator = DiscordUtils.Pagination.AutoEmbedPaginator(ctx)
            paginator.remove_reactions = True
            await paginator.run(e_list)
        except:
            print(traceback.format_exc())
            await ctx.send(traceback.format_exc())


def setup(bot):
    bot.add_cog(Money(bot))
