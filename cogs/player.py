import traceback

import discord
from core.functions import levelup_check
from discord.ext import commands
from discord.ext.commands.bot import AutoShardedBot
from discord.ext.commands.context import Context


class Player(commands.Cog):
    "Owner commands"

    def __init__(self, bot: AutoShardedBot):
        self.bot = bot

    @commands.command(name="talents", help="Show list of skills: talents", aliases=["stats"])
    async def stats(self, ctx: Context):
        try:
            player = self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["stats"]

            embed = discord.Embed(
                colour=0x00ff00,
                description=f"""
                    Diplomacy: {player["diplomacy"]}
                    Warlord: {player["warlord"]}
                    Intrique: {player["intrique"]}
                    Stewardship: {player["stewardship"]}
                    Trading: {player["trading"]}
                    Bartering: {player["bartering"]}
                    Learning: {player["learning"]}""")
            embed.set_author(name="Stats", icon_url=self.bot.user.avatar_url)
            await ctx.send(embed=embed)
        except:
            print(traceback.format_exc())
            await ctx.send(traceback.format_exc())

    @commands.command(name="level", help="Show level, Xp and progress to another level")
    async def level(self, ctx: Context):
        try:
            await levelup_check(self.bot, ctx)
            level = self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["level"]

            xp_for_level = self.bot.configs[ctx.guild.id]["xp_for_level"]
            for _ in range(level):
                xp_for_level *= self.bot.configs[ctx.guild.id]["level_multiplier"]

            xp_for_level = int(xp_for_level)
            xp = self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["xp"]

            if xp == 0:
                progress = 0
            else:
                progress = int((xp / xp_for_level) * 100)

            embed = discord.Embed(
                colour=0x00ff00,
                description=f'Level: {level}\nXp: {xp} / {xp_for_level}\n[{"#"*int(progress/2)+"-"*(50-int(progress/2))}] {progress}%'
            )
            embed.set_author(name="Level", icon_url=self.bot.user.avatar_url)
            await ctx.send(embed=embed)
        except:
            print(traceback.format_exc())
            await ctx.send(traceback.format_exc())

        self.bot.configs[ctx.guild.id].save()

    @commands.command(name="levelup", help="Spend skillpoints for talents: levelup <skill> [value=1]")
    async def skill_add(self, ctx: Context, skill: str, value: int = 1):
        try:
            if skill.lower() in self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["stats"]:
                if self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["skillpoints"] >= value:
                    self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["stats"][skill.lower()
                                                                                      ] += value
                    self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["skillpoints"] -= value

                    embed = discord.Embed(
                        colour=0x00ff00,
                        description=f'✅ Skill point used: {skill} = {self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["stats"][skill.lower()]}'
                    )
                    embed.set_author(name="Add skill",
                                     icon_url=self.bot.user.avatar_url)
                    await ctx.send(embed=embed)

                else:
                    embed = discord.Embed(
                        colour=0xff0000,
                        description=f'❌ Not enought skillpoints'
                    )
                    embed.set_author(name="Add skill",
                                     icon_url=self.bot.user.avatar_url)
                    await ctx.send(embed=embed)
            else:
                embed = discord.Embed(
                    colour=0xff0000,
                    description=f'❌ No skill named {skill} found'
                )
                embed.set_author(name="Add skill",
                                 icon_url=self.bot.user.avatar_url)
                await ctx.send(embed=embed)
        except:
            print(traceback.format_exc())
            await ctx.send(traceback.format_exc())

        self.bot.configs[ctx.guild.id].save()

    @commands.command(name="skillpoints", help="Number of your skillpoints: skillpoints")
    async def skillpoints(self, ctx: Context):
        try:
            embed = discord.Embed(
                colour=0x00ff00,
                description=f'Your skillpoints: {self.bot.configs[ctx.guild.id]["players"][ctx.author.id]["skillpoints"]}'
            )
            embed.set_author(name="Skillpoints",
                             icon_url=self.bot.user.avatar_url)
            await ctx.send(embed=embed)
        except:
            print(traceback.format_exc())
            await ctx.send(traceback.format_exc())


def setup(bot):
    bot.add_cog(Player(bot))
