from datetime import datetime, timedelta
from mongo_data.Models.score import Score
from mongo_data.Models.message import Message
from secrets.secrets import TOKEN
import discord
from discord.ext import commands
import time


word_list = ["nice", "nojs", "noice", "najs"]
description = f'''A Nice bot by Stroid
you get score by writing one of the following words:"{" ".join(word_list)}"'''


leaderboard_anouncement_cooldown_seconds = 3600

nice_count = dict()
last_score_anouncment = time.time()-leaderboard_anouncement_cooldown_seconds

bot = commands.Bot(command_prefix='!nice ',
                   description=description, activity=discord.Game("!nice help"))


def daily_scores(score):
    date = datetime.now()
    start = date.replace(hour=0, minute=0)
    end = date.replace(hour=23, minute=59)
    return score.get_by_date(start, end)


def weekly_scores(score):
    date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    start = date - timedelta(days=date.weekday())
    end = start + timedelta(days=6)
    return score.get_by_date(start, end)


def all_scores(score):
    return score.get()


def score_message(msg, scores):
    for i, count in enumerate(scores):
        v, k = count
        msg += f'\n\t{1 + i}. {k}: {v}'
    return msg


@bot.event
async def on_message(message):
    if message.author.id != bot.user.id and not message.content.startswith("!nice"):
        Message(message).post()
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
    await ctx.send(f"Words im looking for: {' '.join(word_list)}")


@bot.command(brief='Dont use plz, i give cookies', description='This is only a testing function that the one and only master dev stroid that should use :)')
async def test(ctx):
    ctx.send("Dont, plz. Halp")


def main():
    bot.run(TOKEN)


if __name__ == "__main__":
    main()
