from flask_cors import CORS
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from sqlalchemy import create_engine
import json
from flask_jsonpify import jsonify
from flask_mysqldb import MySQL
from bin.config import UserConfig
from bin.functions import *
import pymysql
import random

app = Flask('Cynthia')

app.config['MYSQL_HOST'] = UserConfig["MysqlHost"]
app.config['MYSQL_USER'] = UserConfig["MysqlUser"]
app.config['MYSQL_PASSWORD'] = UserConfig["MysqlPassword"]
app.config['MYSQL_DB'] = UserConfig["MysqlDb"]
host = UserConfig["host"]
port = UserConfig["port"]
debugmode = UserConfig["debug"]

mysql_host = UserConfig["MysqlHost"]
mysql_user = UserConfig["MysqlUser"]
mysql_password = UserConfig["MysqlPassword"]
mysql_db = UserConfig["MysqlDb"]
mysql_db2 = UserConfig["MysqlDb2"]

api = Api(app)
cute_200 = [ '200', '200', '200', '200', '200', '200', '2000000000000000000000000']
cute_ment = [ 'Do You Know Nerina?', 'Hmm... im so tired now....', 'Nerina is coding Noob', 'do you know debian?', 'how are you here??????', '' ]
cute_emoji = [ 'Σ(￣□￣;)', 'へ(￣∇￣へ)', '(ㅇ︿ㅇ)', '๑°⌓°๑', '٩(๑`^´๑)۶', '(ง •̀_•́)ง', "٩( 'ω' )و", '(๑╹∀╹๑)', '(╹౪╹*๑)', '٩(๑>∀<๑)۶', '(๑・‿・๑)', '✿˘◡˘✿', '(❀╹◡╹)', 'ʅ（´◔౪◔）ʃ'
 ]
try:
    conn = pymysql.connect(host=mysql_host, user=mysql_user, password=mysql_password, db=mysql_db, charset='utf8')
except:
    print('wtf')
    exit()
cur = conn.cursor()

class mainclass(Resource):
    def get(self):
        json = {"status": {"code": random.choice(cute_200),"message": f'{random.choice(cute_ment)} {random.choice(cute_emoji)}'}}
        return json

class anticheatv1(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        emoji = random.choice(cute_emoji)
        parser.add_argument('r', required=True, type=str, help=emoji)
        parser.add_argument('id', required=True, type=int, help=emoji)
        parser.add_argument('relax', required=True, type=int, help=emoji)
        args = parser.parse_args()
        replay = args['r']
        replayid = args['id']
        relax = args['relax']

        replaydir = replaydownload(relax, replayid)

        result = chkreplay(replaydir, replayid)

        return result

class Leaderboard(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            emoji = random.choice(cute_emoji)
            parser.add_argument('m', required=True, type=int, help=emoji)
            parser.add_argument('r', required=True, type=int, help=emoji)
            parser.add_argument('p', required=True, type=int, help=emoji)
            parser.add_argument('type', required=True, type=int, help=emoji)
            args = parser.parse_args()
            mode = args['m']
            page = args['p']
            relax = args['r']
            type = args['type']

            data = get_leaderboard(mode, page, relax, type)

            return data
        except Exception as e:
            emoji = random.choice(cute_emoji)
            return {'status': '400','message': emoji}

class Leaderboard2(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            emoji = random.choice(cute_emoji)
            parser.add_argument('m', required=True, type=int, help=emoji)
            parser.add_argument('r', required=True, type=int, help=emoji)
            parser.add_argument('offset', required=True, type=int, help=emoji)
            parser.add_argument('type', required=True, type=int, help=emoji)
            args = parser.parse_args()
            mode = args['m']
            page = args['offset']
            relax = args['r']
            type = args['type']

            data = get_leaderboard2(mode, page, relax, type)

            return data
        except Exception as e:
            emoji = random.choice(cute_emoji)
            return {'status': '400','message': emoji}

class TopPlay(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            emoji = random.choice(cute_emoji)
            parser.add_argument('m', required=True, type=int, help=emoji)
            parser.add_argument('rx', required=True, type=int, help=emoji)
            parser.add_argument('period', required=True, type=str, help=emoji)
            args = parser.parse_args()
            mode = args['m']
            relax = args['rx']
            time = args['period']

            data = get_topplay(mode, relax, time)

            return data
        except Exception as e:
            emoji = random.choice(cute_emoji)
            return {'status': '400','message': emoji}        

class SearchDebianBeatmap(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            emoji = random.choice(cute_emoji)
            parser.add_argument('offset', required=True, type=int, help=emoji)
            parser.add_argument('amount', required=True, type=int, help=emoji)
            parser.add_argument('mode', required=True, type=int, help=emoji)
            parser.add_argument('status', required=True, type=int, help=emoji)
            parser.add_argument('query', required=False, type=str, help=emoji)
            parser.add_argument('category', required=False, type=int, help=emoji)
            parser.add_argument('type', required=False, type=int, help=emoji)
            args = parser.parse_args() 

            offset = args['offset']           
            amount = args['amount']           
            mode = args['mode']           
            status = args['status']         
            query = args['query']   
            category = args['category']   
            type = args['type']   

            data = get_debianranks(offset, amount, mode, status, query, category, type)

            return data
        except Exception as e:
            emoji = random.choice(cute_emoji)
            return {'status': '400','message': emoji}       

class BeatmapData(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            emoji = random.choice(cute_emoji)
            parser.add_argument('bid', required=False, type=int, help=emoji)
            parser.add_argument('setid', required=False, type=int, help=emoji)
            parser.add_argument('name', required=False, type=str, help=emoji)
            parser.add_argument('md5', required=False, type=str, help=emoji)
            args = parser.parse_args()

            b_id = args['bid']           
            b_setid = args['setid']           
            b_name = args['name']           
            b_md5 = args['md5']

            if b_id is not None:
                type = 0
            if b_setid is not None:
                type = 1
            if b_name is not None:
                type = 2
            if b_md5 is not None:
                type = 3
            if b_setid is None:
                b_setid = 0
            if b_name is None:
                b_name = '0'
            if b_md5 is None:
                b_md5 = '0'

            data = get_beatmap(type, b_id, b_setid, b_name, b_md5)

            return data

        except Exception as e:
            emoji = random.choice(cute_emoji)
            return {'status': '400','message': emoji}

class BeatmapDataMd5(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            emoji = random.choice(cute_emoji)
            parser.add_argument('m', required=False, type=str, help=emoji)
            args = parser.parse_args()

            b_md5 = args['m']

            print(b_md5)
            data = get_beatmap(3, 0, 0, '', b_md5)

            return data

        except Exception as e:
            emoji = random.choice(cute_emoji)
            return {'status': '400','message': emoji}
            
class ScoreBoardPage(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            emoji = random.choice(cute_emoji)
            parser.add_argument('id', required=True, type=int, help=emoji)
            parser.add_argument('relax', required=True, type=int, help=emoji)
            parser.add_argument('mode', required=True, type=int, help=emoji)
            args = parser.parse_args()
            id = args['id']
            relax = args['relax']
            mode = args['mode']

            data = get_beatmap_score_data(id, relax, mode)
            
            return data
        except Exception as e:
            emoji = random.choice(cute_emoji)
            return {'status': '400','message': emoji, 'error': e}  

class ScoreBoardPageB(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            emoji = random.choice(cute_emoji)
            parser.add_argument('id', required=True, type=int, help=emoji)
            args = parser.parse_args()
            id = args['id']

            data = get_beatmap_score_data_beatmap(id)
            
            return data
        except Exception as e:
            emoji = random.choice(cute_emoji)
            return {'status': '400','message': emoji, 'error': e}  

class ScoreBoardPageS(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            emoji = random.choice(cute_emoji)
            parser.add_argument('id', required=True, type=int, help=emoji)
            parser.add_argument('relax', required=True, type=int, help=emoji)
            parser.add_argument('mode', required=True, type=int, help=emoji)
            args = parser.parse_args()
            id = args['id']
            relax = args['relax']
            mode = args['mode']

            data = get_beatmap_score_data_score(id, relax, mode)
            
            return data
        except Exception as e:
            emoji = random.choice(cute_emoji)
            return {'status': '400','message': emoji, 'error': e}  

class BanchoGayBar(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            emoji = random.choice(cute_emoji)
            parser.add_argument('u', required=True, type=str, help=emoji)
            args = parser.parse_args()
            username = args['u']

            data = get_bancho_user_gay(username)

            return data
        except:
            emoji = random.choice(cute_emoji)
            return {'status': '404040400404', 'message': emoji}

class PPGraph(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            emoji = random.choice(cute_emoji)
            parser.add_argument('u', required=True, type=int, help=emoji)
            parser.add_argument('r', required=True, type=int, help=emoji)
            parser.add_argument('m', required=True, type=int, help=emoji)
            parser.add_argument('t', required=False, type=int, help=emoji)
            args = parser.parse_args()
            userid = args['u']
            relax = args['r']
            mode = args['m']
            types = args['t']

            if type(types) == None:
                types = 0

            data = get_user_ppgraph(userid, relax, mode, types)

            return data

        except:
            emoji = random.choice(cute_emoji)
            return {'status': '404040400404', 'message': emoji}

class Userdata(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            emoji = random.choice(cute_emoji)
            parser.add_argument('u', required=True, type=int, help=emoji)
            parser.add_argument('r', required=True, type=int, help=emoji)
            parser.add_argument('m', required=True, type=int, help=emoji)
            args = parser.parse_args()
            userid = args['u']
            relax = args['r']
            mode = args['m']

            data = get_user_data(userid, relax, mode)

            return data

        except:
            emoji = random.choice(cute_emoji)
            return {'status': '404040400404', 'message': emoji}

class RecordingUserScore(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            emoji = random.choice(cute_emoji)
            parser.add_argument('id', required=True, type=int, help=emoji)
            parser.add_argument('r', required=True, type=int, help=emoji)
            args = parser.parse_args()    
            id = args['id']
            relax = args['r']

            data = record_userscore_data(id, relax)
            
            return data
        except Exception as e:
            emoji = random.choice(cute_emoji)
            return {'status': '400','message': emoji, 'error': e}

class test_mode_rank_(Resource):
    def get(self):
        try:
            data = get_mode_user_rank()
            
            return data
        except Exception as e:
            emoji = random.choice(cute_emoji)
            return {'status': '400','message': emoji, 'error': e}
            
class current_hosts(Resource):
    def get(self):
        json = {'osu.ppy.sh': '49.165.136.97',
        'c.ppy.sh': '49.165.136.97',
        'c1.ppy.sh': '49.165.136.97',
        'c2.ppy.sh': '49.165.136.97',
        'c3.ppy.sh': '49.165.136.97',
        'c4.ppy.sh': '49.165.136.97',
        'c5.ppy.sh': '49.165.136.97',
        'c6.ppy.sh': '49.165.136.97',
        'ce.ppy.sh': '49.165.136.97',
        'a.ppy.sh': '49.165.136.97',
        'i.ppy.sh': '49.165.136.97'
        }
        return json

class current_ip(Resource):
    def get(self):
        json = {'ip': '49.165.136.97'}
        return json

class User_RecentPlay(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            emoji = random.choice(cute_emoji)
            parser.add_argument('u', required=True, type=int, help=emoji)
            parser.add_argument('r', required=True, type=int, help=emoji)
            parser.add_argument('m', required=True, type=int, help=emoji)
            parser.add_argument('p', required=True, type=int, help=emoji)
            args = parser.parse_args()
            userid = args['u']
            relax = args['r']
            mode = args['m']
            page = args['p']

            data = get_user_recent_play(userid, relax, mode, page)

            return data

        except:
            emoji = random.choice(cute_emoji)
            return {'status': '404040400404', 'message': emoji}

class User_BestPlay(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            emoji = random.choice(cute_emoji)
            parser.add_argument('u', required=True, type=int, help=emoji)
            parser.add_argument('r', required=True, type=int, help=emoji)
            parser.add_argument('m', required=True, type=int, help=emoji)
            parser.add_argument('p', required=True, type=int, help=emoji)
            args = parser.parse_args()
            userid = args['u']
            relax = args['r']
            mode = args['m']
            page = args['p']

            data = get_user_best_play(userid, relax, mode, page)

            return data

        except:
            emoji = random.choice(cute_emoji)
            return {'status': '404040400404', 'message': emoji}

class User_MostPlay(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            emoji = random.choice(cute_emoji)
            parser.add_argument('u', required=True, type=int, help=emoji)
            parser.add_argument('r', required=True, type=int, help=emoji)
            parser.add_argument('p', required=True, type=int, help=emoji)
            args = parser.parse_args()
            userid = args['u']
            relax = args['r']
            page = args['p']

            data = get_user_most_play(userid, relax, page)

            return data

        except:
            emoji = random.choice(cute_emoji)
            return {'status': '404040400404', 'message': emoji}
            
class User_TopPlay(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            emoji = random.choice(cute_emoji)
            parser.add_argument('u', required=True, type=int, help=emoji)
            parser.add_argument('r', required=True, type=int, help=emoji)
            parser.add_argument('m', required=True, type=int, help=emoji)
            parser.add_argument('p', required=True, type=int, help=emoji)
            args = parser.parse_args()
            userid = args['u']
            relax = args['r']
            mode = args['m']
            page = args['p']

            data = get_user_top_play(userid, relax, mode, page)

            return data

        except:
            emoji = random.choice(cute_emoji)
            return {'status': '404040400404', 'message': emoji}

class User_RecentActivity(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            emoji = random.choice(cute_emoji)
            parser.add_argument('u', required=True, type=int, help=emoji)
            parser.add_argument('r', required=True, type=int, help=emoji)
            parser.add_argument('m', required=True, type=int, help=emoji)
            parser.add_argument('p', required=True, type=int, help=emoji)
            args = parser.parse_args()
            userid = args['u']
            relax = args['r']
            mode = args['m']
            page = args['p']

            data = get_user_recentactivity(userid, relax, mode, page)

            return data

        except:
            emoji = random.choice(cute_emoji)
            return {'status': '404040400404', 'message': emoji}

class User_Achievements(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            emoji = random.choice(cute_emoji)
            parser.add_argument('u', required=True, type=int, help=emoji)
            parser.add_argument('m', required=True, type=int, help=emoji)
            parser.add_argument('a', required=True, type=int, help=emoji)
            args = parser.parse_args()
            userid = args['u']
            mode = args['m']
            type = args['a']

            data = get_user_achievements(userid, mode, type)

            return data

        except:
            emoji = random.choice(cute_emoji)
            return {'status': '404040400404', 'message': emoji}

class SendBanMail(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            emoji = random.choice(cute_emoji)
            parser.add_argument('u', required=True, type=int, help=emoji)
            parser.add_argument('k', required=True, type=str, help=emoji)
            args = parser.parse_args()
            user = args['u']
            key = args['k']
            
            if key != "nerina!241@909*":
                return "Authorization Faild"
            else:
                a = send_ban_mail(user)
                if type(a) == bool:
                    return "mail send sucessfully"
                else:
                    return a
        except:
            return{'status': '404040400404', 'message': emoji}

api.add_resource(mainclass, '/')
api.add_resource(Leaderboard, '/leaderboard')
api.add_resource(Leaderboard2, '/leaderboard2')
api.add_resource(anticheatv1, '/anticheat/v1')
api.add_resource(TopPlay, '/plays')
api.add_resource(BeatmapData, '/get/beatmap')
api.add_resource(BeatmapDataMd5, '/get/beatmap/md5')
api.add_resource(SearchDebianBeatmap, '/beatmap/debian')
api.add_resource(RecordingUserScore, '/score/record')
api.add_resource(test_mode_rank_, '/user/test')
api.add_resource(current_hosts, '/ip/hosts')
api.add_resource(current_ip, '/ip')
api.add_resource(ScoreBoardPageB, '/scoreboard/b')
api.add_resource(ScoreBoardPage, '/scoreboard/all')
api.add_resource(ScoreBoardPageS, '/scoreboard/s')
api.add_resource(BanchoGayBar, '/get/bancho/username')
api.add_resource(PPGraph, '/user/graph')
api.add_resource(Userdata, '/user/get')
api.add_resource(User_RecentPlay, '/user/recent')
api.add_resource(User_BestPlay, '/user/best')
api.add_resource(User_MostPlay, '/user/most')
api.add_resource(User_TopPlay, '/user/top')
api.add_resource(User_RecentActivity, '/user/recent_activity')
api.add_resource(User_Achievements, '/user/achievements')
api.add_resource(SendBanMail, '/send/ban/mail')

if __name__ == "__main__":
    app.run(port=port, host='0.0.0.0', debug=False)