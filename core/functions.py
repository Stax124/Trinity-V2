from discord.ext.commands import Bot
from discord.ext.commands.bot import AutoShardedBot
from discord.ext.commands.context import Context
import discord
import asyncio
import logging


async def confirm(bot: Bot, ctx: Context, message: str, timeout: int = 20, author: str = "Confirm"):
    try:
        embed = discord.Embed(
            colour=discord.Colour.from_rgb(255, 255, 0),
            description=message
        )
        embed.set_author(name=author, icon_url=bot.user.avatar_url)

        msg = await ctx.send(embed=embed)
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")

        def check(reaction, user):
            return user == ctx.message.author and str(reaction.emoji) in ['✅', '❌']

        reaction, _ = await bot.wait_for('reaction_add', timeout=timeout, check=check)
        if reaction.emoji == '❌':
            await msg.delete()
            return False
        elif reaction.emoji == '✅':
            await msg.delete()
            return True
    except asyncio.TimeoutError:
        await msg.delete()
        return False


def jsonKeys2int(x):
    if isinstance(x, dict):
        try:
            return {int(k): v for k, v in x.items()}
        except:
            pass
    return x

async def levelup_check(bot: AutoShardedBot,ctx: Context):
    logging.debug(f"Triggering levelup_check for {ctx.author.display_name}")
    player = ctx.author
    xp = bot.configs[ctx.guild.id]["players"][player.id]["xp"]
    level = bot.configs[ctx.guild.id]["players"][player.id]["level"]

    xp_for_level = bot.configs[ctx.guild.id]["xp_for_level"]
    for _ in range(level):
        xp_for_level *= bot.configs[ctx.guild.id]["level_multiplier"]

    xp_for_level = int(xp_for_level)

    if xp >= xp_for_level:
        bot.configs[ctx.guild.id]["players"][player.id]["xp"] -= xp_for_level
        bot.configs[ctx.guild.id]["players"][player.id]["level"] += 1
        bot.configs[ctx.guild.id]["players"][player.id]["skillpoints"] += 1
        embed = discord.Embed(
            colour=discord.Colour.from_rgb(255, 255, 0),
            description=f'You are now level `{bot.configs[ctx.guild.id]["players"][player.id]["level"]}`'
        )
        embed.set_author(name="Level up", icon_url=bot.user.avatar_url)
        await ctx.send(embed=embed)
        logging.debug(
            f"{ctx.author.display_name} is now level {bot.configs[ctx.guild.id]['players'][player.id]['level']}")
        await levelup_check(ctx)
