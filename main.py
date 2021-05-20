from secrets.secrets import TOKEN
from discord.ext import commands
import discord
import re
import time

class MyClient(discord.Client):
    nice_count = dict()
    last_score_anouncment = time.time()

    def score_message(self):
        nice_count_view = [ (v,k) for k,v in self.nice_count.items() ]
        nice_count_view.sort(reverse=True)

        msg = 'NICE LEADERBOARD'
        for i, count in enumerate(nice_count_view):
            v, k = count
            msg += f'\n\t{1 + i}. {k}: {v}'
        return msg
        

    async def on_ready(self):
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')

    async def on_message(self, message):
        # we do not want the bot to reply to itself
        if message.author.id == self.user.id:
            return

        content = message.content.lower()

        if content.startswith('!nice'):
            content = content.split(" ")
            if len(content) == 1:
                await message.channel.send('Write "!nice help" to get help')
                return

            if content[1] == "help":
                await message.channel.send(
                    '''You collect your daily NicePoints by typing "nice" or "nojs
type "!nice score" to get the current score for everyone
                    ''')
                return

            if content[1] == "score":
                await message.channel.send()
                return

        content = re.findall("(nice|nojs)", content)
        if content:
            author = message.author.name
            try:
                self.nice_count[author] += len(content)
            except KeyError:
                self.nice_count[author] = len(content)
            if(time.time() - self.last_score_anouncment > 1):
                await message.channel.send(self.score_message())
                self.last_score_anouncment = time.time()
            return


client = MyClient()
client.run(TOKEN)
