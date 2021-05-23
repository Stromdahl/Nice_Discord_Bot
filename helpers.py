from datetime import datetime, timedelta
import discord

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


def score_message(title, scores):
    msg = ""
    for i, count in enumerate(scores):
        v, k = count
        msg += f'\n\t{1 + i}. {k}: {v}'
    return discord.Embed(title=title, description=msg, color=discord.Color.red())