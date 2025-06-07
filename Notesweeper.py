import os
import subprocess
import time
import keyboard as kb
import random

with open('Game.txt', 'w', encoding='utf-8') as f:
    f.write(r'''
 _   _       _                                               
| \ | |     | |                                              
|  \| | ___ | |_ ___  _____      _____  ___ _ __   ___ _ __  
| . ` |/ _ \| __/ _ \/ __\ \ /\ / / _ \/ _ \ '_ \ / _ \ '__| 
| |\  | (_) | ||  __/\__ \\ V  V /  __/  __/ |_) |  __/ |    
\_| \_/\___/ \__\___||___/ \_/\_/ \___|\___| .__/ \___|_|    
                                           | |               
                                           |_|               
''')
os.system('taskkill /f /im notepad.exe')
subprocess.Popen(['notepad.exe', r'Game.txt'])
time.sleep(1)
level = ['0']*100
reveal = [0]*81
cursor = 0
run = True
bomb_indices = random.sample(range(81), 10)
stime = 0

for index in bomb_indices:
    level[index] = "💣"

def count(index, grid):
    row = index // 9
    col = index % 9
    directions = [(-1, -1), (-1, 0), (-1, 1), 
                  (0, -1),          (0, 1), 
                  (1, -1), (1, 0), (1, 1)]
    
    total = 0
    for dr, dc in directions:
        new_row = row + dr
        new_col = col + dc
        if 0 <= new_row < 9 and 0 <= new_col < 9:
            new_index = new_row * 9 + new_col
            if grid[new_index] == "💣":
                total += 1
    
    return total

    
for i in range(81):
    if level[i]!="💣":
        level[i] = str(count(i, level))

def end():
    global run
    run = False
    time.sleep(.3)
    with open('Game.txt', 'w', encoding='utf-8') as f:
        f.write('You stepped on a mine!\n')
        f.write(str(round(time.time()-stime))+' Seconds')
        os.system('taskkill /f /im notepad.exe')
        subprocess.Popen(['notepad.exe', r'Game.txt'])

def win():
    global run
    run = False
    time.sleep(.3)
    with open('Game.txt', 'w', encoding='utf-8') as f:
        f.write('You won!\n')
        f.write(str(round(time.time()-stime))+' Seconds')
        os.system('taskkill /f /im notepad.exe')
        subprocess.Popen(['notepad.exe', r'Game.txt'])
        
def update():
    with open('Game.txt', 'w', encoding='utf-8') as f:
        for i in range(9):
            for j in range(9):
                if (i*9+j==cursor):
                    char1 = '['
                    char2 = ']'
                else:
                    char1 = ' '
                    char2 = ' '
                if reveal[i*9+j]==1:
                    if level[i*9+j]=='0':
                        f.write(char1+' '+char2)
                    else:
                        f.write(char1+str(level[i*9+j])+char2)
                elif reveal[i*9+j]==0:
                    f.write(char1+'■'+char2)
                elif reveal[i*9+j]==3:
                    f.write(char1+'#'+char2)
            f.write('\n')
    os.system('taskkill /f /im notepad.exe')
    subprocess.Popen(['notepad.exe', r'Game.txt'])
update()

def flood_fill(cursor, grid, reveal):
    if reveal[cursor] == 1:
        return
    reveal[cursor] = 1
    row = cursor // 9
    col = cursor % 9
    directions = [(-1, -1), (-1, 0), (-1, 1), 
                  (0, -1),          (0, 1), 
                  (1, -1), (1, 0), (1, 1)]
    for dr, dc in directions:
        new_row = row + dr
        new_col = col + dc
        if 0 <= new_row < 9 and 0 <= new_col < 9:
            new_cursor = new_row * 9 + new_col
            
            if grid[new_cursor] == "0":
                flood_fill(new_cursor, grid, reveal)  
            else:
                reveal[new_cursor] = 1 


def reveal_cell(cursor, grid, reveal):
    if grid[cursor] == "0":
        flood_fill(cursor, grid, reveal)
    else:
        reveal[cursor] = 1

while run:
    if kb.is_pressed('left'):
        if cursor > 0:
            cursor = cursor - 1
            update()
    if kb.is_pressed('right'):
        if cursor < 81:
            cursor = cursor + 1
            update()
    if kb.is_pressed('up'):
        if cursor-9 > -1:
            cursor = cursor -9
            update()
    if kb.is_pressed('down'):
        if cursor+9 < 82:
            cursor = cursor +9
            update()
    if kb.is_pressed('space'):
        if stime == 0:
            stime=time.time()
        if reveal[cursor]==0:
            reveal_cell(cursor, level, reveal)
        update()
        if level[cursor]=="💣":
            end()
    if kb.is_pressed('ctrl'):
        if reveal[cursor]==0:
            reveal[cursor]=3
        elif reveal[cursor]==3:
            reveal[cursor]=0
        update()
    if reveal.count(1) >= 71:
        win()
    time.sleep(.1)

