화면 띄울때마다 갱신 하지 말기

# 1. 대충 디자인

| 순위 | 유저명 | 월 | 화 | 수 | 목 | 금 | 토 | 일 | 이번주 푼 문제수 합 |
|-||||||||||
| 1 | SpicyKong | 1 |||||||1|

딱 이렇게만 할거다.
# 2. DB 설계
## 2.1. USER
| id | username | timestamp|
| - |||
|pk|boj 유저명| 마지막 제출의 timestamp |

## 2.2. WEEK_BOARD
| id | user | week | MON | TUE | THR | WES | FRI | SAT | SUN | TOTAL |
| - |||||||||||
| id | 외래키, 유저 id | 몇 주차 | 월 문제수 | 화 문제수 | 수 문제수 | 목 문제수 |금 문제수 | 토 문제수 | 일 문제수 | 이번주 문제수 |

## 2.3. PROBLEM
| id | user_id | p_id |
| - |||
|id|유저 id| 문제id(in BOJ) |
# 3. URL 설계

## 3.1. ```/```
| url | 방식 | 반환 | 설명 |
|-||||
|``` / ```| ```GET``` | ```HTML``` | 스코어 보드 현황을 띄워 준다. |
|```/admin```| ```GET``` | ```HTML``` | 로그인 시 유저 목록을 수정 할 수 있는 어드민 페이지 (깃허브로 로그인 시키자)|
|``` /login ```| ```GET``` | ```HTML``` | oauth 로그인을 위한 리다이렉트를 해준다. |
|``` /getcode ```| ```GET``` | ```HTML``` | oauth에서 리다이렉트 해서 오면 로그인 시도를 해준다. |

## 3.2. ```/user```
| url | 방식 | 반환 | 설명 |
|-||||
|```/user```| ```POST``` | ```JSON``` |  |
|```/user```| ```PATCH``` | ```JSON``` |  |
|```/user```| ```DELETE``` | ```JSON``` |  |


# 4. To do
## 4.0. db의 두 테이블 모두 crud 설계
```create_user(username)```: username에 해당하는 유저를 추가  
```update_user(username1, username2)```: user1의 이름을 user2로 바꿈  
```delete_user(username)```: user 삭제
## 4.1. 어드민 페이지 관련
### 4.1.1. 로그인
1. Oauth로 리다이렉트 페이지 하나 만들기 
2. oauth코드값 받는 페이지 하나 만들기
3. 2번의 페이지에서 로그인 처리해주기  

### 4.1.2. 어드민 페이지
1. 유저를 추가할 수 있는 폼
2. 유저명을 수정할 수 있는 폼
3. 유저를 삭제할 수 있는 폼


## 4.2. 크롤링 관련
```is_user(username)```: 해당 유저가 존재하는지 확인(참/거짓)  
```get_num_problem(username)```: 해당 유저의 해결한 문제수를 반환

## 4.3. 요청이 왔을때 소켓으로 브로드 캐스팅 해서 정보 뿌리기
```board_update()```: 모든 유저의 문제 수를 조회해 반영함  
```board_reset()```: 새로운 week를 만들고 0으로 초기화 해둠
## 4.4. 템플릿 작성
디자인은 1번을 참고하며 좌우에 버튼이 하나씩 있음.
## 4.5. css, javascript로 꾸미기
사이트는 깔끔하게 인덱스 페이지만 존재하며, 좌, 우 버튼 활성화 비활성화를 통해 주차마다 해결한 문제 수를 볼 수 있음.   

구현하면 좋을것:
1. 좌 우 버튼 눌렀을때 애니메이션으로 넘어가기
2. 순위 변동시 스무스한 애니메이션으로 엎치락 뒤치락 하기
3. 해결한 문제가 없을땐 회색의 ``` -```로 표시, 푼 문제가 있을 경우 초록색 ```+1``` 이런식으로 표시

```
1. get_problem_num(유저명): 유저명으로 백준 사이트 크롤링 해 푼 문제수 가져오는 함수
2. is_user(유저명): 해당 유저가 존재하는지 true/false
3. add_user(유저명)
4. delete_user(유저명)
5. update_user(기존 유저명, 새로운 유저명)
6. reset_table(): 모든 유저 초기화
```
## 4.1. 
참고 사이트: https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FbblUjX%2Fbtq4p3fMgcJ%2FJMahzKNOxPNzShoQtAvsM1%2Fimg.png