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

bot = commands.Bot(command_prefix='!nice ', description=description, activity=discord.Game("!nice help"))

def create_regex_pattern(word_list):
    return f'({"|".join(word_list)})'

def get_amount_of_matches(message):
    pattern = create_regex_pattern(word_list)
    return len(re.findall(pattern, message))

def get_score(guild_id):
    total = Guild(str(guild_id)).get_total().items()
    nice_count_view = [ (v,k) for k,v in total]
    nice_count_view.sort(reverse=True)
    return nice_count_view

def score_message(guild_id):
    msg = 'NICE LEADERBOARD'
    for i, count in enumerate(get_score(guild_id)):
        v, k = count
        msg += f'\n\t{1 + i}. {k}: {v}'
    return msg

def add_score(guild_id, channel_id, name, amount):
    Guild(str(guild_id)).post(channel_id, name, amount)

@bot.event
async def on_message(message):
    if message.author.id != bot.user.id and not message.content.startswith("!nice"):
        global last_score_anouncment
        amount = get_amount_of_matches(message.content.lower())
        if amount:
            add_score(message.guild.id, message.channel.id, message.author.name, amount)
            if(time.time() - last_score_anouncment > leaderboard_anouncement_cooldown_seconds):
                await message.channel.send(score_message(message.guild.id))
                last_score_anouncment = time.time()
            return
    await bot.process_commands(message)

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

@bot.command(brief='Dont use plz, i give cookies', description='Dont use plz')
async def test(ctx):
    print("test")


def main():
    bot.run(TOKEN)


if __name__ == "__main__":
    main()
