import os
import getpass
import json
import msvcrt
import sys


# game_map = [[5, 5, 4, 4, 4, 4],
#             [4, 4, 4, 5, 1, 4],
#             [4, 5, 5, 3, 0, 4],
#             [4, 5, 5, 2, 5, 4],
#             [4, 4, 5, 5, 4, 4],
#             [5, 4, 4, 4, 4, 5]
#             ]


# 0 箱子到达目的地
# 1 箱子的目的地
# 2 箱子
# 3 工人
# 4 墙
# 5 空白
# 6 工人到达箱子的目的地
def print_map(game_map):
    # 遍历地图中的每一行
    for row in game_map:
        # 遍历当前行中的每一个数字
        for num in row:
            # 根据数字打印不同的符号，下同
            if num == 0:
                print("★", end="")
            elif num == 1:
                print("☆", end="")
            elif num == 2:
                print("□", end="")
            elif num == 3:
                print("♀", end="")
            elif num == 4:
                print("■", end="")
            elif num == 5:
                print("  ", end="")
            elif num == 6:
                print("◎", end="")
        print("\n", end="")  # 打印完一行后需要换行


def move(direction, game_map, worker_loc):
    # 获取工人初始位置横坐标和纵坐标
    row = worker_loc[0]
    col = worker_loc[1]

    # 根据移动方向设置工人和箱子在横向和纵向上的位移量
    if direction == "up":
        step_x = -1  # 行数减1，使工人向上移动一格
        step_y = 0  # 列数不变
        step_box_x = -2  # 行数减2，箱子向上移动2格
        step_box_y = 0  # 列数不变
    elif direction == "down":
        step_x = 1  # 行数加1，使工人向下移动一格
        step_y = 0  # 列数不变
        step_box_x = 2  # 行数加2，箱子向下移动2格
        step_box_y = 0  # 列数不变
    elif direction == "left":
        step_x = 0  # 行数不变
        step_y = -1  # 列数减1，使工人向左移动一格
        step_box_x = 0  # 行数不变
        step_box_y = -2  # 列数减2，使箱子向左移动两格
    elif direction == "right":
        step_x = 0  # 行数不变
        step_y = 1  # 列数加1，使工人向右移动一格
        step_box_x = 0  # 行数不变
        step_box_y = 2  # 列数加2，使箱子向右移动两格
    # print("step_x = %s step_y = %s" % (step_x,step_y))
    # 判断目标位置是否为终点，如果是，将目标位置修改为箱子在终点上或者空终点，然后更新工人位置
    if game_map[row + step_x][col + step_y] == 5:
        # 如果目标位置为5，即终点，则将目标位置修改为3
        game_map[row + step_x][col + step_y] = 3
        if game_map[row][col] == 6:
            # 如果当前位置为6，即箱子在终点上，则将当前位置修改为1（表示终点），否则将其修改为5
            game_map[row][col] = 1
        else:
            game_map[row][col] = 5
        # 更新工人（玩家）的位置为目标位置
        worker_loc[0] = row + step_x
        worker_loc[1] = col + step_y

    # 如果目标位置为终点，将终点上的箱子移出，否则将箱子移到终点
    elif game_map[row + step_x][col + step_y] == 1:
        # 如果目标位置为1，即目标位置为终点，则将目标位置修改为6（箱子放到了终点），并更新工人位置
        game_map[row + step_x][col + step_y] = 6
        if game_map[row][col] == 6:
            game_map[row][col] = 1
        else:
            game_map[row][col] = 5
        # 更新工人（玩家）的位置为目标位置
        worker_loc[0] = row + step_x
        worker_loc[1] = col + step_y

    # 如果目标位置为障碍物或空位置
    elif game_map[row + step_x][col + step_y] == 2 or game_map[row + step_x][col + step_y] == 0:
        # 判断箱子移动后的位置是否为终点，如果是，将目标位置修改为箱子在终点上或者空终点，然后更新工人和箱子位置，保证移动后状态正确
        if game_map[row + step_box_x][col + step_box_y] == 5:
            # 如果该位置为5，即目标箱子移动到了终点，则将目标位置修改为3或6（与当前位置相同），并更新工人和箱子位置，保证移动后状态正确
            if game_map[row + step_x][col + step_y] == 2:
                game_map[row + step_x][col + step_y] = 3
            if game_map[row + step_x][col + step_y] == 0:
                game_map[row + step_x][col + step_y] = 6
            game_map[row + step_box_x][col + step_box_y] = 2
            if game_map[row][col] == 6:
                game_map[row][col] = 1
            else:
                game_map[row][col] = 5
            worker_loc[0] = row + step_x
            worker_loc[1] = col + step_y

        # 如果该位置为1，即终点上有箱子，则将该位置修改为0，即推出终点，并更新工人和箱子位置，保证移动后状态正确
        if game_map[row + step_box_x][col + step_box_y] == 1:
            if game_map[row + step_x][col + step_y] == 2:
                game_map[row + step_x][col + step_y] = 3
            if game_map[row + step_x][col + step_y] == 0:
                game_map[row + step_x][col + step_y] = 6
            game_map[row + step_box_x][col + step_box_y] = 0
            if game_map[row][col] == 6:
                game_map[row][col] = 1
            else:
                game_map[row][col] = 5
            worker_loc[0] = row + step_x
            worker_loc[1] = col + step_y


def is_ok(game_map, box_locs):
    # 判断游戏是否通关
    for box_loc in box_locs:
        if game_map[box_loc[0]][box_loc[1]] != 0:
            return
    # 所有箱子位置上都有目标点，通关成功
    print("success")


def read_cfg():
    # 读取关卡信息
    with open('box.json', "r", encoding='utf-8') as f:
        cfg = f.read()
        d = json.loads(cfg)
        f.close()
    return d


'''if __name__ == '__main__':
    # 选择关卡
    level = input("输入关卡（1-2）：")
    d = read_cfg()
    game_map = d[level]["game_map"]
    worker_loc = d[level]["worker_loc"]
    box_locs = d[level]["box_locs"]
    print_map(game_map)
    while True:
        cmd = getpass.getpass(prompt="")  # 密码输入方式，避免显示在屏幕上
        # cmd = msvcrt.getch()
        # print(cmd)
        # cmd = input()
        if cmd == "8":
            move("up", game_map, worker_loc)
            os.system("cls")
            print_map(game_map)
        elif cmd == "2":
            move("down", game_map, worker_loc)
            os.system("cls")
            print_map(game_map)
        elif cmd == "4":
            move("left", game_map, worker_loc)
            os.system("cls")
            print_map(game_map)
        elif cmd == "6":
            move("right", game_map, worker_loc)
            os.system("cls")
            print_map(game_map)
        is_ok(game_map, box_locs)'''

if __name__ == '__main__':
    # 选择关卡并初始化游戏地图和工人/箱子位置
    level = input("输入关卡（1-2）：")
    d = read_cfg()  # 读取存储游戏地图和位置等信息的字典
    game_map = d[level]["game_map"]
    worker_loc = d[level]["worker_loc"]
    box_locs = d[level]["box_locs"]

    print_map(game_map)  # 打印游戏地图

    while True:
        cmd = msvcrt.getch()  # 获取按键输入
        # 根据输入选择移动方向并更新游戏地图和位置信息
        if cmd in [b'w', b'8']:
            move("up", game_map, worker_loc)
            os.system("cls")
            print_map(game_map)
        elif cmd in [b's', b'2']:
            move("down", game_map, worker_loc)
            os.system("cls")
            print_map(game_map)
        elif cmd in [b'a', b'4']:
            move("left", game_map, worker_loc)
            os.system("cls")
            print_map(game_map)
        elif cmd in [b'd', b'6']:
            move("right", game_map, worker_loc)
            os.system("cls")
            print_map(game_map)

        if is_ok(game_map, box_locs):  # 判断游戏是否胜利
            print("游戏胜利！")
            break  # 如果胜利就结束游戏循环