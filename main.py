from helpers import all_scores, daily_scores, score_message, weekly_scores
from mongo_data.Models.score import Score
from mongo_data.Models.message import Message
import discord
from discord.ext import commands
from config import Config

commant_prefix = "!nice "
word_list = ["nice", "nojs", "noice", "najs"]
description = f'''A Nice bot by Stroid"'''
activity = discord.Game("!nice help")
bot = commands.Bot(command_prefix=commant_prefix, description=description, activity=activity)


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
    scores = all_scores(Score(ctx.guild.id))
    await ctx.send(score_message("NICE LEADERBOARD", scores))


@bot.command(brief="Daily scoreboard")
async def daily(ctx):
    scores = daily_scores(Score(ctx.guild.id))
    await ctx.send(score_message("DAILY LEADERBOARD", scores))


@bot.command(brief="Weekly scoreboard")
async def weekly(ctx):
    scores = weekly_scores(Score(ctx.guild.id))
    await ctx.send(score_message("WEEKLY LEADERBOARD", scores))


@bot.command(brief="The list of words")
async def wordlist(ctx):
    word_list = Config("config_files/config.json").WORD_LIST
    await ctx.send(f"Words im looking for: {' '.join(word_list)}")


@bot.command(brief='Dont use plz, i give cookies', description='This is only a testing function that the one and only master dev stroid that should use :)')
async def test(ctx):
    await ctx.send("Dont, plz. Halp")

if __name__ == "__main__":
    secrets = Config("config_files/secrets.json")
    bot.run(secrets.DISCORD_TOKEN)
