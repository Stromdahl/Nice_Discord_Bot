from mongo_data.Models.score import Score
from mongo_data.Models.message import Message
from mongo_data.Models.guilds import Guild
from secrets.secrets import TOKEN
import discord
from discord.ext import commands
import re
import time


word_list = ["nice", "nojs", "noice", "najs"]
description = f'''A Nice bot by Stroid
you get score by writing one of the following words:"{" ".join(word_list)}"'''


leaderboard_anouncement_cooldown_seconds = 3600

nice_count = dict()
last_score_anouncment = time.time()-leaderboard_anouncement_cooldown_seconds

bot = commands.Bot(command_prefix='!nice ',
                   description=description, activity=discord.Game("!nice help"))


def score_message(guild_id):
    msg = 'NICE LEADERBOARD'
    for i, count in enumerate(Score(guild_id).get()):
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


@bot.command(description="Get the leaderboard")
async def score(ctx):
    await ctx.send(score_message(ctx.guild.id))


@bot.command()
async def wordlist(ctx):
    await ctx.send(f"Words im looking for: {' '.join(word_list)}")


@bot.command(brief='Dont use plz, i give cookies', description='This is only a testing function that the one and only master dev stroid that should use :)')
async def test(ctx):
    print("test")


def main():
    bot.run(TOKEN)


if __name__ == "__main__":
    main()
