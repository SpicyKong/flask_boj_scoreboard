import sys
from collections import deque
"""
[core]
	repositoryformatversion = 0
	filemode = true
	bare = false
	logallrefupdates = true
[user]
	email = ssw30951@gmail.com
	name = SpicyKong
[remote "origin"]
	url = https://ssw30951%40gmail.com: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@github.com/SpicyKong/flask_login.git
	fetch = +refs/heads/*:refs/remotes/origin/*

"""
def bfs(s):
    list_visit = [0]*1001
    list_visit[s] = 1
    list_queue = deque([s])
    ret = []
    while list_queue:
        now = list_queue.popleft()
        ret.append(now)
        for new in list_node[now]:
            if list_visit[new]:
                continue
            list_visit[new] = 1
            list_queue.append(new)
    return ret

def dfs(s):
    list_visit = [0]*1001
    list_visit[s] = 1
    list_stack = [s]
    ret = [s]
    while list_stack:
        now = list_stack[-1]
        chk = 1
        for new in list_node[now]:
            if not list_visit[new]:
                chk=0
                list_visit[new] = 1
                list_stack.append(new)
                ret.append(new)
                break
        if chk:
            list_stack.pop()
    return ret
            
            
        
    

N, M, V = map(int, sys.stdin.readline().split())
list_node = [[] for _ in range(N+1)]
for _ in range(M):
    a, b = map(int, sys.stdin.readline().split())
    list_node[a].append(b)
    list_node[b].append(a)
for i in range(N):
    list_node[i+1].sort()
print(*dfs(V))
print(*bfs(V))