import numpy as np

COLOR_NONE = 0
COLOR_WHITE = 1
COLOR_BLACK = 2


class AI(object):
    # chessboard_size, color, time_out passed from agent
    def __init__(self, chessboard_size, color, time_out):
        self.chessboard_size = chessboard_size
        # You are white or black
        self.color = color
        # the max time you should use, your algorithm's run time must not
        # exceed the time limit.
        self.time_out = time_out
        # You need add your decision into your candidate_list. System will get
        # the end of your candidate_list as your decision.
        self.candidate_list = []

    # The input is current chessboard.
    def go(self, chessboard):
        # Clear candidate_list
        self.candidate_list.clear()
        # ==================================================================
        # Write your algorithm here
        # Here is the simplest sample:Random decision
        indexes = np.where(chessboard != -1)
        indexes = list(zip(indexes[0], indexes[1]))

        chess_Value = [[0 for i in range(self.chessboard_size)]
                       for i in range(self.chessboard_size)]
        if self.color == -1:  # Black
            dic = {"1": 8, "2": 10,
                   "11": 100, "22": 1000,
                   "111": 3000, "222": 3000,
                   "1111": 50000, "21": 4, "12": 2,
                   "211": 25, "122": 20,
                   "112": 30, "11122": 2000,
                   "1112": 3000, "221": 500,
                   "2221": 1000,
                   "22212": 1000, "22211": 50000, "22221": 100000, "2222": 100000, "22222": 200000}
        else:  # White
            dic = {"2": 8, "1": 10,
                   "22": 100, "11": 1000,
                   "222": 3000, "111": 3000,
                   "2222": 50000, "12": 4, "21": 2,
                   "122": 25, "211": 20,
                   "221": 30, "22211": 2000,
                   "2221": 3000, "112": 500,
                   "1112": 1000,
                   "11121": 1000, "11122": 50000, "11112": 100000, "1111": 100000, "11111": 200000}
        chess_color = 0
        for index in indexes:
            if chessboard[index[0], index[1]] != COLOR_NONE:
                continue
            code = ""
            chess_color = 0

            if index[0] == self.chessboard_size - 1:
                x_min_right = index[0]
            else:
                x_min_right = index[0] + 1
            if index[0] >= self.chessboard_size - 7:
                x_max_right = self.chessboard_size - 1
            else:
                x_max_right = index[0] + 6
            for x in range(x_min_right, x_max_right):  # 向右
                if chessboard[x, index[1]] == COLOR_NONE:
                    break
                else:
                    if chess_color == 0:
                        if chessboard[x, index[1]] == -1:
                            code += "2"
                        else:
                            code += "1"
                        chess_color = chessboard[x, index[1]]
                    else:
                        if chess_color == chessboard[x, index[1]]:
                            if chessboard[x, index[1]] == -1:
                                code += "2"
                            else:
                                code += "1"
                        else:
                            if chessboard[x, index[1]] == -1:
                                code += "2"
                            else:
                                code += "1"
                            break
            value = dic.get(code, 0)
            print("Right Code: " + code)
            print("Right Value: " + str(value))
            if value:
                chess_Value[index[0]][index[1]] += value
            code = ""
            chess_color = 0

            if index[0] == 0:
                x_min_left = index[0]
            else:
                x_min_left = index[0] - 1
            if index[0] <= self.chessboard_size - 10:
                x_max_left = self.chessboard_size - 1
            else:
                x_max_left = index[0] - 6
            for x in range(x_min_left, x_max_left):  # 向左
                if chessboard[x, index[1]] == COLOR_NONE:
                    break
                else:
                    if chess_color == 0:
                        if chessboard[x, index[1]] == -1:
                            code += "2"
                        else:
                            code += "1"
                        chess_color = chessboard[x, index[1]]
                    else:
                        if chess_color == chessboard[x, index[1]]:
                            if chessboard[x, index[1]] == -1:
                                code += "2"
                            else:
                                code += "1"
                        else:
                            if chessboard[x, index[1]] == -1:
                                code += "2"
                            else:
                                code += "1"
                            break
            value = dic.get(code, 0)
            print("Left Value: " + str(value))
            if value:
                chess_Value[index[0]][index[1]] += value
            code = ""
            chess_color = 0

            if index[1] == 0:
                y_min_up = index[1]
            else:
                y_min_up = index[1] - 1
            if index[1] <= self.chessboard_size - 10:
                y_max_up = self.chessboard_size - 1
            else:
                y_max_up = index[1] - 6
            for y in range(y_min_up, y_max_up):  # 向上
                if chessboard[index[0], y] == COLOR_NONE:
                    break
                else:
                    if chess_color == 0:
                        if chessboard[index[0], y] == -1:
                            code += "2"
                        else:
                            code += "1"
                        chess_color = chessboard[index[0], y]
                    else:
                        if chess_color == chessboard[index[0], y]:
                            if chessboard[index[0], y] == -1:
                                code += "2"
                            else:
                                code += "1"
                        else:
                            if chessboard[index[0], y] == -1:
                                code += "2"
                            else:
                                code += "1"
                            break
            value = dic.get(code, 0)
            print("Up Value: " + str(value))
            if value:
                chess_Value[index[0]][index[1]] += value
            code = ""
            chess_color = 0

            if index[1] == self.chessboard_size - 1:
                y_min_down = index[1]
            else:
                y_min_down = index[1] + 1
            if index[1] >= self.chessboard_size - 7:
                y_max_down = self.chessboard_size - 1
            else:
                y_max_down = index[1] + 6
            for y in range(y_min_down, y_max_down):  # 向下
                if chessboard[index[0], y] == COLOR_NONE:
                    break
                else:
                    if chess_color == 0:
                        if chessboard[index[0], y] == -1:
                            code += "2"
                        else:
                            code += "1"
                        chess_color = chessboard[index[0], y]
                    else:
                        if chess_color == chessboard[index[0], y]:
                            if chessboard[index[0], y] == -1:
                                code += "2"
                            else:
                                code += "1"
                        else:
                            if chessboard[index[0], y] == -1:
                                code += "2"
                            else:
                                code += "1"
                            break
            value = dic.get(code, 0)
            print("Down Value: " + str(value))
            if value:
                chess_Value[index[0]][index[1]] += value
            code = ""
            chess_color = 0

            for x, y in zip(range(x_min_right, x_max_right), range(y_min_up, y_max_up)):  # 向右上
                if chessboard[x, y] == COLOR_NONE:
                    break
                else:
                    if chess_color == 0:
                        if chessboard[x, y] == -1:
                            code += "2"
                        else:
                            code += "1"
                        chess_color = chessboard[x, y]
                    else:
                        if chess_color == chessboard[x, y]:
                            if chessboard[x, y] == -1:
                                code += "2"
                            else:
                                code += "1"
                        else:
                            if chessboard[x, y] == -1:
                                code += "2"
                            else:
                                code += "1"
                            break
            value = dic.get(code, 0)
            print("Right Up Value: " + str(value))
            if value:
                chess_Value[index[0]][index[1]] += value
            code = ""
            chess_color = 0

            for x, y in zip(range(x_min_right, x_max_right), range(y_min_down, y_max_down)):  # 向右下
                if chessboard[x, y] == COLOR_NONE:
                    break
                else:
                    if chess_color == 0:
                        if chessboard[x, y] == -1:
                            code += "2"
                        else:
                            code += "1"
                        chess_color = chessboard[x, y]
                    else:
                        if chess_color == chessboard[x, y]:
                            if chessboard[x, y] == -1:
                                code += "2"
                            else:
                                code += "1"
                        else:
                            if chessboard[x, y] == -1:
                                code += "2"
                            else:
                                code += "1"
                            break
            value = dic.get(code, 0)
            print("Right Down Value: " + str(value))
            if value:
                chess_Value[index[0]][index[1]] += value
            code = ""
            chess_color = 0

            for x, y in zip(range(x_min_left, x_max_left), range(y_min_up, y_max_up)):  # 向左上
                if chessboard[x, y] == COLOR_NONE:
                    break
                else:
                    if chess_color == 0:
                        if chessboard[x, y] == -1:
                            code += "2"
                        else:
                            code += "1"
                        chess_color = chessboard[x, y]
                    else:
                        if chess_color == chessboard[x, y]:
                            if chessboard[x, y] == -1:
                                code += "2"
                            else:
                                code += "1"
                        else:
                            if chessboard[x, y] == -1:
                                code += "2"
                            else:
                                code += "1"
                            break
            value = dic.get(code, 0)
            print("Left Up Value: " + str(value))
            if value:
                chess_Value[index[0]][index[1]] += value
            code = ""
            chess_color = 0

            for x, y in zip(range(x_min_left, x_max_left), range(y_min_down, y_max_down)):  # 向左下
                if chessboard[x, y] == COLOR_NONE:
                    break
                else:
                    if chess_color == 0:
                        if chessboard[x, y] == -1:
                            code += "2"
                        else:
                            code += "1"
                        chess_color = chessboard[x, y]
                    else:
                        if chess_color == chessboard[x, y]:
                            if chessboard[x, y] == -1:
                                code += "2"
                            else:
                                code += "1"
                        else:
                            if chessboard[x, y] == -1:
                                code += "2"
                            else:
                                code += "1"
                            break
            value = dic.get(code, 0)
            print("Left Down Value: " + str(value))
            if value:
                chess_Value[index[0]][index[1]] += value
            code = ""
            chess_color = 0

        mymax = 0
        result = [0 for i in range(2)]

        # 遍历棋盘
        for index in indexes:
            if chess_Value[index[0]][index[1]] >= mymax and chessboard[index[0], index[1]] == COLOR_NONE:
                # 获得权值最大点，xxx，yyy保存最大点位置
                mymax = chess_Value[index[0]][index[1]]
                result[0] = index[0]
                result[1] = index[1]

        print("color: " + str(self.color))
        print("chess_Value: " + str(chess_Value))
        print("result: " + str(result))
        # pos_idx = random.randint(0, len(idx)-1)
        # new_pos = idx[pos_idx]
        # ==============Find new pos========================================
        # Make sure that the position of your decision in chess board is empty.
        # If not, return error.
        assert chessboard[result[0], result[1]] == COLOR_NONE, result
        # Add your decision into candidate_list, Records the chess board
        self.candidate_list.append(result)
