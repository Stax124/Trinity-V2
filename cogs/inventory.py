import argparse
import shlex
import traceback
from typing import Union

import discord
import DiscordUtils
from discord.ext.commands.bot import AutoShardedBot
from core.functions import confirm
from core.static import rarity
from discord.ext import commands
from discord.ext.commands.context import Context


class Inventory(commands.Cog):
    "Owner commands"

    def __init__(self, bot: AutoShardedBot):
        self.bot = bot

    @commands.command(name="inventory", help="Shows your 'realy usefull' items in your inventory: inventory", aliases=["inv", "backpack", "loot"])
    async def inventory(self, ctx: Context):
        try:
            e_list = []
            index = 1
            last = len(self.bot.configs[ctx.guild.id]
                       ["players"][ctx.author.id]["inventory"])
            for name in self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["inventory"]:
                item = self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["inventory"][name]
                embed = discord.Embed(
                    title=name, description=item["description"] if item["description"] != None else "", color=rarity.__dict__[item["rarity"]])
                embed.set_author(
                    name="Inventory" + f" ({index}/{last})", icon_url=self.bot.user.avatar_url)
                embed.add_field(name="Type", value=item["type"], inline=True)
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
                e_list.append(embed)
                index += 1

            if e_list == []:
                embed = discord.Embed(
                    colour=discord.Colour.from_rgb(255, 255, 0),
                    description=f"❌ Nothing in inventory"
                )
                embed.set_author(name="Inventory",
                                 icon_url=self.bot.user.avatar_url)
                await ctx.send(embed=embed)
                return

            paginator = DiscordUtils.Pagination.AutoEmbedPaginator(ctx)
            paginator.remove_reactions = True
            await paginator.run(e_list)
        except:
            print(traceback.format_exc())
            await ctx.send(traceback.format_exc())

    @commands.command(name="equiped", help="Shows your equiped items: equiped")
    async def equiped(self, ctx: Context):
        try:
            e_list = []
            index = 1
            last = len(self.bot.configs[ctx.guild.id]
                       ["players"][ctx.author.id]["equiped"])
            for name in self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["equiped"]:
                item = self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["equiped"][name]
                embed = discord.Embed(
                    title=name, description=item["description"], color=rarity.__dict__[item["rarity"]])
                embed.set_author(
                    name="Inventory" + f" ({index}/{last})", icon_url=self.bot.user.avatar_url)
                embed.add_field(name="Type", value=item["type"], inline=True)
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
                e_list.append(embed)
                index += 1

            if e_list == []:
                embed = discord.Embed(
                    colour=discord.Colour.from_rgb(255, 255, 0),
                    description=f"❌ Nothing in inventory"
                )
                embed.set_author(name="Inventory",
                                 icon_url=self.bot.user.avatar_url)
                await ctx.send(embed=embed)
                return

            paginator = DiscordUtils.Pagination.AutoEmbedPaginator(ctx)
            paginator.remove_reactions = True
            await paginator.run(e_list)
        except:
            print(traceback.format_exc())
            await ctx.send(traceback.format_exc())

    @commands.command(name="equip", help="Equip item: equip <*item: str>")
    async def equip(self, ctx: Context, *, item: str):
        try:
            try:
                types = []
                for equiped in self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["equiped"]:
                    equiped = self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["equiped"][equiped]
                    types.append(equiped["type"])

                if self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["inventory"][item]["type"] in types:
                    embed = discord.Embed(
                        colour=discord.Colour.from_rgb(255, 255, 0),
                        description=f"❌ Slot already occupied"
                    )
                    embed.set_author(
                        name="Equip", icon_url=self.bot.user.avatar_url)
                    await ctx.send(embed=embed)
                    return

                self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["equiped"][
                    item] = self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["inventory"][item]
                del self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["inventory"][item]
                embed = discord.Embed(
                    colour=discord.Colour.from_rgb(255, 255, 0),
                    description=f"✅ {item} equiped"
                )
                embed.set_author(
                    name="Equip", icon_url=self.bot.user.avatar_url)
                await ctx.send(embed=embed)

            except KeyError:
                embed = discord.Embed(
                    colour=discord.Colour.from_rgb(255, 255, 0),
                    description=f"❌ {item} not found in your inventory"
                )
                embed.set_author(
                    name="Equip", icon_url=self.bot.user.avatar_url)
                await ctx.send(embed=embed)
        except:
            print(traceback.format_exc())
            await ctx.send(traceback.format_exc())

        self.bot.configs[ctx.guild.id].save()

    @commands.command(name="unequip", help="Unequip item: unequip <*item: str>")
    async def unequip(self, ctx: Context, *, item: str):
        try:
            try:
                self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["inventory"][
                    item] = self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["equiped"][item]
                del self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["equiped"][item]
                embed = discord.Embed(
                    colour=discord.Colour.from_rgb(255, 255, 0),
                    description=f"✅ {item} unequiped"
                )
                embed.set_author(
                    name="Unequip", icon_url=self.bot.user.avatar_url)
                await ctx.send(embed=embed)

            except KeyError:
                embed = discord.Embed(
                    colour=discord.Colour.from_rgb(255, 255, 0),
                    description=f"❌ {item} not found in your inventory"
                )
                embed.set_author(
                    name="Unequip", icon_url=self.bot.user.avatar_url)
                await ctx.send(embed=embed)
        except:
            print(traceback.format_exc())
            await ctx.send(traceback.format_exc())

        self.bot.configs[ctx.guild.id].save()

    @commands.command(name="recycle", help="Recycle item: recycle <*item: str>")
    async def recycle(self, ctx: Context, *, item: str):
        try:
            if item in self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["inventory"]:
                confirmed = await confirm(self.bot, ctx, f"Item found: Recycle {item} ?")
                if not confirmed:
                    return

                del self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["inventory"][item]

                embed = discord.Embed(
                    colour=discord.Colour.from_rgb(255, 255, 0),
                    description=f"✅ Recycled"
                )
                embed.set_author(
                    name="Recycle", icon_url=self.bot.user.avatar_url)
                await ctx.send(embed=embed)

            else:
                embed = discord.Embed(
                    colour=discord.Colour.from_rgb(255, 255, 0),
                    description=f"❌ {item} not found"
                )
                embed.set_author(
                    name="Recycle", icon_url=self.bot.user.avatar_url)
                await ctx.send(embed=embed)
        except:
            print(traceback.format_exc())
            await ctx.send(traceback.format_exc())

        self.bot.configs[ctx.guild.id].save()

    @commands.command(name="recycle-all", help="Recycle item: recycle-all <rarity: str>")
    async def recycle_all(self, ctx: Context, rarity: str = "common"):
        try:
            items = [item for item in self.bot.configs[ctx.guild.id]["players"]
                     [ctx.author.id]["inventory"] if self.bot.configs[ctx.guild.id]["players"]
                     [ctx.author.id]["inventory"][item]["rarity"] == rarity]

            await ctx.send(items)
        except:
            print(traceback.format_exc())
            await ctx.send(traceback.format_exc())

        self.bot.configs[ctx.guild.id].save()

    @commands.command(name="add-player-item", help="Add new item to players inventory: add-player-item UNION[str, discord.Member] [--income INCOME] [--income_percent INCOME_PERCENT] [--discount DISCOUNT] [--discount_percent DISCOUNT_PERCENT] [--description DESCRIPTION] name {common,uncommon,rare,epic,legendary,event} {helmet,weapon,armor,leggins,boots,artefact}")
    @commands.has_permissions(administrator=True)
    async def add_player_item(self, ctx: Context, user: Union[discord.Member, str], *querry):
        fparser = argparse.ArgumentParser()
        fparser.add_argument("name", type=str)
        fparser.add_argument("rarity", choices=[
                             "common", "uncommon", "rare", "epic", "legendary", "event"], type=str)
        fparser.add_argument(
            "type", choices=["helmet", "weapon", "armor", "leggins", "boots", "artefact"])
        fparser.add_argument("--income", type=int, default=0)
        fparser.add_argument("--income_percent", type=int, default=100)
        fparser.add_argument("--discount", type=str, default=None)
        fparser.add_argument("--discount_percent", type=int, default=0)
        fparser.add_argument("--description", type=str, default=None)

        querry = shlex.split(" ".join(querry))

        try:
            fargs = fparser.parse_args(querry)
        except SystemExit:
            return

        if user == "loot-table":
            self.bot.configs[ctx.guild.id]["loot-table"][fargs.name] = {
                "description": fargs.description,
                "type": fargs.type,
                "rarity": fargs.rarity,
                "income": fargs.income,
                "income_percent": fargs.income_percent,
                "discount": fargs.discount,
                "discount_percent": fargs.discount_percent,
                "equiped": False
            }
        else:
            self.bot.configs[ctx.guild.id]["players"][user.id]["inventory"][fargs.name] = {
                "description": fargs.description,
                "type": fargs.type,
                "rarity": fargs.rarity,
                "income": fargs.income,
                "income_percent": fargs.income_percent,
                "discount": fargs.discount,
                "discount_percent": fargs.discount_percent,
                "equiped": False
            }

        embed = discord.Embed(
            title=fargs.name, description=fargs.description, color=rarity.__dict__[fargs.rarity])
        embed.set_author(name="Succesfully added to inventory",
                         icon_url=self.bot.user.avatar_url)
        embed.add_field(name="Type", value=fargs.type, inline=True)
        embed.add_field(name="Income", value=fargs.income, inline=True)
        embed.add_field(name="Income %",
                        value=fargs.income_percent, inline=True)
        embed.add_field(name="Discount", value=fargs.discount, inline=True)
        embed.add_field(name="Discount %",
                        value=fargs.discount_percent, inline=True)
        embed.add_field(name="Rarity", value=fargs.rarity, inline=True)
        await ctx.send(embed=embed)

        self.bot.configs[ctx.guild.id].save()

    @commands.command(name="remove-player-item", help="Remove item from players inventory: remove-player-item <user: Union[str, discord.Member]> <item: str>")
    @commands.has_permissions(administrator=True)
    async def remove_player_item(self, ctx: Context, user: Union[str, discord.Member], *, item: str):
        if user == "loot-table":
            del self.bot.configs[ctx.guild.id]["loot-table"][item]
            embed = discord.Embed(
                colour=discord.Colour.from_rgb(255, 255, 0),
                description=f"✅ Removed {item} from loot-table"
            )
            embed.set_author(name="Remove player item",
                             icon_url=self.bot.user.avatar_url)
            await ctx.send(embed=embed)
        elif item in self.bot.configs[ctx.guild.id]["players"][user.id]["inventory"]:
            del self.bot.configs[ctx.guild.id]["players"][user.id]["inventory"][item]

            embed = discord.Embed(
                colour=discord.Colour.from_rgb(255, 255, 0),
                description=f"✅ Removed {item} from <@{user.id}>´s inventory"
            )
            embed.set_author(name="Remove player item",
                             icon_url=self.bot.user.avatar_url)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                colour=discord.Colour.from_rgb(255, 255, 0),
                description=f"❌ {item} not found in <@{user.id}>´s inventory"
            )
            embed.set_author(name="Remove player item",
                             icon_url=self.bot.user.avatar_url)
            await ctx.send(embed=embed)

        self.bot.configs[ctx.guild.id].save()


def setup(bot):
    bot.add_cog(Inventory(bot))
