import argparse
import asyncio
import datetime
import logging
import random
import shlex
import time
import traceback

import discord
import DiscordUtils
import pytz
from core.static import rarity
from discord.ext import commands
from discord.ext.commands.bot import AutoShardedBot
from discord.ext.commands.context import Context


class Expeditions(commands.Cog):
    "Quests, rewards and more rewards"

    def __init__(self, bot: AutoShardedBot):
        self.bot = bot

    @commands.command(name="add-expedition", help="Add new expedition: add-expedition [-h] [--manpower MANPOWER] [--level LEVEL] [--chance CHANCE] [--common COMMON] [--uncommon UNCOMMON] [--rare RARE] [--epic EPIC] [--legendary LEGENDARY] [--xp XP] [--description DESCRIPTION] name cost hours")
    @commands.has_permissions(administrator=True)
    async def add_mission(self, ctx: Context, *_querry):
        fparser = argparse.ArgumentParser()
        fparser.add_argument("name", type=str)
        fparser.add_argument("cost", type=int)
        fparser.add_argument("hours", type=int)
        fparser.add_argument("--manpower", type=int, default=0)
        fparser.add_argument("--level", type=int, default=0)
        fparser.add_argument("--chance", type=int, default=100)
        fparser.add_argument("--common", type=float, default=1)
        fparser.add_argument("--uncommon", type=float, default=0)
        fparser.add_argument("--rare", type=float, default=0)
        fparser.add_argument("--epic", type=float, default=0)
        fparser.add_argument("--legendary", type=float, default=0)
        fparser.add_argument("--xp", type=int, default=0)
        fparser.add_argument("--description", default=None)

        querry = shlex.split(" ".join(_querry))

        try:
            fargs = fparser.parse_args(querry)
        except SystemExit:
            return

        try:
            self.bot.configs[ctx.guild.id]["missions"][fargs.name] = {
                "cost": fargs.cost,
                "hours": fargs.hours,
                "manpower": fargs.manpower,
                "level": fargs.level,
                "chance": fargs.chance,
                "xp": fargs.xp,
                "description": fargs.description,
                "loot-table": {
                    "common": fargs.common,
                    "uncommon": fargs.uncommon,
                    "rare": fargs.rare,
                    "epic": fargs.epic,
                    "legendary": fargs.legendary,
                }
            }

            embed = discord.Embed(title=fargs.name, description=fargs.description,
                                  colour=0x00ff00)
            embed.set_author(name="Succesfully added to missions",
                             icon_url=self.bot.user.avatar_url)
            embed.add_field(name="Cost", value=f"{fargs.cost:,}".replace(
                ",", " "), inline=True)
            embed.add_field(name="Hours", value=f"{fargs.hours:,}".replace(
                ",", " "), inline=True)
            embed.add_field(name="Required manpower", value=f"{fargs.manpower:,}".replace(
                ",", " "), inline=True)
            embed.add_field(name="Required Level",
                            value=fargs.level, inline=True)
            embed.add_field(name="Chance", value=str(
                fargs.chance) + "%", inline=True)
            embed.add_field(name="Xp", value=f"{fargs.xp:,}".replace(
                ",", " "), inline=True)
            embed.add_field(name="Common", value=str(
                fargs.common*100) + "%", inline=False)
            embed.add_field(name="Uncommon", value=str(
                fargs.uncommon*100) + "%", inline=False)
            embed.add_field(name="Rare", value=str(
                fargs.rare*100) + "%", inline=False)
            embed.add_field(name="Epic", value=str(
                fargs.epic*100) + "%", inline=False)
            embed.add_field(name="Legendary", value=str(
                fargs.legendary*100) + "%", inline=False)
            await ctx.send(embed=embed)

        except:
            print(traceback.format_exc())
            await ctx.send(traceback.format_exc())

        self.bot.configs[ctx.guild.id].save()

    @commands.command(name="remove-expedition", help="Remove expedition: remove-missiom")
    @commands.has_permissions(administrator=True)
    async def remove_mission(self, ctx: Context, mission: str):
        try:
            try:
                del self.bot.configs[ctx.guild.id]["missions"][mission]
                embed = discord.Embed(
                    colour=0x00ff00,
                    description=f"✅ Expedition removed"
                )
                embed.set_author(name="Remove expedition",
                                 icon_url=self.bot.user.avatar_url)
                await ctx.send(embed=embed)
            except KeyError:
                embed = discord.Embed(
                    colour=0xff0000,
                    description=f"❌ Expedition not found"
                )
                embed.set_author(name="Remove expedition",
                                 icon_url=self.bot.user.avatar_url)
                await ctx.send(embed=embed)
                return
        except:
            print(traceback.format_exc())
            ctx.send(traceback.format_exc())

        self.bot.configs[ctx.guild.id].save()

    @commands.command(name="expeditions", help="List of expeditions")
    async def missions(self, ctx: Context):
        try:
            e_list = []
            index = 1
            for _mission in self.bot.configs[ctx.guild.id]["missions"]:
                mission = self.bot.configs[ctx.guild.id]["missions"][_mission]
                embed = discord.Embed(
                    title=_mission, description=mission["description"], color=0x00ff00)
                embed.set_author(
                    name="Missions", icon_url=self.bot.user.avatar_url)
                embed.add_field(
                    name="Cost", value=mission["cost"], inline=True)
                embed.add_field(name="Manpower",
                                value=mission["manpower"], inline=True)
                embed.add_field(
                    name="Level", value=mission["level"], inline=True)
                embed.add_field(name="Chance", value=str(
                    mission["chance"]) + "%", inline=True)
                embed.add_field(name="Time to complete", value=str(
                    mission["hours"]) + "h", inline=True)
                embed.add_field(name="Xp", value=mission["xp"], inline=True)
                embed.add_field(name="Common", value=str(
                    mission["loot-table"]["common"]*100) + "%", inline=False)
                embed.add_field(name="Uncommon", value=str(
                    mission["loot-table"]["uncommon"]*100) + "%", inline=False)
                embed.add_field(name="Rare", value=str(
                    mission["loot-table"]["rare"]*100) + "%", inline=False)
                embed.add_field(name="Epic", value=str(
                    mission["loot-table"]["epic"]*100) + "%", inline=False)
                embed.add_field(name="Legendary", value=str(
                    mission["loot-table"]["legendary"]*100) + "%", inline=False)
                e_list.append(embed)
                index += 1

            if e_list == []:
                embed = discord.Embed(
                    colour=0xff0000,
                    description=f"❌ No expeditions yet"
                )
                embed.set_author(name="Expeditions",
                                 icon_url=self.bot.user.avatar_url)
                await ctx.send(embed=embed)
                return

            paginator = DiscordUtils.Pagination.AutoEmbedPaginator(ctx)
            paginator.remove_reactions = True
            await paginator.run(e_list)
        except:
            print(traceback.format_exc())
            await ctx.send(traceback.format_exc())

    @commands.command(name="expedition", help="Start an expedition", aliases=["expedition-start"])
    async def mission_start(self, ctx: Context, expedition_name: str, mention: bool = True):
        global time
        global asyncs_on_hold

        if self.bot.configs[ctx.guild.id]["block_asyncs"]:
            await ctx.send("❌ Function blocked by 'block-asyncs'")
            return

        user = ctx.author
        expedition = self.bot.configs[ctx.guild.id]["missions"][expedition_name]

        if not self.bot.configs[ctx.guild.id]["players"][user.id]["level"] >= expedition["level"]:
            embed = discord.Embed(
                colour=0xff0000,
                description=f"❌ Your level is too low"
            )
            embed.set_author(name="Expedition",
                             icon_url=self.bot.user.avatar_url)
            await ctx.send(embed=embed)
            return

        if not self.bot.configs[ctx.guild.id]["players"][user.id]["balance"] >= expedition["cost"]:
            embed = discord.Embed(
                colour=0xff0000,
                description=f"❌ Not enought money"
            )
            embed.set_author(name="Expedition",
                             icon_url=self.bot.user.avatar_url)
            await ctx.send(embed=embed)
            return

        if not self.bot.configs[ctx.guild.id]["players"][user.id]["manpower"] >= expedition["manpower"]:
            embed = discord.Embed(
                colour=0xff0000,
                description=f"❌ Not enought manpower"
            )
            embed.set_author(name="Expedition",
                             icon_url=self.bot.user.avatar_url)
            await ctx.send(embed=embed)
            return

        self.bot.configs[ctx.guild.id]["players"][user.id]["balance"] -= expedition["cost"]
        self.bot.configs[ctx.guild.id]["players"][user.id]["manpower"] -= expedition["manpower"]

        random.seed(time.time())

        _time = datetime.datetime.now(tz=pytz.timezone(
            'Europe/Prague')).strftime(r'%H:%M:%S')
        a_time = (datetime.datetime.now(tz=pytz.timezone('Europe/Prague')) +
                  datetime.timedelta(hours=expedition["hours"])).strftime(r'%H:%M:%S')
        self.bot.asyncs_on_hold.append(a_time)
        seconds = expedition["hours"] * 3600

        embed = discord.Embed(title=expedition_name, description=expedition["description"]
                              if expedition["description"] != None else "", color=0x00ff00)
        embed.set_author(name="✅ Succesfully added to queue",
                         icon_url=self.bot.user.avatar_url)
        embed.add_field(name="Time", value=(datetime.datetime.now(tz=pytz.timezone(
            'Europe/Prague')) + datetime.timedelta(hours=expedition["hours"])).strftime(r'%H:%M:%S'), inline=False)
        embed.add_field(name="Manpower on hold",
                        value=expedition["manpower"], inline=False)
        embed.add_field(name="Required level",
                        value=expedition["level"], inline=False)
        embed.add_field(
            name="Chance", value=expedition["chance"], inline=False)
        embed.add_field(name="XP", value=expedition["xp"], inline=False)
        await ctx.send(embed=embed)

        await asyncio.sleep(delay=seconds)
        await ctx.send("Mission started")

        if random.randint(0, 100) < expedition["chance"]:
            msg = "✅ Successs"
            self.bot.configs[ctx.guild.id]["players"][user.id]["xp"] += expedition["xp"] + expedition["xp"] * \
                self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["stats"]["learning"] * \
                self.bot.configs[ctx.guild.id]["learning_rate"]

            if len(self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["inventory"]) < self.bot.configs[ctx.guild.id]["max_player_items"]:

                rarities = expedition["loot-table"]
                items = self.bot.configs[ctx.guild.id]["loot-table"]

                weighted_list = ['common'] * int(rarities["common"]*100) + ['uncommon'] * int(rarities["uncommon"]*100) + \
                    ['rare'] * int(rarities["rare"]*100) + ['epic'] * \
                    int(rarities["epic"]*100) + \
                    ['legendary'] * int(rarities["legendary"]*100)

                logging.debug(weighted_list)

                selected_rarity = random.choice(weighted_list)

                item_list = []

                for item in items:
                    if items[item]["rarity"] == selected_rarity:
                        item_list.append(item)

                if item_list != []:
                    chosen_item = random.choice(item_list)
                else:
                    chosen_item = None

                if chosen_item == None:
                    embed = discord.Embed(
                        colour=0xff0000,
                        description=f"❌ No item found"
                    )
                    embed.set_author(name="Expedition",
                                     icon_url=self.bot.user.avatar_url)
                    await ctx.send(embed=embed)
                else:
                    name = chosen_item
                    item = self.bot.configs[ctx.guild.id]["loot-table"][chosen_item]
                    embed = discord.Embed(
                        title=name, description=item["description"] if item["description"] != None else "", color=rarity.__dict__[item["rarity"]])
                    embed.set_author(
                        name="Item found", icon_url=self.bot.user.avatar_url)
                    embed.add_field(
                        name="Type", value=item["type"], inline=True)
                    embed.add_field(
                        name="Income", value=item["income"], inline=True) if item["income"] != 0 else None
                    embed.add_field(
                        name="Income %", value=item["income_percent"], inline=True) if item["income_percent"] != 0 else None
                    embed.add_field(
                        name="Discount", value=item["discount"], inline=True) if item["discount"] != 0 else None
                    embed.add_field(
                        name="Discount %", value=item["discount_percent"], inline=True) if item["discount_percent"] != 0 else None
                    embed.add_field(
                        name="Rarity", value=item["rarity"], inline=True)
                    await ctx.send(embed=embed)

                    index = 1
                    extname = name
                    while name in self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["inventory"]:
                        name = extname + f" ({index})"
                        index += 1
                        logging.debug(
                            f"Item found in inventory! Trying suffix ({index})")
                    self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["inventory"][name] = item
            else:
                embed = discord.Embed(
                    colour=0xff0000,
                    description=f"❌ Maximum item limit reached"
                )
                embed.set_author(name="Expedition",
                                 icon_url=self.bot.user.avatar_url)
                await ctx.send(embed=embed)

        else:
            msg = "❌ Failed"

        embed = discord.Embed(
            colour=0x0000ff,
            description=f"<@{user.id}>´s mission from {_time}\n\n{msg}".replace(
                ",", " ")
        )
        embed.set_author(name="Expedition", icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)

        if mention:
            await ctx.send(ctx.author.mention)

        self.bot.configs[ctx.guild.id]["players"][user.id]["manpower"] += expedition["manpower"]

        self.bot.asyncs_on_hold.remove(a_time)

        self.bot.configs[ctx.guild.id].save()


def setup(bot):
    bot.add_cog(Expeditions(bot))
