#https://www.acmicpc.net/status?problem_id=&user_id=ssw3095&language_id=-1&result_id=4

from bs4 import BeautifulSoup
import requests



"""
title="2021-03-18 00:14:19" data-timestamp="1615994059"
"""

def read_html():
    username="ssw3095"
    URL = "https://www.acmicpc.net/status?problem_id=&user_id="+username+"&language_id=-1&result_id=4"
    html = requests.get(URL)
    with open("html.txt", "w") as f:
        f.write(html.text)
def get_html():
    html = ''
    with open("html.txt", "r") as f:
        html = f.read()
    return html

# 저장된 타임 스탬프의 값보다 높은 값이 있다면, 푼 문제로 추가
# 같은 문제에 대해 맞았습니다가 뜨는 것을 어떻게 해결할지가 문제다.
"""
1. 초기에 유저 생성시 푼 문제 목록도 받아온다.
2. 해결한 문제 수 갱신시 푼 적이 있는 문제인지 검사한다.
3-1. 풀었던 문제라면 카운팅 하지 않는다
3-2. 새로 푼 문제라면 카운팅 한다.

이렇게 되면 문제를 저장하는 db를 하나 더 만들어야 한다

"""
def get_pnum(username):
    key_time = 1615994059
    
    html = get_html()
    soup = BeautifulSoup(html, 'html.parser')
    
    list_success = soup.select('a.real-time-update')
    num = 0
    while True:
        pass
    print([a.attrs['data-timestamp'] for a in list_success])

    
