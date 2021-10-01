"""
할 거
로그인을 post로 요청하기

"""

from flask import Blueprint, render_template, make_response, request, current_app as app, redirect


from bs4 import BeautifulSoup
import requests, json

from main.models import User, Week_board, Problem
from main import db, socketio

from flask_socketio import emit

from sqlalchemy import and_

import jwt
from time import time, localtime
from datetime import datetime

from functools import wraps

bp = Blueprint('user', __name__, url_prefix='/user')

def safe_process(org_func):
    """500오류 페이지를 띄어주는 데코레이터용 함수
    
    인자:
        데코레이터를 붙힐 함수
    
    반환:
        오류가 날 경우: 
            http status 500 error
        정상 작동 시: 
            원본 함수
    """
    @wraps(org_func)
    def safe_func(*args, **kwargs):
        try:
            return org_func(*args, **kwargs)
        except:
            return make_response('아마도 서버 잘못일듯?', 500)
    return safe_func

def check_auth(org_func):
    """유효한 인증 여부를 확인해주는 데코레이터용 함수
    
    인자:
        데코레이터를 붙힐 함수
        
    반환:
        인증이 유효한 경우:
            원본함수
        그렇지 아니할 경우:
            http error 401
        
    """
    @wraps(org_func)
    def verify(*args, **kwargs):
        try:
            
            user_jwt = request.cookies.get('user_jwt')
            claim_set = jwt.decode(user_jwt, options={"verify_signature": False}, algorithms=['HS256'])
            print(claim_set)
            if claim_set['id'] != app.config['ADMIN']:
                return make_response('어드민 권한이 없는 사용자입니다.', 401)
            if claim_set['exp'] - time() < 0:
                return redirect('https://github.com/login/oauth/authorize?'+'client_id='+app.config['GITHUB_CLIENT'])
            
            jwt.decode(user_jwt, app.config['SECRET_KEY'], algorithms=['HS256'])
            print('ok')
            print(args)
            print(kwargs)
            return org_func(*args, **kwargs)
        except:
            print('wrong2')
            return make_response('어드민 권한이 없는 사용자이거나, 로그인을 해 주세요.')
    return verify

@bp.route('/<string:username>', methods=['POST'])
@check_auth
def create_user(username):
    """유저를 생성하는 함수
    
    인자:
        등록할 유저 이름
        
    반환:
        성공시:
            http status code: 200
        실패시:
            http status code: error
    
    """
    is_user = is_user_in_boj(username)
    if not is_user:
        return make_response('없는 사용자', 404)
    
    time_now = int(time())
    
    # 혹시 유저 생성하고 서버가 다운되었을 경우를 대비해
    
    if User.query.filter(User.username == username).first() is None:
        user = User(username, get_start(time_now))
        db.session.add(user)
        db.session.commit()
    else:
        user = User.query.filter(User.username == username).first()
    week = Week_board(user.user_id, get_week(time_now))
    # 당장은 쓰지 않을 예정
    #init_user_solved_problem(user.user_id)
    
    db.session.add(week)
    db.session.commit()
    
    update_solved_problem()
    #print(str(week))
    return make_response('정상 처리 됨', 200)

@bp.route('/test', methods=['GET'])
@check_auth
def test_cookie():
    return make_response('정상 처리 됨', 200)

@bp.route('/<string:username1>', methods=['PATCH'])
@check_auth
def update_user(username1):
    tteesstt = make_response('ok', 200)
    tteesstt.headers['Access-Control-Allow-Origin'] = '*'
    data = request.get_json()
    print(request.get_json())
    print(data)
    username2 = data['username2']
    
    user = User.query.filter(User.username==username1).first_or_404()
    user.username = username2
    db.session.add(user)
    db.session.commit()
    return tteesstt#make_response('정상 처리 됨', 200)

@bp.route('/<string:username>', methods=['DELETE'])
@check_auth
def delete_user(username):
    print(username)
    user = User.query.filter(User.username==username).first_or_404()
    print(user)
    db.session.delete(user)
    db.session.commit()
    return make_response('정상 처리 됨', 200)



@bp.route('/admin', methods=['GET'])
def admin_page():
    return render_template('admin.html')

@bp.route('/login', methods=['POST'])
def login():
    code = request.json.get('code', None)
    print(code)
    
    if not code:
        return make_response('로그인 이상함', 401)
        #https://github.com/login/oauth/authorize?client_id=fb0b9cd9b0766772bdfc
        #return redirect('https://github.com/login/oauth/authorize?'+'client_id='+app.config['GITHUB_CLIENT'])
    
    json_from_user = request.get_json()
    
    headers = {
        'Content-Type': 'application/json',
        'Accept' : 'application/vnd.github.v3+json'
    }
    data = {
        'client_id' : app.config['GITHUB_CLIENT'],
        'client_secret' : app.config['GITHUB_SECRET'],
    }
    message = 'ok'
    http_status = 200
    
    URL = 'https://github.com/login/oauth/access_token'
    data['code'] = code
    data = json.dumps(data)
    req = requests.post(URL, headers=headers, data=data).json()
    access_token = req['access_token'] if 'access_token' in req else ''
    
    headers['Authorization'] = 'token ' + access_token
    URL = 'https://api.github.com/user'
    req  = requests.get(URL, headers=headers).json()
    
    uid = req['id'] if 'id' in req else 0
    
    
    if uid == app.config['ADMIN']:
        claim_set = {
            'exp':(int(time())+1800),
            'id':app.config['ADMIN'],
        }
        user_jwt = jwt.encode(claim_set, app.config['SECRET_KEY'], algorithm='HS256')
    else:
        message = 'Sorry, It must be accessed by admin.'
        http_status = 401
        
    response = make_response(redirect('https://alrigothm.shop/user/admin'))
    if http_status == 200:
        response.set_cookie('user_jwt', user_jwt, httponly=True)
    response.headers['credentials']='include'
    
    return response


def is_user_in_boj(username):
    url = 'https://www.acmicpc.net/user/' + username
    response = requests.get(url)
    return 200 <= response.status_code < 300

def parsing_solved_num(response):
    return int(BeautifulSoup(response.text, 'html.parser').select_one('#u-solved').text)

def get_table_by_json():
    update_solved_problem()
    
    list_week = Week_board.query.filter(Week_board.week==get_week(int(time()))).order_by(Week_board.total.desc())
    dict_week_for_json = [
        {
            'rank':i+1,
            'username':User.query.get(week.user_id).username,
            'mon':week.mon,
            'tue':week.tue,
            'wed':week.wed,
            'thu':week.thu,
            'fri':week.fri,
            'sat':week.sat,
            'sun':week.sun,
            'total':week.total,
        } for i, week in enumerate(list_week) if User.query.get(week.user_id) is not None
    ]
    
    return json.dumps(dict_week_for_json, indent=4)

def init_user_solved_problem(user):
    html = requests.get('https://www.acmicpc.net/user/'+user.username)
    soup = BeautifulSoup(html, 'html.parser')
    for p_num in soup.select('.panel-body a'):
        new_p = Problem(user_id, int(p_num.text))
        db.session.add(new_p)
    db.session.commit()

    
def get_day(timestamp):
    """timestamp가 무슨 요일인지 구하는 함수
    """
    key = app.config['KEY_STAMP']
    return ((timestamp-key)//86400)%7
def get_week(timestamp):
    """timestamp가 몇 번째 주인지 구하는 함수
    """
    key = app.config['KEY_STAMP']
    return (timestamp-key)//(604800)

def get_start(timestamp):
    """이번주의 시작 timestamp를 구하는 함수
    
    """
    key = app.config['KEY_STAMP']
    return timestamp - (timestamp - key)%604800


# ===================================== 테스트를 위한 함수들 -==================================
def update_solved_problem():
    user_list = User.query.order_by(User.user_id)
    for user in user_list:
        top = ''
        done = False
        while not done:
            URL = "https://www.acmicpc.net/status?problem_id=&user_id="+user.username+"&language_id=-1&result_id=4"
            html = requests.get(URL + ('&top=' if top else '' + top)).text
            soup = BeautifulSoup(html, 'html.parser')
            list_solved = [(int(a.select_one('td').text), int(a.select_one('a.problem_title').text), int(a.select_one('a.real-time-update').attrs['data-timestamp'])) for a in soup.select('tbody tr')]
            for s_id, p_id, t in list_solved:
                top = str(s_id-1)
                if t <= user.timestamp:
                    done=True
                    break
                
                if Problem.query.filter(Problem.boj_id == p_id).first() is not None:
                    continue
                p = Problem(user.user_id, p_id)
                db.session.add(p)
                
                
                week = Week_board.query.filter(and_(Week_board.user_id==user.user_id, Week_board.week==get_week(t))).first()
                if week is None:
                    week = Week_board(user.user_id, get_week(t))
                week.update(get_day(t), 1)
                db.session.add(week)
                db.session.commit()
                
            if not list_solved:
                break

"""

@bp.route('update/<string:username>', methods=['GET'])
def user_commit(username):
    user = User.query.filter(User.username==username).first()
    week = Week_board.query.filter(and_(Week_board.user_id==user.user_id, Week_board.week==get_week(int(time())))).first()
    week.update(get_day(int(time())), 1)
    db.session.add(week)
    db.session.commit()
    return 'success'

#@bp.route('test_for_problem/<int:num>', methods=['GET'])
def test_for_problem(num):
    week = Week_board.query.filter(and_(Week_board.user_id==num, Week_board.week==get_week(int(time())))).first()
    week.update(get_day(int(time())), 1)
    db.session.add(week)
    db.session.commit()
    
    #return 'hello..'
"""