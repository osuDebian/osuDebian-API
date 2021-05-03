import pymysql
import jsons
from .config import UserConfig
from flask_jsonpify import jsonify
import random
import requests
import time
from pytz import timezone
from datetime import datetime
import circleguard
from discord_webhook import *
import math
from smtplib import SMTP_SSL

serverURL = UserConfig['serverURL']
api = UserConfig['BanchoKey']
mysql_host = UserConfig["MysqlHost"]
mysql_user = UserConfig["MysqlUser"]
mysql_password = UserConfig["MysqlPassword"]
mysql_db = UserConfig["MysqlDb"]
mysql_db2 = UserConfig["MysqlDb2"]

apikeys = []

print("db server connection is ok")

try:
    conn = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, db=mysql_db, charset='utf8')
except:
    exit()

cute_emoji = [ 'Σ(￣□￣;)', 'へ(￣∇￣へ)', '(ㅇ︿ㅇ)', '๑°⌓°๑', '٩(๑`^´๑)۶', '(ง •̀_•́)ง', "٩( 'ω' )و", '(๑╹∀╹๑)', '(╹౪╹*๑)', '٩(๑>∀<๑)۶', '(๑・‿・๑)', '✿˘◡˘✿', '(❀╹◡╹)', 'ʅ（´◔౪◔）ʃ'
 ]

scorerow = [0, 30000, 130000, 340000, 700000, 1250000, 2030000, 3080000, 4440000, 6150000, 8250000, 10780000, 13780000, 17290000, 21350000, 26000000, 31280000, 37230000, 43890000, 51300000, 59500000, 68530000, 78430000, 89240000, 101000000, 113750000, 127530000, 142380000, 158340000, 175450000, 193750000, 213280000, 234080000, 256190000, 279650000, 304500000, 330780000, 358530000, 387790000, 418600000, 451000000, 485030000, 520730000, 558140000, 597300000, 638250000, 681030000, 725680000, 772240000, 820750000, 871250000, 923780000, 978380000, 1035090000, 1093950000, 1155000000, 1218280000, 1283830000, 1351690001, 1421900001, 1494500002, 1569530004, 1647030007, 1727040013, 1809600024, 1894750043, 1982530077, 2072980138, 2166140248, 2262050446, 2360750803, 2462281446, 2566682603, 2673994685, 2784258433, 2897515180, 3013807324, 3133179183, 3255678529, 3381359353, 3510286835, 3642546304, 3778259346, 3917612824, 4060911082, 4208669948, 4361785907, 4521840633, 4691649139, 4876246450, 5084663609, 5333124496, 5650800094, 6090166168, 6745647103, 7787174786, 9520594614, 12496396305, 17705429349, 26931190829]
def get_level(score:int):
    maxscore = int(scorerow[99])
    if score <= 0:
        return 1
    elif score >= maxscore:
        return int(100 + int((score-scorerow[99])/100000000000))
    else:
        for i in range (0, 99):
            scores = scorerow[i]
            if scores > score:
                return i

def getscoretoleve(level:int):
    if int(level) <= 0:
        return 0
    if int(level) <= 100:
        return int(scorerow[level-1])
    else:
        return int(scorerow[99]) + 100000000000 * (level - 100)

def getlevelpercent(score):
    score = int(score)
    baseLevel = get_level(score)
    baseLevelScore = getscoretoleve(baseLevel)
    scoreProgress = score - baseLevelScore
    scoreLevelDiff = getscoretoleve(baseLevel + 1) - baseLevelScore
    res = scoreProgress / scoreLevelDiff + baseLevel
    resRound = round(res,2)

    levels = str(resRound).split(".")
    level = int(levels[0])
    percent = int(levels[1])
    
    if math.isinf(res) or math.isnan(res):
        return 0
    return [level, percent]

def download(url, file_name):
    with open(file_name, "wb") as file:   # open in binary mode
        response = requests.get(url)               # get request
        file.write(response.content)

def replaydownload(relax, id):
    id = str(id)
    now = str(int(time.time()))
    if relax == 0:
        url = "https://debian.moe/web/replays/" + id
    elif relax == 1:
        url = "https://debian.moe/web/replays_relax/" + id

    row = ['regular', 'relax']
    relax= row[relax]
    
    result = "replay/" + relax + "_" + id + "_" + now + ".osr"
    download(url, result)
    return result

def chkreplay(dir, id):
    fmt = "%Y-%m-%d %H:%M:%S %Z%z"
    KST = datetime.now(timezone('Asia/Seoul'))
    kor_time = KST.strftime(fmt)
    replay = circleguard.ReplayPath(str(dir))
    cg = circleguard.Circleguard(api)

    cg.load(replay)

    r_mode = replay.mods
    r_replayid = replay.replay_id
    r_userid = replay.user_id
    r_username = replay.username
    r_mapid = id

    url = UserConfig['AntiCheatLogWebhook']
    webhook = DiscordWebhook(url=url)
    embed = DiscordEmbed(title="Debian Anticheat v1", color=random.randint(0, 16777215), description=f'Request Time: {kor_time}')
    embed.set_timestamp()
    embed.set_footer(text='Debian AntiCheat v1', ts=True)
    embed.add_embed_field(name="Replay Data", value=f"Replay Player: ``{r_username}`` | Mods: ``{r_mode}``", inline=False)

    status = []
    try:
        ur = cg.ur(replay)
        try:
            chk = int(ur)
            ur = round(ur, 1)
        except:
            pass
        status.append({'ur': 'check succesful'})
        embed.add_embed_field(name="Relax Hack Checker", value=f"Successful \n``result``:\n{ur} ur", inline=True)
        print(f'ur check successful: {ur}ur')
    except Exception as e:
        status.append({'ur': 'check failed'})
        embed.add_embed_field(name="Relax Hack Checker", value=f"Failed\n``details``:\n{e} ur", inline=True)
        print(f'ur check failed \n   Details: {e}')

    try:
        snaps = cg.snaps(replay, max_angle=10, min_distance=8)
        status.append({'snaps': 'check succesful'})
        a = len(snaps)
        embed.add_embed_field(name="Correction Checker", value=f"Successful \n``result``:\n{a} snaps detect", inline=True)
        print('snaps check successful')
    except Exception as e:
        status.append({'snaps': 'check failed'})
        embed.add_embed_field(name="Correction Checker", value=f"Failed\n``details``:\n{e}", inline=True)
        print(f'snaps check failed \n   Details: {e}')
        
    try:
        r_mode = str(r_mode)
        if 'DT' in r_mode:
            print("dt detect")
            ftampetime_mode = 'dt'
        elif 'HT' in r_mode:
            print("ht detect")
            ftampetime_mode = 'ht'
        elif 'NM' in r_mode:
            print("nm detect")
            ftampetime_mode = 'nm'
        else:
            print("mode not detect")
            ftampetime_mode = 'raise'
        frametime = cg.frametime(replay, cv=True, mods_unknown=ftampetime_mode)
        frametime = round(frametime, 1)
        status.append({'frametime': 'check succesful'})
        embed.add_embed_field(name="Timewarp Hack Checker", value=f"Successful \n``result``:\n{frametime} avg cv frametime", inline=True)
        print('frametime check successful')
    except Exception as e:
        status.append({'frametime': 'check failed'})
        embed.add_embed_field(name="Timewarp Hack Checker", value=f"Failed\n``details``:\n{e}", inline=True)
        print(f'frametime check failed \n   Details: {e}')

    webhook.add_embed(embed)
    response = webhook.execute()

    result = [{'result': status, 'data': [{'relax check': f"{ur} ur"},{'correction check': f"{snaps}"},{'timewarp check': f"{frametime}"}]}]
    return result

def get_leaderboard(mode, page, relax, type):
    try:
        cur = conn.cursor()    
        cur.execute("select version()")
    except:
        conn = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, db=mysql_db, charset='utf8')
    cur = conn.cursor()   
    if page == 1:
        page = 0
    else:
        page = page - 1
        page = page * 50  
    try:
        relax_ary = ['users_stats', 'rx_stats']
        relax = relax_ary[relax]

        type_ary = ['pp', 'ranked_score']
        type = type_ary[type]

        mode_ary = ['std', 'taiko', 'ctb', 'mania']
        mode = mode_ary[mode]

        try:
            if relax == 0:
                cur.execute(f"SELECT users.id, users.username, {relax}.country, {relax}.pp_{mode} as pp, {relax}.ranked_score_{mode} as score, {relax}.avg_accuracy_{mode} as accuracy ,{relax}.playcount_{mode} as playcount, {relax}.level_{mode} as level FROM Ainu.{relax} AS {relax} JOIN (select * from Ainu.users where NOT ban_datetime > 0) AS users ON users.id = {relax}.id where not ranked_score_{mode} = 0 order by {type}_{mode} desc limit {page}, 50")
            else:
                cur.execute(f"SELECT users.id, users.username, userstats.country, {relax}.pp_{mode} as pp, {relax}.ranked_score_{mode} as score, {relax}.avg_accuracy_{mode} as accuracy ,{relax}.playcount_{mode} as playcount, {relax}.level_{mode} as level FROM Ainu.{relax} AS {relax} JOIN (select * from Ainu.users where NOT ban_datetime > 0) AS users ON users.id = {relax}.id JOIN (select country, id from Ainu.users_stats) as userstats on userstats.id = {relax}.id where not ranked_score_{mode} = 0 order by {type}_{mode} desc limit {page}, 50;")
            row_headers = [x[0] for x in cur.description]
            rv = cur.fetchall()
        except:
            emoji = random.choice(cute_emoji)
            return {'code': '400', 'message': emoji}

        json_data = []
        for result in rv:
            json_data.append(dict(zip(row_headers, result)))

        return json_data
    except Exception as e:
        emoji = random.choice(cute_emoji)
        return {'code': '400', 'message': emoji, 'error': e}

def get_leaderboard2(mode, page, relax, type):
    try:
        cur = conn.cursor()    
        cur.execute("select version()")
    except:
        conn = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, db=mysql_db, charset='utf8')
    cur = conn.cursor()   
    try:
        relax_ary = ['users_stats', 'rx_stats']
        relax = relax_ary[relax]

        type_ary = ['pp', 'ranked_score']
        type = type_ary[type]

        mode_ary = ['std', 'taiko', 'ctb', 'mania']
        mode = mode_ary[mode]
        try:
            cur.execute(f"SELECT users.id, users.username, {relax}.country, {relax}.pp_{mode} as pp, {relax}.ranked_score_{mode} as score, {relax}.avg_accuracy_{mode} as accuracy ,{relax}.playcount_{mode} as playcount, {relax}.level_{mode} as level FROM Ainu.{relax} AS {relax} JOIN (select * from Ainu.users where NOT ban_datetime > 0) AS users ON users.id = {relax}.id where not ranked_score_{mode} = 0 order by {type}_{mode} desc limit {page}, 50")
            row_headers = [x[0] for x in cur.description]
            rv = cur.fetchall()
        except:
            emoji = random.choice(cute_emoji)
            return {'code': '400', 'message': emoji}

        json_data = []
        for result in rv:
            json_data.append(dict(zip(row_headers, result)))

        return json_data
    except Exception as e:
        emoji = random.choice(cute_emoji)
        return {'code': '400', 'message': emoji, 'error': e}


def get_topplay(mode, relax, time):
    try:
        cur = conn.cursor()    
        cur.execute("select version()")
    except:
        conn = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, db=mysql_db, charset='utf8')
    cur = conn.cursor()     
    try:
        relax_ary = ['scores', 'scores_relax']
        relax = relax_ary[relax]

        try:
            if time == 'all':
                cur.execute(f"SELECT SQL_CACHE DISTINCT scoreid, userid, username, beatmap_id, beatmapset_id, song_name, max_combo as fc, combo, mods, time, play_mode, accuracy, pp, rank FROM Ainu.beatmaps as beatmaps JOIN (SELECT id as scoreid, beatmap_md5, userid, combo, mods, time, play_mode, accuracy, pp, rank FROM (SELECT id, beatmap_md5, userid, max_combo as combo, mods, time, play_mode, accuracy, pp, rank, ROW_NUMBER() OVER(PARTITION BY beatmap_md5 ORDER BY pp DESC) as Rowldx FROM Ainu.{relax} WHERE play_mode = {mode} AND completed = 3 AND userid IN (SELECT DISTINCT id FROM Ainu.users WHERE ban_datetime = 0)) as scores WHERE Rowldx = 1) as data on data.beatmap_md5 = beatmaps.beatmap_md5 JOIN (SELECT username, id FROM Ainu.users) as users on users.id = userid ORDER BY pp DESC LIMIT 66")
            if time == 'month':
                cur.execute(f"SELECT SQL_CACHE DISTINCT scoreid, userid, username, beatmap_id, beatmapset_id, song_name, max_combo as fc, combo, mods, time, play_mode, accuracy, pp, rank FROM Ainu.beatmaps as beatmaps JOIN (SELECT id as scoreid, beatmap_md5, userid, combo, mods, time, play_mode, accuracy, pp, rank FROM (SELECT id, beatmap_md5, userid, max_combo as combo, mods, time, play_mode, accuracy, pp, rank, ROW_NUMBER() OVER(PARTITION BY beatmap_md5 ORDER BY pp DESC) as Rowldx FROM Ainu.{relax} WHERE play_mode = {mode} AND completed = 3 AND userid IN (SELECT DISTINCT id FROM Ainu.users WHERE ban_datetime = 0) AND time > UNIX_TIMESTAMP() - 2592000) as scores WHERE Rowldx = 1) as data on data.beatmap_md5 = beatmaps.beatmap_md5 JOIN (SELECT username, id FROM Ainu.users) as users on users.id = userid ORDER BY pp DESC LIMIT 66")
            if time == 'week':
                cur.execute(f"SELECT SQL_CACHE DISTINCT scoreid, userid, username, beatmap_id, beatmapset_id, song_name, max_combo as fc, combo, mods, time, play_mode, accuracy, pp, rank FROM Ainu.beatmaps as beatmaps JOIN (SELECT id as scoreid, beatmap_md5, userid, combo, mods, time, play_mode, accuracy, pp, rank FROM (SELECT id, beatmap_md5, userid, max_combo as combo, mods, time, play_mode, accuracy, pp, rank, ROW_NUMBER() OVER(PARTITION BY beatmap_md5 ORDER BY pp DESC) as Rowldx FROM Ainu.{relax} WHERE play_mode = {mode} AND completed = 3 AND userid IN (SELECT DISTINCT id FROM Ainu.users WHERE ban_datetime = 0) AND time > UNIX_TIMESTAMP() - 604800) as scores WHERE Rowldx = 1) as data on data.beatmap_md5 = beatmaps.beatmap_md5 JOIN (SELECT username, id FROM Ainu.users) as users on users.id = userid ORDER BY pp DESC LIMIT 66")

            first_data = cur.fetchall()
            row_headers = [x[0] for x in cur.description]
            second_data = list(first_data)
            data = []
            for result in second_data:
                data.append(dict(zip(row_headers, result)))

        except Exception as e:
         #   print(e)
            emoji = random.choice(cute_emoji)
            return {'code': '400', 'message': emoji}

        json = {"status": {"code": "200","message": random.choice(cute_emoji)}, "result": data}

        return json
    except:
        emoji = random.choice(cute_emoji)
        return {'code': '400', 'message': emoji}


def get_debianranks(offset, amount, mode, status, query, category, type):
    try:
        cur = conn.cursor()    
        cur.execute("select version()")
    except:
        conn = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, db=mysql_db, charset='utf8')
    cur = conn.cursor()     
    try:
        if "'" in query:
            emoji = random.choice(cute_emoji)
            return {'code': '404', 'message': emoji}
        if '"' in query:
            emoji = random.choice(cute_emoji)
            return {'code': '404', 'message': emoji}

        a = int(-1)

        if type == 0:
            if query == '' or ' ':
                if category == 0:
                    if mode == a:
                        if status == -3: #모든 모드, 모든 랭크상태
                            cur.execute(f"SELECT SQL_CACHE rankedby, beatmap_id, beatmapset_id, CASE WHEN ranked = 0 THEN 'Unranked' WHEN ranked = 2 THEN 'Ranked' WHEN ranked = 4 THEN 'Qualified' WHEN ranked = 5 THEN 'Loved' END ranked, title, artist, creator, bancho.mode, latest_update, debian.passcount FROM Ainu.beatmaps as debian JOIN cheesegull.beatmaps as bancho on bancho.id = debian.beatmap_id GROUP BY beatmapset_id ORDER BY debian.passcount DESC LIMIT {offset},{amount}")
                        else:
                            cur.execute(f"SELECT SQL_CACHE rankedby, beatmap_id, beatmapset_id, CASE WHEN ranked = 0 THEN 'Unranked' WHEN ranked = 2 THEN 'Ranked' WHEN ranked = 4 THEN 'Qualified' WHEN ranked = 5 THEN 'Loved' END ranked, title, artist, creator, bancho.mode, latest_update, debian.passcount FROM Ainu.beatmaps as debian JOIN cheesegull.beatmaps as bancho on bancho.id = debian.beatmap_id WHERE ranked = {status} GROUP BY beatmapset_id ORDER BY debian.passcount DESC LIMIT {offset},{amount}")
                    else: 
                        if status == -3:
                            cur.execute(f"SELECT SQL_CACHE rankedby, beatmap_id, beatmapset_id, CASE WHEN ranked = 0 THEN 'Unranked' WHEN ranked = 2 THEN 'Ranked' WHEN ranked = 4 THEN 'Qualified' WHEN ranked = 5 THEN 'Loved' END ranked, title, artist, creator, bancho.mode, latest_update, debian.passcount FROM Ainu.beatmaps as debian JOIN cheesegull.beatmaps as bancho on bancho.id = debian.beatmap_id WHERE bancho.mode = {mode} GROUP BY beatmapset_id ORDER BY debian.passcount DESC LIMIT {offset},{amount}")
                        else:
                            cur.execute(f"SELECT SQL_CACHE rankedby, beatmap_id, beatmapset_id, CASE WHEN ranked = 0 THEN 'Unranked' WHEN ranked = 2 THEN 'Ranked' WHEN ranked = 4 THEN 'Qualified' WHEN ranked = 5 THEN 'Loved' END ranked, title, artist, creator, bancho.mode, latest_update, debian.passcount FROM Ainu.beatmaps as debian JOIN cheesegull.beatmaps as bancho on bancho.id = debian.beatmap_id WHERE bancho.mode = {mode} AND ranked = {status} GROUP BY beatmapset_id ORDER BY debian.passcount DESC LIMIT {offset},{amount}")
                if category == 1:
                    if mode == a:
                        if status == -3: #모든 모드, 모든 랭크상태
                            cur.execute(f"SELECT SQL_CACHE rankedby, beatmap_id, beatmapset_id, CASE WHEN ranked = 0 THEN 'Unranked' WHEN ranked = 2 THEN 'Ranked' WHEN ranked = 4 THEN 'Qualified' WHEN ranked = 5 THEN 'Loved' END ranked, title, artist, creator, bancho.mode, latest_update, debian.passcount FROM Ainu.beatmaps as debian JOIN cheesegull.beatmaps as bancho on bancho.id = debian.beatmap_id GROUP BY beatmapset_id ORDER BY debian.latest_update DESC LIMIT {offset},{amount}")
                        else:
                            cur.execute(f"SELECT SQL_CACHE rankedby, beatmap_id, beatmapset_id, CASE WHEN ranked = 0 THEN 'Unranked' WHEN ranked = 2 THEN 'Ranked' WHEN ranked = 4 THEN 'Qualified' WHEN ranked = 5 THEN 'Loved' END ranked, title, artist, creator, bancho.mode, latest_update, debian.passcount FROM Ainu.beatmaps as debian JOIN cheesegull.beatmaps as bancho on bancho.id = debian.beatmap_id WHERE bancho.mode = {mode} GROUP BY beatmapset_id ORDER BY debian.latest_update DESC LIMIT {offset},{amount}")
                    else: 
                        if status == -3:
                            cur.execute(f"SELECT SQL_CACHE rankedby, beatmap_id, beatmapset_id, CASE WHEN ranked = 0 THEN 'Unranked' WHEN ranked = 2 THEN 'Ranked' WHEN ranked = 4 THEN 'Qualified' WHEN ranked = 5 THEN 'Loved' END ranked, title, artist, creator, bancho.mode, latest_update, debian.passcount FROM Ainu.beatmaps as debian JOIN cheesegull.beatmaps as bancho on bancho.id = debian.beatmap_id WHERE bancho.mode = {mode} GROUP BY beatmapset_id ORDER BY debian.latest_update DESC LIMIT {offset},{amount}")
                        else:
                            cur.execute(f"SELECT SQL_CACHE rankedby, beatmap_id, beatmapset_id, CASE WHEN ranked = 0 THEN 'Unranked' WHEN ranked = 2 THEN 'Ranked' WHEN ranked = 4 THEN 'Qualified' WHEN ranked = 5 THEN 'Loved' END ranked, title, artist, creator, bancho.mode, latest_update, debian.passcount FROM Ainu.beatmaps as debian JOIN cheesegull.beatmaps as bancho on bancho.id = debian.beatmap_id WHERE bancho.mode = {mode} AND ranked = {status} GROUP BY beatmapset_id ORDER BY debian.latest_update DESC LIMIT {offset},{amount}")
            else:
                if category == 0:
                    if mode == a:
                        if status == -3: #모든 모드, 모든 랭크상태
                            cur.execute(f"SELECT SQL_CACHE rankedby, beatmap_id, beatmapset_id, CASE WHEN ranked = 0 THEN 'Unranked' WHEN ranked = 2 THEN 'Ranked' WHEN ranked = 4 THEN 'Qualified' WHEN ranked = 5 THEN 'Loved' END ranked, title, artist, creator, bancho.mode, latest_update, debian.passcount FROM Ainu.beatmaps as debian JOIN cheesegull.beatmaps as bancho on bancho.id = debian.beatmap_id WHERE CONCAT(title, artist, creator) REGEXP '{query}' GROUP BY beatmapset_id ORDER BY debian.passcount DESC LIMIT {offset},{amount}")
                        else:
                            cur.execute(f"SELECT SQL_CACHE rankedby, beatmap_id, beatmapset_id, CASE WHEN ranked = 0 THEN 'Unranked' WHEN ranked = 2 THEN 'Ranked' WHEN ranked = 4 THEN 'Qualified' WHEN ranked = 5 THEN 'Loved' END ranked, title, artist, creator, bancho.mode, latest_update, debian.passcount FROM Ainu.beatmaps as debian JOIN cheesegull.beatmaps as bancho on bancho.id = debian.beatmap_id WHERE ranked = {status} AND CONCAT(title, artist, creator) REGEXP '{query}' GROUP BY beatmapset_id ORDER BY debian.passcount DESC LIMIT {offset},{amount}")
                    else: 
                        if status == -3:
                            cur.execute(f"SELECT SQL_CACHE rankedby, beatmap_id, beatmapset_id, CASE WHEN ranked = 0 THEN 'Unranked' WHEN ranked = 2 THEN 'Ranked' WHEN ranked = 4 THEN 'Qualified' WHEN ranked = 5 THEN 'Loved' END ranked, title, artist, creator, bancho.mode, latest_update, debian.passcount FROM Ainu.beatmaps as debian JOIN cheesegull.beatmaps as bancho on bancho.id = debian.beatmap_id WHERE bancho.mode = {mode} AND CONCAT(title, artist, creator) REGEXP '{query}' GROUP BY beatmapset_id ORDER BY debian.passcount DESC LIMIT {offset},{amount}")
                        else:
                            cur.execute(f"SELECT SQL_CACHE rankedby, beatmap_id, beatmapset_id, CASE WHEN ranked = 0 THEN 'Unranked' WHEN ranked = 2 THEN 'Ranked' WHEN ranked = 4 THEN 'Qualified' WHEN ranked = 5 THEN 'Loved' END ranked, title, artist, creator, bancho.mode, latest_update, debian.passcount FROM Ainu.beatmaps as debian JOIN cheesegull.beatmaps as bancho on bancho.id = debian.beatmap_id WHERE bancho.mode = {mode} AND ranked = {status} AND CONCAT(title, artist, creator) REGEXP '{query}' GROUP BY beatmapset_id ORDER BY debian.passcount DESC LIMIT {offset},{amount}")
                if category == 1:
                    if mode == a:
                        if status == -3: #모든 모드, 모든 랭크상태
                            cur.execute(f"SELECT SQL_CACHE rankedby, beatmap_id, beatmapset_id, CASE WHEN ranked = 0 THEN 'Unranked' WHEN ranked = 2 THEN 'Ranked' WHEN ranked = 4 THEN 'Qualified' WHEN ranked = 5 THEN 'Loved' END ranked, title, artist, creator, bancho.mode, latest_update, debian.passcount FROM Ainu.beatmaps as debian JOIN cheesegull.beatmaps as bancho on bancho.id = debian.beatmap_id WHERE CONCAT(title, artist, creator) REGEXP '{query}' GROUP BY beatmapset_id ORDER BY debian.latest_update DESC LIMIT {offset},{amount}")
                        else:
                            cur.execute(f"SELECT SQL_CACHE rankedby, beatmap_id, beatmapset_id, CASE WHEN ranked = 0 THEN 'Unranked' WHEN ranked = 2 THEN 'Ranked' WHEN ranked = 4 THEN 'Qualified' WHEN ranked = 5 THEN 'Loved' END ranked, title, artist, creator, bancho.mode, latest_update, debian.passcount FROM Ainu.beatmaps as debian JOIN cheesegull.beatmaps as bancho on bancho.id = debian.beatmap_id WHERE bancho.mode = {mode} AND CONCAT(title, artist, creator) REGEXP '{query}' GROUP BY beatmapset_id ORDER BY debian.latest_update DESC LIMIT {offset},{amount}")
                    else: 
                        if status == -3:
                            cur.execute(f"SELECT SQL_CACHE rankedby, beatmap_id, beatmapset_id, CASE WHEN ranked = 0 THEN 'Unranked' WHEN ranked = 2 THEN 'Ranked' WHEN ranked = 4 THEN 'Qualified' WHEN ranked = 5 THEN 'Loved' END ranked, title, artist, creator, bancho.mode, latest_update, debian.passcount FROM Ainu.beatmaps as debian JOIN cheesegull.beatmaps as bancho on bancho.id = debian.beatmap_id WHERE bancho.mode = {mode} AND CONCAT(title, artist, creator) REGEXP '{query}' GROUP BY beatmapset_id ORDER BY debian.latest_update DESC LIMIT {offset},{amount}")
                        else:
                            cur.execute(f"SELECT SQL_CACHE rankedby, beatmap_id, beatmapset_id, CASE WHEN ranked = 0 THEN 'Unranked' WHEN ranked = 2 THEN 'Ranked' WHEN ranked = 4 THEN 'Qualified' WHEN ranked = 5 THEN 'Loved' END ranked, title, artist, creator, bancho.mode, latest_update, debian.passcount FROM Ainu.beatmaps as debian JOIN cheesegull.beatmaps as bancho on bancho.id = debian.beatmap_id WHERE bancho.mode = {mode} AND ranked = {status} AND CONCAT(title, artist, creator) REGEXP '{query}' GROUP BY beatmapset_id ORDER BY debian.latest_update DESC LIMIT {offset},{amount}")
            
        if type == 1:
            if query == '' or ' ':
                if category == 0:
                    if mode == a:
                        if status == -3: #모든 모드, 모든 랭크상태
                            cur.execute(f"SELECT SQL_CACHE rankedby, beatmap_id, beatmapset_id, CASE WHEN ranked = 0 THEN 'Unranked' WHEN ranked = 2 THEN 'Ranked' WHEN ranked = 4 THEN 'Qualified' WHEN ranked = 5 THEN 'Loved' END ranked, title, artist, creator, bancho.mode, latest_update, debian.passcount FROM Ainu.beatmaps as debian JOIN cheesegull.beatmaps as bancho on bancho.id = debian.beatmap_id WHERE rankedby != 'Bancho' GROUP BY beatmapset_id ORDER BY debian.passcount DESC LIMIT {offset},{amount}")
                        else:
                            cur.execute(f"SELECT SQL_CACHE rankedby, beatmap_id, beatmapset_id, CASE WHEN ranked = 0 THEN 'Unranked' WHEN ranked = 2 THEN 'Ranked' WHEN ranked = 4 THEN 'Qualified' WHEN ranked = 5 THEN 'Loved' END ranked, title, artist, creator, bancho.mode, latest_update, debian.passcount FROM Ainu.beatmaps as debian JOIN cheesegull.beatmaps as bancho on bancho.id = debian.beatmap_id WHERE rankedby != 'Bancho' AND ranked = {status} GROUP BY beatmapset_id ORDER BY debian.passcount DESC LIMIT {offset},{amount}")
                    else: 
                        if status == -3:
                            cur.execute(f"SELECT SQL_CACHE rankedby, beatmap_id, beatmapset_id, CASE WHEN ranked = 0 THEN 'Unranked' WHEN ranked = 2 THEN 'Ranked' WHEN ranked = 4 THEN 'Qualified' WHEN ranked = 5 THEN 'Loved' END ranked, title, artist, creator, bancho.mode, latest_update, debian.passcount FROM Ainu.beatmaps as debian JOIN cheesegull.beatmaps as bancho on bancho.id = debian.beatmap_id WHERE rankedby != 'Bancho' AND bancho.mode = {mode} GROUP BY beatmapset_id ORDER BY debian.passcount DESC LIMIT {offset},{amount}")
                        else:
                            cur.execute(f"SELECT SQL_CACHE rankedby, beatmap_id, beatmapset_id, CASE WHEN ranked = 0 THEN 'Unranked' WHEN ranked = 2 THEN 'Ranked' WHEN ranked = 4 THEN 'Qualified' WHEN ranked = 5 THEN 'Loved' END ranked, title, artist, creator, bancho.mode, latest_update, debian.passcount FROM Ainu.beatmaps as debian JOIN cheesegull.beatmaps as bancho on bancho.id = debian.beatmap_id WHERE rankedby != 'Bancho' AND bancho.mode = {mode} AND ranked = {status} GROUP BY beatmapset_id ORDER BY debian.passcount DESC LIMIT {offset},{amount}")
                if category == 1:
                    if mode == a:
                        if status == -3: #모든 모드, 모든 랭크상태
                            cur.execute(f"SELECT SQL_CACHE rankedby, beatmap_id, beatmapset_id, CASE WHEN ranked = 0 THEN 'Unranked' WHEN ranked = 2 THEN 'Ranked' WHEN ranked = 4 THEN 'Qualified' WHEN ranked = 5 THEN 'Loved' END ranked, title, artist, creator, bancho.mode, latest_update, debian.passcount FROM Ainu.beatmaps as debian JOIN cheesegull.beatmaps as bancho on bancho.id = debian.beatmap_id WHERE rankedby != 'Bancho' GROUP BY beatmapset_id ORDER BY debian.latest_update DESC LIMIT {offset},{amount}")
                        else:
                            cur.execute(f"SELECT SQL_CACHE rankedby, beatmap_id, beatmapset_id, CASE WHEN ranked = 0 THEN 'Unranked' WHEN ranked = 2 THEN 'Ranked' WHEN ranked = 4 THEN 'Qualified' WHEN ranked = 5 THEN 'Loved' END ranked, title, artist, creator, bancho.mode, latest_update, debian.passcount FROM Ainu.beatmaps as debian JOIN cheesegull.beatmaps as bancho on bancho.id = debian.beatmap_id WHERE rankedby != 'Bancho' AND bancho.mode = {mode} GROUP BY beatmapset_id ORDER BY debian.latest_update DESC LIMIT {offset},{amount}")
                    else: 
                        if status == -3:
                            cur.execute(f"SELECT SQL_CACHE rankedby, beatmap_id, beatmapset_id, CASE WHEN ranked = 0 THEN 'Unranked' WHEN ranked = 2 THEN 'Ranked' WHEN ranked = 4 THEN 'Qualified' WHEN ranked = 5 THEN 'Loved' END ranked, title, artist, creator, bancho.mode, latest_update, debian.passcount FROM Ainu.beatmaps as debian JOIN cheesegull.beatmaps as bancho on bancho.id = debian.beatmap_id WHERE rankedby != 'Bancho' AND bancho.mode = {mode} GROUP BY beatmapset_id ORDER BY debian.latest_update DESC LIMIT {offset},{amount}")
                        else:
                            cur.execute(f"SELECT SQL_CACHE rankedby, beatmap_id, beatmapset_id, CASE WHEN ranked = 0 THEN 'Unranked' WHEN ranked = 2 THEN 'Ranked' WHEN ranked = 4 THEN 'Qualified' WHEN ranked = 5 THEN 'Loved' END ranked, title, artist, creator, bancho.mode, latest_update, debian.passcount FROM Ainu.beatmaps as debian JOIN cheesegull.beatmaps as bancho on bancho.id = debian.beatmap_id WHERE rankedby != 'Bancho' AND bancho.mode = {mode} AND ranked = {status} GROUP BY beatmapset_id ORDER BY debian.latest_update DESC LIMIT {offset},{amount}")
            else:
                if category == 0:
                    if mode == a:
                        if status == -3: #모든 모드, 모든 랭크상태
                            cur.execute(f"SELECT SQL_CACHE rankedby, beatmap_id, beatmapset_id, CASE WHEN ranked = 0 THEN 'Unranked' WHEN ranked = 2 THEN 'Ranked' WHEN ranked = 4 THEN 'Qualified' WHEN ranked = 5 THEN 'Loved' END ranked, title, artist, creator, bancho.mode, latest_update, debian.passcount FROM Ainu.beatmaps as debian JOIN cheesegull.beatmaps as bancho on bancho.id = debian.beatmap_id WHERE rankedby != 'Bancho' AND CONCAT(title, artist, creator) REGEXP '{query}' GROUP BY beatmapset_id ORDER BY debian.passcount DESC LIMIT {offset},{amount}")
                        else:
                            cur.execute(f"SELECT SQL_CACHE rankedby, beatmap_id, beatmapset_id, CASE WHEN ranked = 0 THEN 'Unranked' WHEN ranked = 2 THEN 'Ranked' WHEN ranked = 4 THEN 'Qualified' WHEN ranked = 5 THEN 'Loved' END ranked, title, artist, creator, bancho.mode, latest_update, debian.passcount FROM Ainu.beatmaps as debian JOIN cheesegull.beatmaps as bancho on bancho.id = debian.beatmap_id WHERE rankedby != 'Bancho' AND ranked = {status} AND CONCAT(title, artist, creator) REGEXP '{query}' GROUP BY beatmapset_id ORDER BY debian.passcount DESC LIMIT {offset},{amount}")
                    else: 
                        if status == -3:
                            cur.execute(f"SELECT SQL_CACHE rankedby, beatmap_id, beatmapset_id, CASE WHEN ranked = 0 THEN 'Unranked' WHEN ranked = 2 THEN 'Ranked' WHEN ranked = 4 THEN 'Qualified' WHEN ranked = 5 THEN 'Loved' END ranked, title, artist, creator, bancho.mode, latest_update, debian.passcount FROM Ainu.beatmaps as debian JOIN cheesegull.beatmaps as bancho on bancho.id = debian.beatmap_id WHERE rankedby != 'Bancho' AND bancho.mode = {mode} AND CONCAT(title, artist, creator) REGEXP '{query}' GROUP BY beatmapset_id ORDER BY debian.passcount DESC LIMIT {offset},{amount}")
                        else:
                            cur.execute(f"SELECT SQL_CACHE rankedby, beatmap_id, beatmapset_id, CASE WHEN ranked = 0 THEN 'Unranked' WHEN ranked = 2 THEN 'Ranked' WHEN ranked = 4 THEN 'Qualified' WHEN ranked = 5 THEN 'Loved' END ranked, title, artist, creator, bancho.mode, latest_update, debian.passcount FROM Ainu.beatmaps as debian JOIN cheesegull.beatmaps as bancho on bancho.id = debian.beatmap_id WHERE rankedby != 'Bancho' AND bancho.mode = {mode} AND ranked = {status} AND CONCAT(title, artist, creator) REGEXP '{query}' GROUP BY beatmapset_id ORDER BY debian.passcount DESC LIMIT {offset},{amount}")
                if category == 1:
                    if mode == a:
                        if status == -3: #모든 모드, 모든 랭크상태
                            cur.execute(f"SELECT SQL_CACHE rankedby, beatmap_id, beatmapset_id, CASE WHEN ranked = 0 THEN 'Unranked' WHEN ranked = 2 THEN 'Ranked' WHEN ranked = 4 THEN 'Qualified' WHEN ranked = 5 THEN 'Loved' END ranked, title, artist, creator, bancho.mode, latest_update, debian.passcount FROM Ainu.beatmaps as debian JOIN cheesegull.beatmaps as bancho on bancho.id = debian.beatmap_id WHERE rankedby != 'Bancho' AND CONCAT(title, artist, creator) REGEXP '{query}' GROUP BY beatmapset_id ORDER BY debian.latest_update DESC LIMIT {offset},{amount}")
                        else:
                            cur.execute(f"SELECT SQL_CACHE rankedby, beatmap_id, beatmapset_id, CASE WHEN ranked = 0 THEN 'Unranked' WHEN ranked = 2 THEN 'Ranked' WHEN ranked = 4 THEN 'Qualified' WHEN ranked = 5 THEN 'Loved' END ranked, title, artist, creator, bancho.mode, latest_update, debian.passcount FROM Ainu.beatmaps as debian JOIN cheesegull.beatmaps as bancho on bancho.id = debian.beatmap_id WHERE rankedby != 'Bancho' AND bancho.mode = {mode} AND CONCAT(title, artist, creator) REGEXP '{query}' GROUP BY beatmapset_id ORDER BY debian.latest_update DESC LIMIT {offset},{amount}")
                    else: 
                        if status == -3:
                            cur.execute(f"SELECT SQL_CACHE rankedby, beatmap_id, beatmapset_id, CASE WHEN ranked = 0 THEN 'Unranked' WHEN ranked = 2 THEN 'Ranked' WHEN ranked = 4 THEN 'Qualified' WHEN ranked = 5 THEN 'Loved' END ranked, title, artist, creator, bancho.mode, latest_update, debian.passcount FROM Ainu.beatmaps as debian JOIN cheesegull.beatmaps as bancho on bancho.id = debian.beatmap_id WHERE rankedby != 'Bancho' AND bancho.mode = {mode} AND CONCAT(title, artist, creator) REGEXP '{query}' GROUP BY beatmapset_id ORDER BY debian.latest_update DESC LIMIT {offset},{amount}")
                        else:
                            cur.execute(f"SELECT SQL_CACHE rankedby, beatmap_id, beatmapset_id, CASE WHEN ranked = 0 THEN 'Unranked' WHEN ranked = 2 THEN 'Ranked' WHEN ranked = 4 THEN 'Qualified' WHEN ranked = 5 THEN 'Loved' END ranked, title, artist, creator, bancho.mode, latest_update, debian.passcount FROM Ainu.beatmaps as debian JOIN cheesegull.beatmaps as bancho on bancho.id = debian.beatmap_id WHERE rankedby != 'Bancho' AND bancho.mode = {mode} AND ranked = {status} AND CONCAT(title, artist, creator) REGEXP '{query}' GROUP BY beatmapset_id ORDER BY debian.latest_update DESC LIMIT {offset},{amount}")
            
            
        first_data = cur.fetchall()
        row_headers = [x[0] for x in cur.description]
        second_data = list(first_data)
        data = []
        for result in second_data:
            data.append(dict(zip(row_headers, result)))

        json = {"status": {"code": "200","message": random.choice(cute_emoji)}, "result": data}

        return json

    except Exception as e:
        emoji = random.choice(cute_emoji)
        return {'code': '403', 'message': emoji}



def get_beatmap(type, b_id, b_setid, b_name, b_md5):
    try:
        cur = conn.cursor()    
        cur.execute("select version()")
    except:
        conn = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, db=mysql_db, charset='utf8')
    cur = conn.cursor()     
    try:
        try:
            if type == 0:
                cur.execute(f"SELECT SQL_CACHE rankedby, beatmap_id, beatmapset_id, debian.beatmap_md5, CASE WHEN ranked = 0 THEN 'Unranked' WHEN ranked = 2 THEN 'Ranked' WHEN ranked = 4 THEN 'Qualified' WHEN ranked = 5 THEN 'Loved' END ranked, debian.song_name, title, artist, creator, bancho.mode, debian.bpm, debian.ar, debian.cs, debian.od, debian.hp, debian.playcount, debian.passcount FROM Ainu.beatmaps as debian JOIN cheesegull.beatmaps as bancho on bancho.id = debian.beatmap_id WHERE beatmap_id = {b_id}")
            if type == 1:
                cur.execute(f"SELECT SQL_CACHE rankedby, beatmap_id, beatmapset_id, debian.beatmap_md5, CASE WHEN ranked = 0 THEN 'Unranked' WHEN ranked = 2 THEN 'Ranked' WHEN ranked = 4 THEN 'Qualified' WHEN ranked = 5 THEN 'Loved' END ranked, debian.song_name, title, artist, creator, bancho.mode, debian.bpm, debian.ar, debian.cs, debian.od, debian.hp, debian.playcount, debian.passcount FROM Ainu.beatmaps as debian JOIN cheesegull.beatmaps as bancho on bancho.id = debian.beatmap_id WHERE beatmapset_id = {b_setid}")
            if type == 2:
                cur.execute(f"SELECT rankedby, beatmap_id, beatmapset_id, beatmap_md5, song_name, ar, od, cs, hp, mode, difficulty_std, difficulty_taiko, difficulty_ctb, difficulty_mania, max_combo, bpm, ranked_status_freezed, artist, creator, title, version, pp_100, pp_99, pp_98, pp_95 FROM beatmaps WHERE song_name LIKE '%{b_name}%'")
            if type == 3:
                cur.execute(f"SELECT rankedby, beatmap_id, beatmapset_id, beatmap_md5, song_name, ar, od, cs, hp, mode, difficulty_std, difficulty_taiko, difficulty_ctb, difficulty_mania, max_combo, bpm, ranked_status_freezed, artist, creator, title, version, pp_100, pp_99, pp_98, pp_95 FROM beatmaps WHERE beatmap_md5 = '{b_md5}'")
            row_headers = [x[0] for x in cur.description]
            rv = cur.fetchall()
        except:
            emoji = random.choice(cute_emoji)
            return {'code': '400', 'message': emoji}
        json_data = []
        if str(rv) == '()' or str(rv) == '( )':
            emoji = random.choice(cute_emoji)
            return {'code': '400', 'message': emoji}

        for result in rv:
            json_data.append(dict(zip(row_headers, result)))

        json = {"status": {"code": "200","message": random.choice(cute_emoji)}, "data": json_data}

        return json
    except:
        emoji = random.choice(cute_emoji)
        return {'code': '400', 'message': emoji}


def record_userscore_data(userid, relax):
    try:
        cur = conn.cursor()    
        cur.execute("select version()")
    except:
        conn = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, db=mysql_db, charset='utf8')
    cur = conn.cursor()     
    try:
        if relax == 0:
            try:
                cur.execute(f"SELECT * FROM users_stats WHERE id = {userid}")
            except:
                emoji = random.choice(cute_emoji)
                return {'code': '400', 'message': emoji}
        elif relax == 1:
            try:
                cur.execute(f"SELECT * FROM rx_stats WHERE id = {userid}")
            except:
                emoji = random.choice(cute_emoji)
                return {'code': '400', 'message': emoji}

        userdata = cur.fetchone()
        now_datetime = time.strftime('%Y-%m-%d %H:%M:%S')
        now_timestamp = int(time.time())

        u_id = userdata[0]
        u_name = userdata[1]

        if relax == 0:
            u_ppstd = userdata[41]
            u_pptaiko = userdata[42]
            u_ppctb = userdata[43]
            u_ppmania = userdata[44]

        elif relax == 1:
            u_ppstd = userdata[34]
            u_pptaiko = userdata[35]
            u_ppctb = userdata[36]
            u_ppmania = userdata[37]
        
        try:
            cur.execute(f"INSERT INTO pp_graph VALUES ({u_id}, '{u_name}', {u_ppstd}, {u_pptaiko}, {u_ppctb}, {u_ppmania}, {relax}, '{now_datetime}', {now_timestamp})")
            conn.commit()
            
        except Exception as e:
                emoji = random.choice(cute_emoji)
                return {'code': '400', 'message': emoji, 'error': e}

        data = {'userid': u_id, 'username': u_name, 'is_relax': relax}, {'record': 'ok'}
                

        json = {"status": {"code": "200","message": random.choice(cute_emoji)}, "result": data}

        return json    


    except Exception as e:
        emoji = random.choice(cute_emoji)
        return {'code': '400', 'message': emoji, 'error': e}

def get_mode_user_rank():
    try:
        cur = conn.cursor()    
        cur.execute("select version()")
    except:
        conn = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, db=mysql_db, charset='utf8')
    cur = conn.cursor()     
    try:
        try:
            cur.execute(f"create temporary table AB3F select us.* from Ainu.users as u join (select * from Ainu.users_stats) as us on u.id = us.id where u.ban_datetime = 0;")
            cur.execute(f"create temporary table AB40 select us.* from Ainu.users as u join (select * from Ainu.rx_stats) as us on u.id = us.id where u.ban_datetime = 0;")
            conn.commit()
        except:
            emoji = random.choice(cute_emoji)
            return {'code': '400', 'message': emoji}

        cur.execute(f"select n.id, n.username, n.S as std_rank, n.T as taiko_rank, n.C as catch_rank, n.M as mania_rank, rx.S_R as rx_std_rank, rx.T_R as rx_taiko_rank, rx.C_R as rx_catch_rank from (select s.id, s.username, s.rank as S, t.rank as T, c.rank as C, m.rank as M from (SELECT @RANKs := @RANKs + 1 AS rank, id, username, @LASTs := pp_std as pp FROM AB3F, (SELECT @RANKs := 0)  XXs ORDER BY pp_std DESC )as s join (SELECT @RANKt := @RANKt + 1 AS rank, id, @LASTt := pp_taiko as pp FROM AB3F, (SELECT @RANKt := 0)  XXt ORDER BY pp_taiko DESC )as t on s.id = t.id join (SELECT @RANKc := @RANKc + 1 AS rank, id, @LASTc := pp_ctb as pp FROM AB3F, (SELECT @RANKc := 0)  XXc ORDER BY pp_ctb DESC )as c on s.id = c.id join (SELECT @RANKm := @RANKm + 1 AS rank, id, @LASTm := pp_mania as pp FROM AB3F, (SELECT @RANKm := 0)  XXm ORDER BY pp_mania DESC )as m on s.id = m.id) as n join (select s.id, s.rank as S_R, t.rank as T_R, c.rank as C_R from (SELECT @RANKs_R := @RANKs_R + 1 AS rank, id, username, @LASTs_R := pp_std as pp FROM AB40, (SELECT @RANKs_R := 0)  XXs ORDER BY pp_std DESC )as s join (SELECT @RANKt_R := @RANKt_R + 1 AS rank, id, @LASTt_R := pp_taiko as pp FROM AB40, (SELECT @RANKt_R := 0)  XXt ORDER BY pp_taiko DESC )as t on s.id = t.id join (SELECT @RANKc_R := @RANKc_R + 1 AS rank, id, @LASTc_R := pp_ctb as pp FROM AB40, (SELECT @RANKc_R := 0)  XXc ORDER BY pp_ctb DESC )as c on s.id = c.id) as rx on rx.id =n.id;")
        first_data = cur.fetchall()
        row_headers = [x[0] for x in cur.description]

        cur.execute(f"drop temporary table AB3F,AB40;")
        conn.commit()
        second_data = list(first_data)
        data = []
        for result in second_data:
            data.append(dict(zip(row_headers, result)))

        a = data['result']
        json = {"status": {"code": "200","message": random.choice(cute_emoji)}, "result": data}

        return json    


    except Exception as e:
        emoji = random.choice(cute_emoji)
        return {'code': '400', 'message': emoji, 'error': e}

def get_beatmap_set_data(b_id):
    try:
        cur = conn.cursor()    
        cur.execute("select version()")
    except:
        conn = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, db=mysql_db, charset='utf8')
    cur = conn.cursor()     
    try:
        try:
            cur.execute(f"SELECT SQL_CACHE rankedby, beatmap_id, beatmapset_id, debian.beatmap_md5, CASE WHEN ranked = 0 THEN 'Unranked' WHEN ranked = 2 THEN 'Ranked' WHEN ranked = 4 THEN 'Qualified' WHEN ranked = 5 THEN 'Loved' END ranked, debian.song_name, title, artist, creator, bancho.mode, bancho.difficulty_rating, debian.bpm, debian.ar, debian.cs, debian.od, debian.hp, debian.playcount, debian.passcount FROM Ainu.beatmaps as debian JOIN cheesegull.beatmaps as bancho on bancho.id = debian.beatmap_id WHERE beatmapset_id = {b_id} ORDER BY bancho.difficulty_rating ASC;")
            beatmap_data = cur.fetchall()
        except:
            emoji = random.choice(cute_emoji)
            return {'code': '400', 'message': emoji}     

        row_headers = [x[0] for x in cur.description]
        second_data = list(beatmap_data)
        data = []
        for result in second_data:
            data.append(dict(zip(row_headers, result)))

        return jsonify(data)

    except Exception as e:
        emoji = random.choice(cute_emoji)
        return {'code': '400', 'message': emoji, 'error': e}

def get_beatmap_score_data(beatmap_id,relax, mode):
    try:
        try:
            conn = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, db=mysql_db, charset='utf8')
        except:
            exit()
        cur = conn.cursor()
        try:
            cur.execute(f"select beatmap_id from beatmaps where beatmap_id = {beatmap_id}")
            chkdata = cur.fetchone()
            beatmap_id = chkdata[0]
        except:
            print(f'{beatmap_id} | 비트맵 데이터가 발견되지 않아 등록을 시도합니다.')
            reqjson = requests.get(url=f"https://old.{serverURL}/letsapi/v1/pp?b={beatmap_id}").json()  

        try:
            cur.execute(f"SELECT SQL_CACHE DISTINCT rankedby, beatmap_id, beatmapset_id, debian.beatmap_md5, FROM_UNIXTIME(debian.latest_update, '%Y-%m-%d %H:%i') as ranking_time, CASE WHEN ranked = 0 THEN 'Unranked' WHEN ranked = 2 THEN 'Ranked' WHEN ranked = 4 THEN 'Qualified' WHEN ranked = 5 THEN 'Loved' END ranked, debian.song_name, title, artist, creator, debian.hit_length as time, bancho.mode, CAST(bancho.difficulty_rating AS float) as diff, debian.bpm, debian.ar, debian.cs, debian.od, debian.hp, debian.playcount, debian.passcount, debian.max_combo FROM Ainu.beatmaps as debian JOIN cheesegull.beatmaps as bancho on bancho.id = debian.beatmap_id WHERE beatmap_id = {beatmap_id}")
            beatmap_data = cur.fetchall()
            row_headers = [x[0] for x in cur.description]
            beatmap_md5 = beatmap_data[0][3]
            uname = beatmap_data[0][0]
            set_id = beatmap_data[0][2]
            second_data = list(beatmap_data)
            beatmap_data = []
            for result in second_data:
                beatmap_data.append(dict(zip(row_headers, result)))
        except:
            cur.execute(f"select SQL_CACHE DISTINCT mode from beatmaps where beatmap_id = {beatmap_id}")
            set_iddata = cur.fetchone()
            mode_before = int(set_iddata[0])
            if mode_before == 0:
                diff_get = 'std'
            elif mode_before == 1:
                diff_get = 'taiko'
            elif mode_before == 2:
                diff_get = 'ctb'
            elif mode_before == 3:
                diff_get = 'mania'
            cur.execute(f"SELECT SQL_CACHE DISTINCT rankedby, beatmap_id, beatmapset_id, debian.beatmap_md5, FROM_UNIXTIME(debian.latest_update, '%Y-%m-%d %H:%i') as ranking_time, CASE WHEN ranked = 0 THEN 'Unranked' WHEN ranked = 2 THEN 'Ranked' WHEN ranked = 4 THEN 'Qualified' WHEN ranked = 5 THEN 'Loved' END ranked, debian.song_name, title, artist, creator, debian.hit_length as time, debian.mode, CAST(debian.difficulty_{diff_get} AS float) as diff, debian.bpm, debian.ar, debian.cs, debian.od, debian.hp, debian.playcount, debian.passcount, debian.max_combo FROM Ainu.beatmaps as debian WHERE beatmap_id = {beatmap_id};")
            beatmap_data = cur.fetchall()
            row_headers = [x[0] for x in cur.description]
            beatmap_md5 = beatmap_data[0][3]
            uname = beatmap_data[0][0]
            set_id = beatmap_data[0][2]
            second_data = list(beatmap_data)
            beatmap_data = []
            for result in second_data:
                beatmap_data.append(dict(zip(row_headers, result)))

        
        apikey = random.choice(apikeys)
        reqjson = requests.get(url=f"https://osu.ppy.sh/api/get_beatmaps?k={apikey}&s={set_id}").json()
        b_count = len(reqjson)
        row = ['beatmapset_id', 'beatmap_id', 'mode', 'version', 'diff', 'diffclass', 'modeclass', 'last_update']
        b_data = []

        for i in range (0, b_count):
            setid = int(reqjson[i]['beatmapset_id'])        
            bid = int(reqjson[i]['beatmap_id'])        
            bmode = int(reqjson[i]['mode'])       
            version = reqjson[i]['version']  
            last_update = reqjson[i]['last_update']  
            if bid == beatmap_id:
                bancho_last_update = last_update
            diff = round(float(reqjson[i]['difficultyrating']), 2)
            if diff < 2:
                if bid == beatmap_id:
                    diffclass = 'easy selected'
                else:
                    diffclass = 'easy'
            elif diff >= 2 and diff <= 2.69:
                if bid == beatmap_id:
                    diffclass = 'normal selected'
                else:
                    diffclass = 'normal'
            elif diff >= 2.7 and diff <= 3.99:
                if bid == beatmap_id:
                    diffclass = 'hard selected'
                else:
                    diffclass = 'hard'
            elif diff >= 4 and diff <= 5.29:
                if bid == beatmap_id:
                    diffclass = 'insane selected'
                else:
                    diffclass = 'insane'
            elif diff >= 5.3:
                if bid == beatmap_id:
                    diffclass = 'expert selected'
                else:
                    diffclass = 'expert'
            if bmode == 0:
                modeclass = 'osu' 
            elif bmode == 1:
                modeclass = 'taiko'  
            elif bmode == 2:
                modeclass = 'fruits' 
            elif bmode == 3:
                modeclass = 'mania' 
            b_datas = [setid, bid, bmode, version, diff, diffclass, modeclass, last_update]
            b_data.append(dict(zip(row, b_datas)))

        if uname == 'Bancho':
            bn_data = [{'userid': 999, 'username': 'Bancho', 'last_update': last_update}]
        else:
            try:
                sqlopen = open("./bin/sql/scoreboard/user.sql", 'r')
                sql = (sqlopen.read()).format(uname)
                cur.execute(sql)
                try:
                    dd = str(cur.fetchone()[0])
                    bn_data = jsons.loads(dd)
                except:
                    sqlopen = open("./bin/sql/scoreboard/user2.sql", 'r')
                    sql = (sqlopen.read()).format(uname)
                    cur.execute(sql)
                    dd = str(cur.fetchone()[0])
                    bn_data = jsons.loads(dd)
                id = bn_data['userid']
            except:
                bn_data = [{'username': 'Bancho', 'userid': 999, 'last_update': last_update}]

        ppscore = ['score', 'pp']
        score_type = ppscore[relax]
        relax_row = ['scores', 'scores_relax']
        relax = relax_row[relax]

        try:
            sqlopen = open("./bin/sql/scoreboard/score.sql", 'r')
            sql = (sqlopen.read()).format(beatmap_md5, mode, score_type, relax)
            cur.execute(sql)
            try:
                dd = str(cur.fetchone()[0])
                score_data = jsons.loads(dd)
            except:
                score_data = []
            sqlopen.close()
        except Exception as e:     
            score_data = []

        try:
            sqlopen2 = open("./bin/sql/scoreboard/top_score.sql", 'r')
            sql = (sqlopen2.read()).format(beatmap_md5, mode, score_type, relax)
            cur.execute(sql)
            try:
                dd = str(cur.fetchone()[0])
                topscore_data = jsons.loads(dd)
            except:
                topscore_data = []
            sqlopen.close()
        except Exception as e:
            topscore_data = []

        json = {"status": {"code": "200","message": random.choice(cute_emoji)}, "result": {'beatmapset': b_data, 'bn': bn_data,'beatmap': beatmap_data, 'topscore': topscore_data, 'score': score_data}}

        return json
        
    except Exception as e:
        emoji = random.choice(cute_emoji)
        return {'code': '400', 'message': emoji, 'error': e}

def get_beatmap_score_data_score(beatmap_id,relax, mode):
    try:
        cur = conn.cursor()    
        cur.execute("select version()")
    except:
        conn = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, db=mysql_db, charset='utf8')
    cur = conn.cursor()       
    try:
        try:
            sqlopen = open("./bin/sql/scoreboard/get_beatmap_md5.sql", 'r')
            sql = (sqlopen.read()).format(beatmap_id)
            cur.execute(sql)
            beatmap = cur.fetchone()
            beatmap_md5 = beatmap[0]
        except:
            emoji = random.choice(cute_emoji)
            return {'code': '400', 'message': emoji}

        ppscore = ['score', 'pp']
        score_type = ppscore[relax]
        relax_row = ['scores', 'scores_relax']
        relax = relax_row[relax]    

        try:
            sqlopen = open("./bin/sql/scoreboard/score.sql", 'r')
            sql = (sqlopen.read()).format(beatmap_md5, mode, score_type, relax)
            cur.execute(sql)
            try:
                dd = str(cur.fetchone()[0])
                score_data = jsons.loads(dd)
            except:
                score_data = []
                pass
        except Exception as e:     
            score_data = []

        try:
            sqlopen2 = open("./bin/sql/scoreboard/top_score.sql", 'r')
            sql = (sqlopen2.read()).format(beatmap_md5, mode, score_type, relax)
            cur.execute(sql)
            try:
                dd = str(cur.fetchone()[0])
                topscore_data = jsons.loads(dd)
            except:
                topscore_data = []
            sqlopen.close()
        except Exception as e:
            topscore_data = []

        json = {"status": {"code": "200","message": random.choice(cute_emoji)}, "result": {'score': score_data, 'topscore': topscore_data}}
        return json
    except Exception as e:
        emoji = random.choice(cute_emoji)
        return {'code': '400', 'message': emoji,     'error': e}

def get_beatmap_score_data_beatmap(beatmap_id):
    try:
        cur = conn.cursor()    
        cur.execute("select version()")
    except:
        conn = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, db=mysql_db, charset='utf8')
    cur = conn.cursor()     
    try:
        try:
            cur.execute(f"select beatmap_id from beatmaps where beatmap_id = {beatmap_id}")
            chkdata = cur.fetchone()
            beatmap_id = chkdata[0]
        except:

            reqjson = requests.get(url=f"https://old.debian.moe/letsapi/v1/pp?b={beatmap_id}").json()  

        try:
            sqlopen = open("./bin/sql/scoreboard/beatmap.sql", 'r')
            sql = (sqlopen.read()).format(beatmap_id)
            cur.execute(sql)
            try:
                dd = str(cur.fetchone()[0])
                beatmap_data = jsons.loads(dd)
            except:
                cur.execute(f"select SQL_CACHE DISTINCT mode from beatmaps where beatmap_id = {beatmap_id}")
                set_iddata = cur.fetchone()
                mode_before = int(set_iddata[0])
                if mode_before == 0:
                    diff_get = 'std'
                elif mode_before == 1:
                    diff_get = 'taiko'
                elif mode_before == 2:
                    diff_get = 'ctb'
                elif mode_before == 3:
                    diff_get = 'mania'
                sqlopen = open("./bin/sql/scoreboard/beatmap2.sql", 'r')
                sql = (sqlopen.read()).format(beatmap_id, diff_get)
                cur.execute(sql)
                try:
                    dd = str(cur.fetchone()[0])
                except:
                    emoji = random.choice(cute_emoji)
                    return {'code': '400', 'message': emoji}
                beatmap_data = jsons.loads(dd)
            beatmap_md5 = beatmap_data['beatmap_md5']
            uname = beatmap_data['rankedby']
            set_id = beatmap_data['beatmapset_id']
        except Exception as e:
            emoji = random.choice(cute_emoji)
            return {'code': '400', 'message': emoji, 'error': e}

        if uname == 'Bancho':
            bn_data = [{'userid': 999, 'username': 'Bancho'}]
        else:
            try:
                sqlopen = open("./bin/sql/scoreboard/user.sql", 'r')
                sql = (sqlopen.read()).format(uname)
                cur.execute(sql)
                try:
                    dd = str(cur.fetchone()[0])     
                    bn_data = jsons.loads(dd)
                except:
                    try:
                        sqlopen = open("./bin/sql/scoreboard/user2.sql", 'r')
                        sql = (sqlopen.read()).format(uname)
                        cur.execute(sql)
                        try:
                            dd = str(cur.fetchone()[0])
                            bn_data = jsons.loads(dd)
                        except:
                            bn_data = [{'username': uname, 'userid': 999}]  
                    except:
                        bn_data = [{'username': uname, 'userid': 999}]  
                id = bn_data['userid']
            except:
                bn_data = [{'username': uname, 'userid': 999}]  

        
        apikey = random.choice(apikeys)
        reqjson = requests.get(url=f"https://osu.ppy.sh/api/get_beatmaps?k={apikey}&s={set_id}").json()
        b_count = len(reqjson)
        row = ['beatmapset_id', 'beatmap_id', 'mode', 'version', 'diff', 'diffclass', 'modeclass']
        b_data = []
        for i in range (0, b_count):
            setid = int(reqjson[i]['beatmapset_id'])        
            bid = int(reqjson[i]['beatmap_id'])        
            bmode = int(reqjson[i]['mode'])       
            version = reqjson[i]['version']  
            diff = round(float(reqjson[i]['difficultyrating']), 2)
            if diff < 2:
                if bid == beatmap_id:
                    diffclass = 'easy selected'
                else:
                    diffclass = 'easy'
            elif diff >= 2 and diff <= 2.69:
                if bid == beatmap_id:
                    diffclass = 'normal selected'
                else:
                    diffclass = 'normal'
            elif diff >= 2.7 and diff <= 3.99:
                if bid == beatmap_id:
                    diffclass = 'hard selected'
                else:
                    diffclass = 'hard'
            elif diff >= 4 and diff <= 5.29:
                if bid == beatmap_id:
                    diffclass = 'insane selected'
                else:
                    diffclass = 'insane'
            elif diff >= 5.3:
                if bid == beatmap_id:
                    diffclass = 'expert selected'
                else:
                    diffclass = 'expert'
            if bmode == 0:
                modeclass = 'osu' 
            elif bmode == 1:
                modeclass = 'taiko'  
            elif bmode == 2:
                modeclass = 'fruits' 
            elif bmode == 3:
                modeclass = 'mania' 
            b_datas = [setid, bid, bmode, version, diff, diffclass, modeclass]
            b_data.append(dict(zip(row, b_datas)))

        json = {"status": {"code": "200","message": random.choice(cute_emoji)}, "result": {'beatmapset': b_data, 'bn': bn_data,'beatmap': beatmap_data}}

        return json
    except Exception as e:
        emoji = random.choice(cute_emoji)
        return {'code': '400', 'message': emoji, 'error': e}

def get_user_ppgraph(userid, relax, mode, types):
    mod = mode
    if mode == 3 and relax == 1:
        return {'data': [[0, None]]}
    try:
        cur = conn.cursor()    
        cur.execute("select version()")
    except:
        conn = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, db=mysql_db, charset='utf8')
    cur = conn.cursor()
    moderow = ["std", "taiko", "catch", "mania"]
    mode2row = ["S", "T", "C", "M"]
    mode = moderow[mod]
    mode2 = mode2row[mod]
    try:
        print(types)
        if relax == 0:
            sql = f"select {mode}_rank, {mode2}_PP, to_days(now())-to_days(KST) as KST, UNIX_timestamp FROM thftgr.userRankHistory WHERE id = {userid} order by UNIX_timestamp desc limit 30"
        else:
            sql = f"select rx_{mode}_rank, R_{mode2}_PP, to_days(now())-to_days(KST) as KST, UNIX_timestamp FROM thftgr.userRankHistory WHERE id = {userid} order by UNIX_timestamp desc limit 30"
        cur.execute(sql)
        a = cur.fetchall()
        num = len(a)
        row = ['Rank', 'PP', 'Labels']
        u_data = []
        if num == 0:
            return {'data': ''}
        for i in range(0, num):
            data = a[i]
            if types == 1:
                pp = str(int(data[0]))
            else:
                pp = str(data[1])
            time = -data[2]
            if not time == 0 and pp == '0':
                pp = None
            u_datas = [time, pp]
            u_data.append(u_datas)
        reverse_u_data = u_data[::-1]
        return {'data': reverse_u_data}

    except Exception as e:
        emoji = random.choice(cute_emoji)
        return {'code': '400', 'message': emoji, 'error': e}

def get_user_data(userid, relax, mode):
    try:
        cur = conn.cursor()    
        cur.execute("select version()")
    except:
        conn = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, db=mysql_db, charset='utf8')
    cur = conn.cursor()     
    try:
        try:
            if relax == 0:
                sqlopen = open("./bin/sql/user_data/regular.sql", 'r')
            elif relax == 1:
                sqlopen = open("./bin/sql/user_data/relax.sql", 'r')
            moderow = ['std', 'taiko', 'ctb', 'mania']
            mods = moderow[mode]
            sql = (sqlopen.read()).format(userid, mods)
            cur.execute(sql)
            try:
                first_data = cur.fetchall() 
                score = int(first_data[0][5])
                row_headers = [x[0] for x in cur.description]
                row_headers.insert(5, 'level')
                row_headers.insert(6, 'levelpercent')
                lvdata = (getlevelpercent(score))[0]
                lvpercentdata = (getlevelpercent(score))[1]
                dbdata = first_data[0]
                dbdatalist = list(dbdata)
                dbdatalist.insert(5, lvdata)
                dbdatalist.insert(6, lvpercentdata)
                first_data = tuple(dbdatalist)
                zipdata = zip(row_headers, dbdatalist)
                data = dict(zipdata)
            except:
                data = []
            sqlopen.close()
        except Exception as e:
            data = []   
    
        json = {'status': '200', 'result': data}   

        return json
    except Exception as e:
        emoji = random.choice(cute_emoji)
        return {'code': '4000', 'message': emoji, 'error': e}


def get_bancho_user_gay(username):
    try:
        cur = conn.cursor()    
        cur.execute("select version()")
    except:
        conn = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, db=mysql_db, charset='utf8')
    cur = conn.cursor()     
    
    apikey = random.choice(apikeys)
    reqjson = requests.get(url=f"https://osu.ppy.sh/api/get_user?k={apikey}&u={username}").json()
    u_id = reqjson[0]['user_id']
    return {'userid': u_id}


def get_user_recent_play(userid, relax, mode, page):
    try:
        cur = conn.cursor()    
        cur.execute("select version()")
    except:
        conn = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, db=mysql_db, charset='utf8')
    cur = conn.cursor()     
    try:
        if page == 0 or page == 1:
            page = 10
        else:
            page = page * 10
        try:
            if relax == 0:
                sqlopen = open("./bin/sql/recent_play/regular.sql", 'r')
            elif relax == 1:
                sqlopen = open("./bin/sql/recent_play/relax.sql", 'r')
            sql = (sqlopen.read()).format(userid, mode, page)
            cur.execute(sql)
            try:
                first_data = cur.fetchall()
                row_headers = [x[0] for x in cur.description]
                second_data = list(first_data)
                data = []
                for result in second_data:
                    data.append(dict(zip(row_headers, result)))
            except:
                data = []
            sqlopen.close()
        except Exception as e:
            data = []   
    
        json = {'status': '200', 'result': data}   

        return json
    except Exception as e:
        emoji = random.choice(cute_emoji)
        return {'code': '4000', 'message': emoji, 'error': e}

def get_user_best_play(userid, relax, mode, page):
    try:
        cur = conn.cursor()    
        cur.execute("select version()")
    except:
        conn = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, db=mysql_db, charset='utf8')
    cur = conn.cursor()     
    try:
        if page == 0 or page == 1:
            page = 10
        else:
            page = page * 10
        try:
            if relax == 0:
                sqlopen = open("./bin/sql/best_score/regular.sql", 'r')
            elif relax == 1:
                sqlopen = open("./bin/sql/best_score/relax.sql", 'r')
            sql = (sqlopen.read()).format(userid, mode, page)
            cur.execute(sql)
            try:
                first_data = cur.fetchall()
                row_headers = [x[0] for x in cur.description]
                second_data = list(first_data)
                data = []
                for result in second_data:
                    data.append(dict(zip(row_headers, result)))
            except:
                data = []
            sqlopen.close()
        except Exception as e:
            data = []   
    
        json = {'status': '200', 'result': data}   

        return json
    except Exception as e:
        emoji = random.choice(cute_emoji)
        return {'code': '4000', 'message': emoji, 'error': e}

def get_user_most_play(userid, relax, page):
    try:
        cur = conn.cursor()    
        cur.execute("select version()")
    except:
        conn = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, db=mysql_db, charset='utf8')
    cur = conn.cursor()     
    try:
        if page == 0 or page == 1:
            page = 5
        else:
            page = page * 5
        try:
            if relax == 0:
                sqlopen = open("./bin/sql/most_play/regular.sql", 'r')
            elif relax == 1:
                sqlopen = open("./bin/sql/most_play/relax.sql", 'r')
            sql = (sqlopen.read()).format(userid, page)
            cur.execute(sql)
            try:
                first_data = cur.fetchall()
                row_headers = [x[0] for x in cur.description]
                second_data = list(first_data)
                data = []
                for result in second_data:
                    data.append(dict(zip(row_headers, result)))
            except:
                data = []
            sqlopen.close()
        except Exception as e:
            data = []   
    
        json = {'status': '200', 'result': data}   

        return json
    except Exception as e:
        emoji = random.choice(cute_emoji)
        return {'code': '4000', 'message': emoji, 'error': e}

def get_user_top_play(userid, relax, mode, page):
    try:
        cur = conn.cursor()    
        cur.execute("select version()")
    except:
        conn = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, db=mysql_db, charset='utf8')
    cur = conn.cursor()     
    try:
        if page == 0 or page == 1:
            page = 10
        else:
            page = page * 10
        try:
            if relax == 0:
                sqlopen = open("./bin/sql/top_play/regular.sql", 'r')
            elif relax == 1:
                sqlopen = open("./bin/sql/top_play/relax.sql", 'r')
            sql = (sqlopen.read()).format(userid, page, mode)
            cur.execute(sql)
            try:
                first_data = cur.fetchall()
                row_headers = [x[0] for x in cur.description]
                second_data = list(first_data)
                data = []
                for result in second_data:
                    data.append(dict(zip(row_headers, result)))
            except:
                data = []
            sqlopen.close()
        except Exception as e:
            data = []   
    
        json = {'status': '200', 'result': data}   

        return json
    except Exception as e:
        emoji = random.choice(cute_emoji)
        return {'code': '4000', 'message': emoji, 'error': e}

def get_user_recentactivity(userid, relax, mode, page):
    try:
        cur = conn.cursor()    
        cur.execute("select version()")
    except:
        conn = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, db=mysql_db, charset='utf8')
    cur = conn.cursor()     
    try:
        if page == 0 or page == 1:
            page = 5
        else:
            page = page * 5
        try:
            if relax == 0:
                sqlopen = open("./bin/sql/recent_activity/regular.sql", 'r')
            elif relax == 1:
                sqlopen = open("./bin/sql/recent_activity/relax.sql", 'r')
            sql = (sqlopen.read()).format(userid, mode, page)
            cur.execute(sql)
            try:
                first_data = cur.fetchall()
                row_headers = [x[0] for x in cur.description]
                second_data = list(first_data)
                data = []
                for result in second_data:
                    data.append(dict(zip(row_headers, result)))
            except:
                data = []
            sqlopen.close()
        except Exception as e:
            data = []   
    
        json = {'status': '200', 'result': data}   

        return json
    except Exception as e:
        emoji = random.choice(cute_emoji)
        return {'code': '4000', 'message': emoji, 'error': e}

def get_user_achievements(userid, mode, type):
    try:
        cur = conn.cursor()    
        cur.execute("select version()")
    except:
        conn = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, db=mysql_db, charset='utf8')
    cur = conn.cursor()     
    try:
        try:
            if type == 1:
                sqlopen = open("./bin/sql/achievements/all.sql", 'r')
            else:
                sqlopen = open("./bin/sql/achievements/noall.sql", 'r')

            sql = (sqlopen.read()).format(userid, mode)
            cur.execute(sql)
            try:
                first_data = cur.fetchall()
                row_headers = [x[0] for x in cur.description]
                second_data = list(first_data)
                data = []
                for result in second_data:
                    data.append(dict(zip(row_headers, result)))
            except:
                data = []
            sqlopen.close()
        except Exception as e:
            data = []   
    
        json = {'status': '200', 'result': data}   

        return json
    except Exception as e:
        emoji = random.choice(cute_emoji)
        return {'code': '4000', 'message': emoji, 'error': e}

def get_user_mail(userid):
    try:
        cur = conn.cursor()    
        cur.execute("select version()")
    except:
        conn = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, db=mysql_db, charset='utf8')
    cur = conn.cursor()  
    cur.execute(f"select email from Ainu.users where id={userid}")
    data = cur.fetchone()
    mail = data[0]
    return mail

def get_user_id(userid):
    try:
        cur = conn.cursor()    
        cur.execute("select version()")
    except:
        conn = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, db=mysql_db, charset='utf8')
    cur = conn.cursor()  
    cur.execute(f"select username from Ainu.users where id={userid}")
    data = cur.fetchone()
    mail = data[0]
    return mail

def get_user_country(userid):
    try:
        cur = conn.cursor()    
        cur.execute("select version()")
    except:
        conn = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, db=mysql_db, charset='utf8')
    cur = conn.cursor()  
    cur.execute(f"select country from Ainu.users_stats where id={userid}")
    data = cur.fetchone()
    mail = data[0]
    return mail

def send_ban_mail(user):
    try:
        cur = conn.cursor()    
        cur.execute("select version()")
    except:
        conn = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, db=mysql_db, charset='utf8')
    cur = conn.cursor()    
    try:
        body = """
        We have temporarily restricted your Debian account "{}" due to the suspicious activity on your account.
        If you attempt to create a new account, it will automatically switch to the same state.

        If you wish to repeal for your account restriction, please follow the procedure below.
        - Record your live play and reply to this email.
        - The recording must follow and include these steps: "start PC > reveal task manager > run osu! > reveal task manager > play osu!"

        If you follow these steps correctly and after we have confirmed that there are no problems in your live play, the restriction will be lifted.
        If you record your live play in Debian Server, you will additionally receive a verified badge. 

        multi-accounting is heavily against the rules. If you attempt to evade your restriction by creating or playing on another account, your future repeals may be denied. 

        This mail is processed automatically, and after we have confirmed the legitimacy of your account, the restriction will automatically be lifted from your account.

        Sincerely,
        Debian Support Team
            """
        userid = get_user_id(user)
        toEmail = get_user_mail(user)
        fromEmail = UserConfig['mailFromEmail']
        titleEmail = 'Debian! Account Restriction Notice'
        try:
            body = body.format(userid, userid)
            body = str(body)
        except Exception as e:
            return str(e)
        msg = "\r\n".join(["From: " + fromEmail, "To: " + toEmail, "Subject: " + titleEmail, "", body])
        try:
            mailcon = SMTP_SSL(UserConfig['mailHost'])
            mailcon.ehlo()
            mailcon.login(UserConfig["mailID"], UserConfig["mailPW"])
            mailcon.sendmail(fromEmail, toEmail, msg)
            mailcon.close()
            return True
        except Exception as e:
            return str(e)
    except Exception as e:
        return str(e)