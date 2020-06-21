import random

import discord
from discord.ext import commands
from cerberus import Validator

class MakeTeam:

    def __init__(self):
        self.channel_mem = []
        self.mem_len = 0
        self.vc_state_err = '実行できません。ボイスチャンネルに入ってコマンドを実行してください。'

    def set_mem(self, ctx):
        state = ctx.author.voice # コマンド実行者のVCステータスを取得
        if state is None: 
            return False

        self.channel_mem = [i.name for i in state.channel.members] # VCメンバリスト取得
        self.mem_len = len(self.channel_mem) # 人数取得
        return True

    # チーム数を指定した場合のチーム分け
    def make_party_num(self, ctx, party_num, remainder_flag='false', member_names=''):
        team = []
        team_1 = []
        team_2 = []
        remainder = []
        designation_member_names = []
        
        if self.set_mem(ctx) is False:
            return self.vc_state_err

        # 指定数の確認
        if party_num > self.mem_len or party_num <= 0:
            return '実行できません。チーム分けできる数を指定してください。(チーム数を指定しない場合は、デフォルトで2が指定されます)'

        # 指定されたメンバーを追加、削除
        if member_names != '':
            designation_member_names = self.channel_mem
            for m in member_names.strip('[]').replace(' ', '').split(','):
                if '-' in m:
                    designation_member_names.remove(m.strip('-'))
                if '+' in m:
                    designation_member_names.append(m.strip('+')) 
            self.channel_mem = designation_member_names

        # メンバーリストをシャッフル
        random.shuffle(self.channel_mem)

        # チーム分けで余るメンバーを取得
        if remainder_flag:
            remainder_num = self.mem_len % party_num
            if remainder_num != 0: 
                for r in range(remainder_num):
                    remainder.append(self.channel_mem.pop())
                team.append("=====余り=====")
                team.extend(remainder)

        # チーム分け
        for i in range(party_num): 
            team.append("=====チーム"+str(i+1)+"=====")
            team.extend(self.channel_mem[i:self.mem_len:party_num])
            if i == 0:
                team_1.extend(self.channel_mem[i:self.mem_len:party_num])
            if i == 1:
                team_2.extend(self.channel_mem[i:self.mem_len:party_num])

        return [('\n'.join(team)), remainder, team_1, team_2]

    # チームのメンバー数を指定した場合のチーム分け
    def make_specified_len(self, ctx, specified_len):
        team = []
        remainder = []

        if self.set_mem(ctx) is False:
            return self.vc_state_err

        # 指定数の確認
        if specified_len > self.mem_len or specified_len <= 0:
            return '実行できません。チーム分けできる数を指定してください。'

        # チーム数を取得
        party_num = self.mem_len // specified_len

        # メンバーリストをシャッフル
        random.shuffle(self.channel_mem)

        # チーム分けで余るメンバーを取得
        remainder_num = self.mem_len % party_num
        if remainder_num != 0: 
            for r in range(remainder_num):
                remainder.append(self.channel_mem.pop())
            team.append("=====余り=====")
            team.extend(remainder)

        # チーム分け
        for i in range(party_num): 
            team.append("=====チーム"+str(i+1)+"=====")
            team.extend(self.channel_mem[i:self.mem_len:party_num])

        return ('\n'.join(team))
    
    def splice_team_member(ctx, member_name, old_remainder, old_team_1, old_team_2):
        team = []

        if member_name == '':
            return

        remainder = [i for i in old_remainder if i != member_name]
        team_1 = [i for i in old_team_1 if i != member_name]
        team_2 = [i for i in old_team_2 if i != member_name]

        if remainder:
            team.append("=====余り=====")
            team.extend(remainder)

        team.append("=====チーム1=====")
        team.extend(team_1)
        team.append("=====チーム2=====")
        team.extend(team_2)

        return [('\n'.join(team)), remainder, team_1, team_2]