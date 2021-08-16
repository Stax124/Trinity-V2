import datetime
import logging
import random
import time
import traceback

import discord
import pytz
from discord.ext import commands
from discord.ext.commands.bot import AutoShardedBot
from discord.ext.commands.context import Context


class Work(commands.Cog):
    def __init__(self, bot: AutoShardedBot):
        self.bot = bot

    @commands.command(name="work", help="What are you doing, make some money!: work")
    async def user_work(self, ctx: Context):
        logging.debug(f"{ctx.author.display_name} executing work")
        try:
            if time.time() >= self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["last-work"] + self.bot.configs[ctx.guild.id]["deltatime"]:
                income = 0
                for role in ctx.author.roles:
                    if self.bot.configs[ctx.guild.id]["income"][role.id] != 0:
                        income += self.bot.configs[ctx.guild.id]["income"][role.id]
                if income <= 0:
                    embed = discord.Embed(
                        colour=0xff0000,
                        description=f"❌ You do not have income set, please ask admin to do so"
                    )
                    embed.set_author(
                        name="Work", icon_url=self.bot.user.avatar_url)
                    await ctx.send(embed=embed)
                else:
                    income_multiplier = 1
                    for item in self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["equiped"]:
                        item = self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["equiped"][item]
                        income_multiplier = income_multiplier * \
                            (item["income_percent"] / 100)

                    income_boost = 0
                    for item in self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["equiped"]:
                        item = self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["equiped"][item]
                        income_boost += item["income"]

                    income = (income*income_multiplier)+income_boost+(
                        round(self.bot.configs[ctx.guild.id]['players'][ctx.author.id]['stats']['stewardship']*income*self.bot.configs[ctx.guild.id]['stewardship_rate'], 5))

                    rate = random.randrange(
                        100-self.bot.configs[ctx.guild.id]["work_range"]*100, 100+self.bot.configs[ctx.guild.id]["work_range"]*100) / 100 if self.bot.configs[ctx.guild.id]["work_range"] != 0 else 1
                    if self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["last-work"] != 0:
                        timedelta = (
                            time.time() - self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["last-work"]) / self.bot.configs[ctx.guild.id]["deltatime"]
                        self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["balance"] += int(
                            income * timedelta * rate)
                        self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["last-work"] = time.time()
                    else:
                        timedelta = 1
                        self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["balance"] += income
                        self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["last-work"] = time.time()

                    logging.debug(
                        f"{ctx.author.display_name} ■ {ctx.author.id} is working [timedelta={timedelta}, rate={rate}]")
                    embed = discord.Embed(
                        colour=0x00ff00,
                        description=f"✅ <@{ctx.author.id}> worked and got `{int(timedelta*income*rate):,} {self.bot.configs[ctx.guild.id]['currency_symbol']}`\nNext available at {datetime.datetime.fromtimestamp(int(self.bot.configs[ctx.guild.id]['players'][ctx.author.id]['last-work'] + self.bot.configs[ctx.guild.id]['deltatime']),tz=pytz.timezone('Europe/Prague')).time()}\nIncome boosted: `{income_boost:,}{self.bot.configs[ctx.guild.id]['currency_symbol']}`\nIncome multiplier `{income_multiplier}`\nStewardship bonus: `{self.bot.configs[ctx.guild.id]['players'][ctx.author.id]['stats']['stewardship']*self.bot.configs[ctx.guild.id]['stewardship_rate'] * 100}%`".replace(",", " ")
                    )
                    embed.set_author(
                        name="Work", icon_url=self.bot.user.avatar_url)
                    await ctx.send(embed=embed)
                    logging.debug(
                        f"{ctx.author.display_name} ■ {ctx.author.id} is working [timedelta={timedelta}, rate={rate}], symbol={self.bot.configs[ctx.guild.id]['currency_symbol']}, next={datetime.datetime.fromtimestamp(int(self.bot.configs[ctx.guild.id]['players'][ctx.author.id]['last-work'] + self.bot.configs[ctx.guild.id]['deltatime']),tz=pytz.timezone('Europe/Prague')).time()}, boost={income_boost}, multiplier={income_multiplier}, stewardship={self.bot.configs[ctx.guild.id]['players'][ctx.author.id]['stats']['stewardship']*self.bot.configs[ctx.guild.id]['stewardship_rate']}%")
            else:
                embed = discord.Embed(
                    colour=0xff0000,
                    description=f"❌ You can work at {datetime.datetime.fromtimestamp(int(self.bot.configs[ctx.guild.id]['players'][ctx.author.id]['last-work']+self.bot.configs[ctx.guild.id]['deltatime']),tz=pytz.timezone('Europe/Prague')).time()}"
                )
                embed.set_author(
                    name="Work", icon_url=self.bot.user.avatar_url)
                await ctx.send(embed=embed)
            self.bot.configs[ctx.guild.id].save()
        except:
            print(traceback.format_exc())
            await ctx.send(traceback.format_exc())


def setup(bot):
    bot.add_cog(Work(bot))
