import random
import sys,os
#board = [[1,1,1,1],[1,1,1,1],[0,0,0,0],[1,1,1,1]]
board = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]

def print_board(board, score):
    os.system("cls")
    print(f"Score: {score}")
    for list in board:
        print(list)

def shifty(lis, check, score):
    init_lis = lis.copy()
    while(True):
        if 0 in lis:
            lis.pop(lis.index(0))
        else:
            break
    for x in range(len(lis)-1):
        try:
            if lis[x] == lis[x+1]:
                lis[x] *=2
                lis.pop(x+1)
                score += lis[x]
        except:
            break
    for x in range(4-len(lis)):
        lis.append(0)
    if init_lis != lis:
        check = 1
    return(lis, check, score)

def add_value(board):
    value = random.choice([2,4])
    empty = []
    for y in range(4):
        for x in range(4):
            if board[y][x] == 0:
                empty.append((x,y))
    if len(empty) == 0:
        sys.exit("you lose")
    x,y = random.choice(empty)
    
    b = board.copy()
    b[y][x] = value
    return b

def move_up(board,check, score):
    for column in range(4):
        temp = []
        for x in range(4):
            temp.append(board[x][column])
        temp,check, score = shifty(temp,check, score)
        for x in range(4):
            board[x][column] = temp[x]
    return board,check, score

def move_down(board,check, score):
    for column in range(4):
        temp = []
        for x in range(4):
            temp.append(board[x][column])
        temp = temp[::-1]
        temp,check, score = shifty(temp,check, score)
        temp = temp[::-1]
        for x in range(4):
            board[x][column] = temp[x]
    return board,check, score

def move_left(board,check, score):
    for row in range(4):
        temp = []
        for x in range(4):
            temp.append(board[row][x])
        temp,check, score = shifty(temp,check, score)
        for x in range(4):
            board[row][x] = temp[x]
    return board,check, score

def move_right(board,check, score):
    for row in range(4):
        temp = []
        for x in range(4):
            temp.append(board[row][x])
        temp = temp[::-1]
        temp,check, score = shifty(temp,check, score)
        temp = temp[::-1]
        for x in range(4):
            board[row][x] = temp[x]
    return board,check, score

#print_board(board)
b = add_value(board)
score = 0
while True:
    check = 0
    print_board(b,score)
    action = input("w,s,a,d\n").lower()
    if action == "w":
        b, check, score = move_up(b, check, score)
    elif action == "s":
        b, check, score = move_down(b, check, score)
    elif action == "a":
        b, check, score = move_left(b, check, score)
    elif action == "d":
        b, check, score = move_right(b, check, score)
    else:
        break
    if check == 1:
        b = add_value(board)

    print("\n")


