inf = float('inf')
import time
from queue import PriorityQueue
import random

graph=[]
value=inf
path=[]

class Node:
    def __init__(self, level):
        self.level = level
        self.path = []  # 현재 노드에서 가지고있는 path
        self.bound = 0  # 현재 경로에 대한 bound

    def __lt__(self, other):
        return self.bound < other.bound

def calculateValue(path, graph):  # 인자로 받은 path에 대한 value 계산
    value = 0
    for i, vertex in enumerate(path):
        value += graph[i][vertex - 1]
    return value


def calculateBound(path, graph):
    path_length = len(path)
    graph_length = len(graph)
    row_candidate = list(range(len(graph)))
    value = calculateValue(path, graph)  # 현재까지 경로의 value 구함
    for vertex in path:
        if vertex - 1 in row_candidate:
            row_candidate.remove(vertex - 1)
    for i in range(path_length, graph_length):  # path 길이 3이면 3부터
        min_value = inf
        for vertex in row_candidate:
            if graph[i][vertex] < min_value:
                min_value = graph[i][vertex]
        value += min_value
    return value

def assignment(graph):
    global value  # 최소의 값 찾기
    global path
    queue = PriorityQueue()
    root = Node(0)  # 루트노드 생성
    root.bound = calculateBound(root.path, graph)  # 바운드값 계산
    queue.put((root.bound, root))  # bound값 기준을 우선순위큐 삽입
    while not queue.empty():
        e = queue.get()[1]
        if e.bound < value:  # promising 하다면
            row_candidate = list(range(len(graph)))
            for i in e.path:
                if i - 1 in row_candidate:
                    row_candidate.remove(i - 1)
            for i in range(len(graph)):  # 자식노드 만들기
                if i not in row_candidate:
                    continue
                p = Node(e.level + 1)
                p.path = e.path[:]
                p.path.append(i + 1)
                if p.level == len(graph) - 1:  # 리프노드인경우
                    check_p = list(range(len(graph)))
                    for x in p.path:
                        if x - 1 in check_p:
                            check_p.remove(x - 1)
                    p.path.append(check_p[0] + 1)
                    if calculateValue(p.path, graph) < value:  # 최소비용보다 작다면
                        print(f'최소비용 바뀌는 경우 : {value} -> {calculateValue(p.path, graph)} , {p.path}')
                        value = calculateValue(p.path, graph)
                        path = p.path[:]
                else:  # 리프노드가 아니면
                    p.bound = calculateBound(p.path, graph)
                    if p.bound < value:  # 최소 비용보다 bound가 작으면 우선순위큐에 삽입
                        queue.put((p.bound, p))
                    else:
                        print(f'{p.path} 의 바운드({p.bound})가 최소비용({value})보다 크므로 pruning')
        else:
            print(f'{e.path} 의 바운드({e.bound})가 최소비용({value})보다 크므로 pruning')

def start_seating(set):
    global graph,value,path
    grp=[]
    f = open('preference_data.txt', 'r')
    while(True):
        line = f.readline().strip()
        if not line: break
        l=[]
        for i in range(len(line)):
            if i%2==0:
                l.append(int(line[i]))
        grp.append(l)
    graph=grp[:]

    n = len(graph)

    set_std=[]
    set_seat=[]
    std_plus=[]
    seat_plus=[]

    for i in set:
        set_std.append(i[0])
        set_seat.append(i[1])

    p=0
    for i in range(n):
        if i in set_std:
            p+=1
            continue
        std_plus.append(p)

    p=0
    for i in range(n):
        if i in set_seat:
            p+=1
            continue
        seat_plus.append(p)


    set_seat.sort()
    set_seat.reverse()
    set_std.sort()
    set_std.reverse()

    for i in set_std:
        del(graph[i])

    for i in set_seat:
        for j in range(len(graph)):
            del(graph[j][i])

    n = len(graph)
    value = inf  # 최소의 value를 찾기위한 초기화
    path = []  # 최적의 경로
    starttime = time.time()
    rand_std=[]
    rand_seat=[]
    for i in range(n):
        rand_std.append([i,random.random()])
        rand_seat.append([i,random.random()])
    rand_std.sort(key = lambda x: x[1])
    rand_seat.sort(key = lambda x: x[1])

    std_array=[]
    seat_array=[]
    result_array=[0]*n
    for i in rand_std:
        std_array.append(i[0])
    for i in rand_seat:
        seat_array.append(i[0])

    std=[]
    seat=[]
    std.append(std_array[:int(len(std_array)/2)])
    std.append(std_array[int(len(std_array)/2):])
    seat.append(seat_array[:int(len(seat_array)/2)])
    seat.append(seat_array[int(len(seat_array)/2):])

    path_array=[]
    for i in range(2):
        path=[]
        value=inf
        grp=[]
        for s in range(len(graph)):
            if s in std[i]:
                line=[]
                for t in range(len(graph[s])):
                    if t in seat[i]:
                        line.append(graph[s][t])
                grp.append(line)
        assignment(grp)
        for j in range(len(path)):
            path[j]-=1
        path_tmp=path[:]
        path_array.append((path_tmp))

    for i in range(2):
        for j in range(len(path_array[i])):
            result_array[std[i][j]]=seat[i][path_array[i][j]]

    result=[0]*(n+len(set))

    for student_num,seat_num in enumerate(result_array):
        result[student_num+std_plus[student_num]]=seat_num+seat_plus[seat_num]

    for i in set:
        result[i[0]]=i[1]

    endtime = time.time()
    print(f'걸린시간 : {endtime - starttime}')
    return result