from helpers import all_scores, daily_scores, score_message, weekly_scores
from mongo_data.Models.score import Score
from mongo_data.Models.message import Message
import discord
from discord.ext import commands
from config import Config
from random import random

commant_prefix = "!nice "
word_list = ["nice", "nojs", "noice", "najs"]
description = f'''A Nice bot by Stroid"'''
activity = discord.Game("!nice help")
bot = commands.Bot(command_prefix=commant_prefix, description=description, activity=activity)

@bot.event
async def on_message(message):
    if message.author.id != bot.user.id and not message.content.startswith("!nice"):
        msg = Message(message)
        msg.post()
        if msg.matches > 0 and random() < Config("config_files/config.json").LEADERBOARD_ANOUNCMENT_PROB:
            title = Config("config_files/config.json").LEADERBOARD_ANOUNCMENT_TITLE
            scores = all_scores(Score(message.guild.id))
            await message.channel.send(embed = score_message(title, scores))
        return
    await bot.process_commands(message)


@bot.event
async def on_message_delete(message):
    Message(message).delete()


@bot.event
async def on_message_edit(before, after):
    Message(after).update()


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command(brief="Daz, Leaderboard")
async def score(ctx):
    title = Config("config_files/config.json").LEADERBOARD_ANOUNCMENT_TITLE
    scores = all_scores(Score(ctx.guild.id))
    footer = 'You can also do "!nice daily" and "!nice weekly"'
    await ctx.send(embed = score_message(title, scores, footer=footer))


@bot.command(brief="Daily scoreboard")
async def daily(ctx):
    scores = daily_scores(Score(ctx.guild.id))
    footer = 'You can also do "!nice score" and "!nice weekly"'
    await ctx.send(embed = score_message("DAILY LEADERBOARD", scores, footer=footer))


@bot.command(brief="Weekly scoreboard")
async def weekly(ctx):
    scores = weekly_scores(Score(ctx.guild.id))
    footer = 'You can also do "!nice score" and "!nice daily"'
    await ctx.send(embed = score_message("WEEKLY LEADERBOARD", scores, footer=footer))


@bot.command(brief="The list of words")
async def wordlist(ctx):
    word_list = ' '.join(Config("config_files/config.json").WORD_LIST)
    embed = discord.Embed(title="Word list", description=word_list, color=discord.Color.blue())
    await ctx.send(embed=embed)


@bot.command(brief='Dont use plz, i give cookies', description='This is only a testing function that the one and only master dev stroid that should use :)')
async def test(ctx):
    scores = all_scores(Score(ctx.guild.id))
    await ctx.send(embed=score_message("LEADERBOARD", scores))

if __name__ == "__main__":
    secrets = Config("config_files/secrets.json")
    bot.run(secrets.DISCORD_TOKEN)
