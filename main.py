import os
import traceback

import discord
from discord.ext import commands

from modules.grouping import MakeTeam

token = os.environ['DISCORD_BOT_TOKEN']
bot = commands.Bot(command_prefix='/')
old_team_1 = []
old_team_2 = []
old_remainder = []

"""起動処理"""
@bot.event
async def on_ready():
    print('-----Logged in info-----')
    print(bot.user.name)
    print(bot.user.id)
    print(discord.__version__)
    print('------------------------')

"""コマンド実行"""
# @bot.command()
# async def shuffle_mem(ctx):
#     make_team = MakeTeam()
#     await ctx.channel.sed(msg)

@bot.command()
async def delete_mem(ctx, member_name=''):
    global old_remainder
    global old_team_1
    global old_team_2

    make_team = MakeTeam()
    msg, remainder, team_1, team_2 = make_team.splice_team_member(member_name, old_remainder, old_team_1, old_team_2)

    old_remainder = remainder
    old_team_1 = team_1
    old_team_2 = team_2

    await ctx.channel.send(msg)

# メンバー数が均等になるチーム分け
@bot.command()
async def team(ctx, specified_num=2, member_names):
    global old_remainder
    global old_team_1
    global old_team_2

    make_team = MakeTeam()
    remainder_flag = 'true'
    msg, remainder, team_1, team_2 = make_team.make_party_num(ctx, specified_num, remainder_flag, member_names)

    old_remainder = remainder
    old_team_1 = team_1
    old_team_2 = team_2

    await ctx.channel.send(msg)

# メンバー数が均等にはならないチーム分け
@bot.command()
async def team_norem(ctx, specified_num=2):
    make_team = MakeTeam()
    msg = make_team.make_party_num(ctx,specified_num)
    await ctx.channel.send(msg)

# メンバー数を指定してチーム分け
@bot.command()
async def group(ctx, specified_num=1):
    make_team = MakeTeam()
    msg = make_team.make_specified_len(ctx,specified_num)
    await ctx.channel.send(msg)

bot.run(token)
