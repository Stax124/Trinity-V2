import asyncio
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


class Battle(commands.Cog):
    "Owner commands"

    def __init__(self, bot: AutoShardedBot):
        self.bot = bot

    @commands.command(name="manpower", help="Show manpower of user", aliases=["mp", "power"])
    async def manpower(self, ctx: Context, user: discord.Member = None):
        try:
            if user == None:
                user = ctx.author

            manpower = int(self.bot.configs[ctx.guild.id]['players'][user.id]['manpower'] + (self.bot.configs[ctx.guild.id]['players'][user.id]
                                                                                             ['manpower']*self.bot.configs[ctx.guild.id]['players'][ctx.author.id]['stats']['warlord']*self.bot.configs[ctx.guild.id]['warlord_rate']))

            embed = discord.Embed(
                colour=0x00ff00,
                description=f"Manpower of <@{user.id}> is {manpower:,}\nWarlord boost: `{self.bot.configs[ctx.guild.id]['players'][ctx.author.id]['stats']['warlord']*self.bot.configs[ctx.guild.id]['warlord_rate']*100}%`".replace(
                    ",", " ")
            )
            embed.set_author(
                name="Manpower", icon_url=self.bot.user.avatar_url)
            await ctx.send(embed=embed)
        except:
            print(traceback.format_exc())
            await ctx.send(traceback.format_exc())

    @commands.command(name="attack", help="Automatized battle system: attack <player_manpower: int> ")
    async def attack(self, ctx: Context, player_manpower: int, enemy_manpower: int, hours: float, player_support: int = 0, enemy_support: int = 0, mention: bool = True, skip_colonization: bool = False, income: int = 0, income_role: discord.Role = None):
        global time
        global asyncs_on_hold

        if self.bot.configs[ctx.guild.id]["block_asyncs"]:
            await ctx.send("Function blocked by 'hold-asyncs'")
            return

        random.seed(time.time())

        _time = datetime.datetime.now(tz=pytz.timezone(
            'Europe/Prague')).strftime(r'%H:%M:%S')
        a_time = (datetime.datetime.now(tz=pytz.timezone('Europe/Prague')
                                        ) + datetime.timedelta(hours=hours)).strftime(r'%H:%M:%S')
        self.bot.asyncs_on_hold.append(a_time)
        pstart, estart = player_manpower, enemy_manpower
        seconds = hours * 3600

        if hours > self.bot.configs[ctx.guild.id]["maximum_attack_time"]:
            logging.debug(f"Reached max attack time limit")
            embed = discord.Embed(
                colour=0xff0000,
                description=f"❌ Attack can be postponed for maximum of {self.bot.configs[ctx.guild.id]['maximum_attack_time']}h"
            )
            await ctx.send(embed=embed)
            return

        if self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["manpower"] >= pstart:
            self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["manpower"] -= pstart
        else:
            logging.debug(f"Not enought forces")
            embed = discord.Embed(
                colour=0xff0000,
                description=f"❌ Not enought manpower"
            )
            await ctx.send(embed=embed)
            return

        if skip_colonization == False:
            if self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["balance"] < estart:
                logging.debug(f"Not enought money for colonization")
                embed = discord.Embed(
                    colour=0xff0000,
                    description=f"❌ Not enought money for colonization"
                )
                await ctx.send(embed=embed)
                self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["manpower"] += pstart
                return
            else:
                self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["balance"] -= estart

        self.bot.configs[ctx.guild.id].save()

        embed = discord.Embed(
            title="Attack",
            description=f"<@{ctx.author.id}>",
            color=0x00ff00
        )
        embed.set_author(name="Succesfully added to queue",
                         icon_url=self.bot.user.avatar_url)
        embed.add_field(name="Time", value=(datetime.datetime.now(tz=pytz.timezone(
            'Europe/Prague')) + datetime.timedelta(hours=hours)).strftime(r'%H:%M:%S'), inline=False)
        embed.add_field(name="Your manpower",
                        value=player_manpower, inline=False)
        embed.add_field(name="Enemy manpower",
                        value=enemy_manpower, inline=False)
        embed.add_field(name="Your support",
                        value=player_support, inline=False)
        embed.add_field(name="Enemy support",
                        value=enemy_support, inline=False)
        embed.add_field(name="Role getting income",
                        value=f"@{income_role}" if income_role != None else "None", inline=False)
        embed.add_field(name="Income", value=income, inline=False)
        await ctx.send(embed=embed)

        await asyncio.sleep(delay=seconds)
        await ctx.send("Battle started")

        if player_support > 0:
            player_support_roll = random.randint(0, player_support)
            enemy_manpower -= player_support_roll

        enemy_manpower = max(enemy_manpower, 0)

        if enemy_support > 0:
            enemy_support_roll = random.randint(0, enemy_support)
            player_manpower -= enemy_support_roll

        player_manpower = max(player_manpower, 0)

        iteration = 1

        while iteration <= 3:
            if enemy_manpower > 0 and player_manpower > 0:
                print(
                    f"Rolling: {player_manpower} | {enemy_manpower}: roll - {iteration}")
                e_before_roll = enemy_manpower
                player_roll = random.randint(0, player_manpower)
                enemy_manpower -= player_roll
                enemy_manpower = max(enemy_manpower, 0)

                if enemy_manpower > 0:
                    enemy_roll = random.randint(0, enemy_manpower)
                    player_manpower -= enemy_roll
                if enemy_manpower == 0:
                    enemy_roll = random.randint(0, e_before_roll)
                    player_manpower -= enemy_roll

                player_manpower = max(player_manpower, 0)

            iteration += 1

        if iteration == 4 and player_manpower > 0 and enemy_manpower > 0:
            msg = "❌ Out of rolls"
            colour = 0xff0000
            
            if skip_colonization == False:
                self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["balance"] += estart
        elif player_manpower > 0 and enemy_manpower == 0:
            msg = "✅ You won"
            colour = 0x00ff00

            if self.bot.configs[ctx.guild.id]["allow_attack_income"]:
                if income_role != None:
                    if income >= 200000:
                        ctx.send("Income too high, ask admin to add it")
                    else:
                        self.bot.configs[ctx.guild.id]["income"][income_role.id] += income
        elif player_manpower == 0 and enemy_manpower > 0:
            msg = "❌ You lost"
            colour = 0xff0000
            
            if skip_colonization == False:
                self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["balance"] += estart
        else:
            msg = "❓ Tie ❓"
            colour = 0xffff00
            
            if skip_colonization == False:
                self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["balance"] += estart

        self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["manpower"] += player_manpower

        embed = discord.Embed(
            colour=colour,
            description=f"<@{ctx.author.id}>´s attack from {_time}\n\n{msg}\n\n`Before battle:`\n    Your army: {pstart:,}\n    Enemy army: {estart:,}\n\n`After battle:`\n    Your army: {player_manpower:,}\n    Enemy army: {enemy_manpower:,}\n\n`Casualties:`\n    Your army: {pstart-player_manpower:,}\n    Enemy army: {estart-enemy_manpower}".replace(
                ",", " ")
        )
        embed.set_author(name="Attack", icon_url=self.bot.user.avatar_url)
        await ctx.send(embed=embed)

        if mention:
            await ctx.send(ctx.author.mention)

        self.bot.asyncs_on_hold.remove(a_time)
        self.bot.configs[ctx.guild.id].save()


def setup(bot):
    bot.add_cog(Battle(bot))
