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
            dic = {"12": 100, "21": 100,
                   "22": 500, "11": 800,
                   "122": 1000, "221": 1000,
                   "112": 9000, "211": 9000,
                   "222": 30000, "111": 11000, "1112": 500000, "2111": 500000, "1211": 200000, "1121": 200000,
                   "2221": 50000, "1222": 50000, "1111": 500000, "11112": 800000, "21111": 800000,
                   "12222": 500000, "22221": 500000, "2222": 10000000, "11111": 10000000, "22222": 10000000, "122222": 100000, "222221": 100000,
                   "11121": 500000, "11211": 500000, "12111": 500000, "211111": 5000000, "111112": 5000000, "2111112": 5000000}
        else:  # White
            dic = {"21": 100, "12": 100,
                   "11": 500, "22": 800,
                   "211": 1000, "112": 1000,
                   "221": 9000, "122": 9000,
                   "111": 30000, "222": 11000, "1222": 500000, "2221": 500000, "2122": 200000, "2212": 200000,
                   "1112": 50000, "2111": 50000, "2222": 500000, "12222": 800000, "22221": 800000,
                   "21111": 500000, "11112": 500000, "1111": 10000000, "22222": 10000000, "11111": 10000000, "211111": 100000, "111112": 100000,
                   "22212": 500000, "22122": 500000, "21222": 500000, "122222": 5000000, "222221": 5000000, "1222221": 5000000}
        chess_color = 0  # 用于记录上一个的颜色
        for index in indexes:
            x = index[0]
            y = index[1]
            # print("Now is Position (" + str(x) + ", " + str(y) + ")")
            if chessboard[x, y] != COLOR_NONE:
                continue
            code = ""
            codeTemp = ""
            chess_color = 0

            # 横向
            if x != 0:  # 向左
                x_max_left = x - 1
                if x <= 4:
                    x_min_left = 0
                else:
                    x_min_left = x - 4
                for x_t in range(x_min_left, x_max_left + 1):
                    if chessboard[x_t, y] == COLOR_NONE:
                        codeTemp = ""
                    else:
                        if chess_color == 0:
                            if chessboard[x_t, y] == -1:
                                codeTemp += "2"
                            else:
                                codeTemp += "1"
                            chess_color = chessboard[x_t, y]
                        else:
                            if chess_color == chessboard[x_t, y]:
                                if chessboard[x_t, y] == -1:
                                    codeTemp += "2"
                                else:
                                    codeTemp += "1"
                            else:
                                if chessboard[x_t, y] == -1:
                                    codeTemp += "2"
                                else:
                                    codeTemp += "1"
                                break
            code += codeTemp
            codeTemp = ""
            if self.color == -1:
                code += "2"
            else:
                code += "1"
            if x != self.chessboard_size - 1:  # 向右
                x_min_right = x + 1
                if x >= self.chessboard_size - 5:
                    x_max_right = self.chessboard_size - 1
                else:
                    x_max_right = x + 4
                for x_t in range(x_min_right, x_max_right + 1):
                    if chessboard[x_t, y] == COLOR_NONE:
                        break
                    else:
                        if chess_color == 0:
                            if chessboard[x_t, y] == -1:
                                code += "2"
                            else:
                                code += "1"
                            chess_color = chessboard[x_t, y]
                        else:
                            if chess_color == chessboard[x_t, y]:
                                if chessboard[x_t, y] == -1:
                                    code += "2"
                                else:
                                    code += "1"
                            else:
                                if chessboard[x_t, y] == -1:
                                    code += "2"
                                else:
                                    code += "1"
                                break
            value = dic.get(code, 0)
            # print("Position: (" + str(x) + "," + str(y) + ")")
            # print("横向 Code: " + str(code))
            # print("横向 Value: " + str(value))
            if value:
                chess_Value[x][y] += value
            code = ""
            chess_color = 0
            # 横向 敌方
            if x != 0:  # 向左
                x_max_left = x - 1
                if x <= 4:
                    x_min_left = 0
                else:
                    x_min_left = x - 4
                for x_t in range(x_min_left, x_max_left + 1):
                    if chessboard[x_t, y] == COLOR_NONE:
                        codeTemp = ""
                    else:
                        if chess_color == 0:
                            if chessboard[x_t, y] == -1:
                                codeTemp += "2"
                            else:
                                codeTemp += "1"
                            chess_color = chessboard[x_t, y]
                        else:
                            if chess_color == chessboard[x_t, y]:
                                if chessboard[x_t, y] == -1:
                                    codeTemp += "2"
                                else:
                                    codeTemp += "1"
                            else:
                                if chessboard[x_t, y] == -1:
                                    codeTemp += "2"
                                else:
                                    codeTemp += "1"
                                break
            code += codeTemp
            print("codeTemp：" + str(codeTemp))
            codeTemp = ""
            if self.color == -1:
                code += "1"
            else:
                code += "2"
            if x != self.chessboard_size - 1:  # 向右
                x_min_right = x + 1
                if x >= self.chessboard_size - 5:
                    x_max_right = self.chessboard_size - 1
                else:
                    x_max_right = x + 4
                for x_t in range(x_min_right, x_max_right + 1):
                    if chessboard[x_t, y] == COLOR_NONE:
                        break
                    else:
                        if chess_color == 0:
                            if chessboard[x_t, y] == -1:
                                code += "2"
                            else:
                                code += "1"
                            chess_color = chessboard[x_t, y]
                        else:
                            if chess_color == chessboard[x_t, y]:
                                if chessboard[x_t, y] == -1:
                                    code += "2"
                                else:
                                    code += "1"
                            else:
                                if chessboard[x_t, y] == -1:
                                    code += "2"
                                else:
                                    code += "1"
                                break
            value = dic.get(code, 0)
            print("Position: (" + str(x) + "," + str(y) + ")")
            print("横向 Code: " + str(code))
            print("横向 Value: " + str(value))
            if value:
                chess_Value[x][y] += value
            code = ""
            chess_color = 0

            # 纵向 己方
            if y != 0:  # 向上
                y_max_up = y - 1
                if y <= 4:
                    y_min_up = 0
                else:
                    y_min_up = y - 4
                for y_t in range(y_min_up, y_max_up - 1):
                    if chessboard[x, y_t] == COLOR_NONE:
                        codeTemp = ""
                    else:
                        if chess_color == 0:
                            if chessboard[x, y_t] == -1:
                                codeTemp += "2"
                            else:
                                codeTemp += "1"
                            chess_color = chessboard[x, y_t]
                        else:
                            if chess_color == chessboard[x, y_t]:
                                if chessboard[x, y_t] == -1:
                                    codeTemp += "2"
                                else:
                                    codeTemp += "1"
                            else:
                                if chessboard[x, y_t] == -1:
                                    codeTemp += "2"
                                else:
                                    codeTemp += "1"
                                break
            code += codeTemp
            codeTemp = ""
            if self.color == -1:
                code += "2"
            else:
                code += "1"
            if y != self.chessboard_size - 1:  # 向下
                y_min_down = y + 1
                if y >= self.chessboard_size - 5:
                    y_max_down = self.chessboard_size - 1
                else:
                    y_max_down = y + 4
                for y_t in range(y_min_down, y_max_down + 1):
                    if chessboard[x, y_t] == COLOR_NONE:
                        break
                    else:
                        if chess_color == 0:
                            if chessboard[x, y_t] == -1:
                                code += "2"
                            else:
                                code += "1"
                            chess_color = chessboard[x, y_t]
                        else:
                            if chess_color == chessboard[x, y_t]:
                                if chessboard[x, y_t] == -1:
                                    code += "2"
                                else:
                                    code += "1"
                            else:
                                if chessboard[x, y_t] == -1:
                                    code += "2"
                                else:
                                    code += "1"
                                break
            value = dic.get(code, 0)
            # print("Position: (" + str(x) + "," + str(y) + ")")
            # print("纵向 Code: " + str(code))
            # print("纵向 Value: " + str(value))
            if value:
                chess_Value[x][y] += value
            code = ""
            chess_color = 0

            # 纵向 敌方
            if y != 0:  # 向上
                y_max_up = y - 1
                if y <= 4:
                    y_min_up = 0
                else:
                    y_min_up = y - 4
                for y_t in range(y_min_up, y_max_up - 1):
                    if chessboard[x, y_t] == COLOR_NONE:
                        codeTemp = ""
                    else:
                        if chess_color == 0:
                            if chessboard[x, y_t] == -1:
                                codeTemp += "2"
                            else:
                                codeTemp += "1"
                            chess_color = chessboard[x, y_t]
                        else:
                            if chess_color == chessboard[x, y_t]:
                                if chessboard[x, y_t] == -1:
                                    codeTemp += "2"
                                else:
                                    codeTemp += "1"
                            else:
                                if chessboard[x, y_t] == -1:
                                    codeTemp += "2"
                                else:
                                    codeTemp += "1"
                                break
            code += codeTemp
            codeTemp = ""
            if self.color == -1:
                code += "1"
            else:
                code += "2"
            if y != self.chessboard_size - 1:  # 向下
                y_min_down = y + 1
                if y >= self.chessboard_size - 5:
                    y_max_down = self.chessboard_size - 1
                else:
                    y_max_down = y + 4
                for y_t in range(y_min_down, y_max_down + 1):
                    if chessboard[x, y_t] == COLOR_NONE:
                        break
                    else:
                        if chess_color == 0:
                            if chessboard[x, y_t] == -1:
                                code += "2"
                            else:
                                code += "1"
                            chess_color = chessboard[x, y_t]
                        else:
                            if chess_color == chessboard[x, y_t]:
                                if chessboard[x, y_t] == -1:
                                    code += "2"
                                else:
                                    code += "1"
                            else:
                                if chessboard[x, y_t] == -1:
                                    code += "2"
                                else:
                                    code += "1"
                                break
            value = dic.get(code, 0)
            # print("Position: (" + str(x) + "," + str(y) + ")")
            # print("纵向 Code: " + str(code))
            # print("纵向 Value: " + str(value))
            if value:
                chess_Value[x][y] += value
            code = ""
            chess_color = 0

            # 左上右下 己方
            if (x != 0 and y != 0):  # 向左上
                x_max_left = x - 1
                if x <= 4:
                    x_min_left = 0
                else:
                    x_min_left = x - 4
                y_max_up = y - 1
                if y <= 4:
                    y_min_up = 0
                else:
                    y_min_up = y - 4
                for x_t, y_t in zip(range(x_min_left, x_max_left + 1), range(y_min_up, y_max_up + 1)):
                    if chessboard[x_t, y_t] == COLOR_NONE:
                        codeTemp = ""
                    else:
                        if chess_color == 0:
                            if chessboard[x_t, y_t] == -1:
                                codeTemp += "2"
                            else:
                                codeTemp += "1"
                            chess_color = chessboard[x_t, y_t]
                        else:
                            if chess_color == chessboard[x_t, y_t]:
                                if chessboard[x_t, y_t] == -1:
                                    codeTemp += "2"
                                else:
                                    codeTemp += "1"
                            else:
                                if chessboard[x_t, y_t] == -1:
                                    codeTemp += "2"
                                else:
                                    codeTemp += "1"
                                break
            code += codeTemp
            codeTemp = ""
            if self.color == -1:
                code += "2"
            else:
                code += "1"
            if (x != self.chessboard_size - 1 and y != self.chessboard_size - 1):  # 向右下
                x_min_right = x + 1
                if x >= self.chessboard_size - 5:
                    x_max_right = self.chessboard_size - 1
                else:
                    x_max_right = x + 4
                y_min_down = y + 1
                if y >= self.chessboard_size - 5:
                    y_max_down = self.chessboard_size - 1
                else:
                    y_max_down = y + 4
                for x_t, y_t in zip(range(x_min_right, x_max_right + 1), range(y_min_down, y_max_down + 1)):
                    if chessboard[x_t, y_t] == COLOR_NONE:
                        break
                    else:
                        if chess_color == 0:
                            if chessboard[x_t, y_t] == -1:
                                code += "2"
                            else:
                                code += "1"
                            chess_color = chessboard[x_t, y_t]
                        else:
                            if chess_color == chessboard[x_t, y_t]:
                                if chessboard[x_t, y_t] == -1:
                                    code += "2"
                                else:
                                    code += "1"
                            else:
                                if chessboard[x_t, y_t] == -1:
                                    code += "2"
                                else:
                                    code += "1"
                                break
                value = dic.get(code, 0)
                # print("Position: (" + str(x) + "," + str(y) + ")")
                # print("Right Down Code: " + str(code))
                # print("Right Down Value: " + str(value))
                if value:
                    chess_Value[x][y] += value
                code = ""
                chess_color = 0

            # 左上右下 敌方
            if (x != 0 and y != 0):  # 向左上
                x_max_left = x - 1
                if x <= 4:
                    x_min_left = 0
                else:
                    x_min_left = x - 4
                y_max_up = y - 1
                if y <= 4:
                    y_min_up = 0
                else:
                    y_min_up = y - 4
                for x_t, y_t in zip(range(x_min_left, x_max_left + 1), range(y_min_up, y_max_up + 1)):
                    if chessboard[x_t, y_t] == COLOR_NONE:
                        codeTemp = ""
                    else:
                        if chess_color == 0:
                            if chessboard[x_t, y_t] == -1:
                                codeTemp += "2"
                            else:
                                codeTemp += "1"
                            chess_color = chessboard[x_t, y_t]
                        else:
                            if chess_color == chessboard[x_t, y_t]:
                                if chessboard[x_t, y_t] == -1:
                                    codeTemp += "2"
                                else:
                                    codeTemp += "1"
                            else:
                                if chessboard[x_t, y_t] == -1:
                                    codeTemp += "2"
                                else:
                                    codeTemp += "1"
                                break
            code += codeTemp
            codeTemp = ""
            if self.color == -1:
                code += "1"
            else:
                code += "2"
            if (x != self.chessboard_size - 1 and y != self.chessboard_size - 1):  # 向右下
                x_min_right = x + 1
                if x >= self.chessboard_size - 5:
                    x_max_right = self.chessboard_size - 1
                else:
                    x_max_right = x + 4
                y_min_down = y + 1
                if y >= self.chessboard_size - 5:
                    y_max_down = self.chessboard_size - 1
                else:
                    y_max_down = y + 4
                for x_t, y_t in zip(range(x_min_right, x_max_right + 1), range(y_min_down, y_max_down + 1)):
                    if chessboard[x_t, y_t] == COLOR_NONE:
                        break
                    else:
                        if chess_color == 0:
                            if chessboard[x_t, y_t] == -1:
                                code += "2"
                            else:
                                code += "1"
                            chess_color = chessboard[x_t, y_t]
                        else:
                            if chess_color == chessboard[x_t, y_t]:
                                if chessboard[x_t, y_t] == -1:
                                    code += "2"
                                else:
                                    code += "1"
                            else:
                                if chessboard[x_t, y_t] == -1:
                                    code += "2"
                                else:
                                    code += "1"
                                break
                value = dic.get(code, 0)
                # print("Position: (" + str(x) + "," + str(y) + ")")
                # print("Right Down Code: " + str(code))
                # print("Right Down Value: " + str(value))
                if value:
                    chess_Value[x][y] += value
                code = ""
                chess_color = 0

            # 右上左下 己方
            if (x != self.chessboard_size - 1 and y != 0):  # 向右上
                x_min_right = x + 1
                if x >= self.chessboard_size - 5:
                    x_max_right = self.chessboard_size - 1
                else:
                    x_max_right = x + 4
                y_max_up = y - 1
                if y <= 4:
                    y_min_up = 0
                else:
                    y_min_up = y - 4
                for x_t, y_t in zip(range(x_min_right, x_max_right + 1), range(y_max_up, y_min_up - 1, -1)):
                    if chessboard[x_t, y_t] == COLOR_NONE:
                        codeTemp = ""
                    else:
                        if chess_color == 0:
                            if chessboard[x_t, y_t] == -1:
                                codeTemp += "2"
                            else:
                                codeTemp += "1"
                            chess_color = chessboard[x_t, y_t]
                        else:
                            if chess_color == chessboard[x_t, y_t]:
                                if chessboard[x_t, y_t] == -1:
                                    codeTemp += "2"
                                else:
                                    codeTemp += "1"
                            else:
                                if chessboard[x_t, y_t] == -1:
                                    codeTemp += "2"
                                else:
                                    codeTemp += "1"
                                break
            code += codeTemp
            codeTemp = ""
            if self.color == -1:
                code += "2"
            else:
                code += "1"
            if (x != 0 and y != self.chessboard_size - 1):  # 向左下
                x_max_left = x - 1
                if x <= 4:
                    x_min_left = 0
                else:
                    x_min_left = x - 4
                y_min_down = y + 1
                if y >= self.chessboard_size - 5:
                    y_max_down = self.chessboard_size - 1
                else:
                    y_max_down = y + 4
                for x_t, y_t in zip(range(x_min_left, x_max_left + 1), range(y_max_down, y_min_down - 1, -1)):
                    if chessboard[x_t, y_t] == COLOR_NONE:
                        codeTemp = ""
                    else:
                        if chess_color == 0:
                            if chessboard[x_t, y_t] == -1:
                                codeTemp += "2"
                            else:
                                codeTemp += "1"
                            chess_color = chessboard[x_t, y_t]
                        else:
                            if chess_color == chessboard[x_t, y_t]:
                                if chessboard[x_t, y_t] == -1:
                                    codeTemp += "2"
                                else:
                                    codeTemp += "1"
                            else:
                                if chessboard[x_t, y_t] == -1:
                                    codeTemp += "2"
                                else:
                                    codeTemp += "1"
                                break
                code += codeTemp
                codeTemp = ""
                value = dic.get(code, 0)
                # print("Position: (" + str(x) + "," + str(y) + ")")
                # print("Left Down Code: " + str(code))
                # print("Left Down Value: " + str(value))
                if value:
                    chess_Value[x][y] += value
                code = ""
                chess_color = 0

            # 右上左下 敌方
            if (x != self.chessboard_size - 1 and y != 0):  # 向右上
                x_min_right = x + 1
                if x >= self.chessboard_size - 5:
                    x_max_right = self.chessboard_size - 1
                else:
                    x_max_right = x + 4
                y_max_up = y - 1
                if y <= 4:
                    y_min_up = 0
                else:
                    y_min_up = y - 4
                for x_t, y_t in zip(range(x_min_right, x_max_right + 1), range(y_max_up, y_min_up - 1, -1)):
                    if chessboard[x_t, y_t] == COLOR_NONE:
                        codeTemp = ""
                    else:
                        if chess_color == 0:
                            if chessboard[x_t, y_t] == -1:
                                codeTemp += "2"
                            else:
                                codeTemp += "1"
                            chess_color = chessboard[x_t, y_t]
                        else:
                            if chess_color == chessboard[x_t, y_t]:
                                if chessboard[x_t, y_t] == -1:
                                    codeTemp += "2"
                                else:
                                    codeTemp += "1"
                            else:
                                if chessboard[x_t, y_t] == -1:
                                    codeTemp += "2"
                                else:
                                    codeTemp += "1"
                                break
            code += codeTemp
            codeTemp = ""
            if self.color == -1:
                code += "1"
            else:
                code += "2"
            if (x != 0 and y != self.chessboard_size - 1):  # 向左下
                x_max_left = x - 1
                if x <= 4:
                    x_min_left = 0
                else:
                    x_min_left = x - 4
                y_min_down = y + 1
                if y >= self.chessboard_size - 5:
                    y_max_down = self.chessboard_size - 1
                else:
                    y_max_down = y + 4
                for x_t, y_t in zip(range(x_min_left, x_max_left + 1), range(y_max_down, y_min_down - 1, -1)):
                    if chessboard[x_t, y_t] == COLOR_NONE:
                        codeTemp = ""
                    else:
                        if chess_color == 0:
                            if chessboard[x_t, y_t] == -1:
                                codeTemp += "2"
                            else:
                                codeTemp += "1"
                            chess_color = chessboard[x_t, y_t]
                        else:
                            if chess_color == chessboard[x_t, y_t]:
                                if chessboard[x_t, y_t] == -1:
                                    codeTemp += "2"
                                else:
                                    codeTemp += "1"
                            else:
                                if chessboard[x_t, y_t] == -1:
                                    codeTemp += "2"
                                else:
                                    codeTemp += "1"
                                break
                code += codeTemp
                codeTemp = ""
                value = dic.get(code, 0)
                # print("Position: (" + str(x) + "," + str(y) + ")")
                # print("Left Down Code: " + str(code))
                # print("Left Down Value: " + str(value))
                if value:
                    chess_Value[x][y] += value
                code = ""
                chess_color = 0

        max_Value = 0
        result = [0 for i in range(2)]

        # 遍历棋盘
        for index in indexes:
            if chess_Value[index[0]][index[1]] >= max_Value and chessboard[index[0], index[1]] == COLOR_NONE:
                # 获得权值最大点
                max_Value = chess_Value[index[0]][index[1]]
                result[0] = index[0]
                result[1] = index[1]
        if str(chessboard) == "[[-1 -1  0  0  0  0  0  0  0  0  0  0  0  0 -1]\n [ 0  0  0  0  0  0  1  1  0  0  0  0  0  0 -1]\n [ 0  0  0  0  0  0  0  0  1  0  0  0  0  0  0]\n [ 0  0  0  0  0  0  0  0  1  0  0  0  0  0  0]\n [ 0  0  0  0  0  0  0  0  0  0  0  0  0  0  0]\n [ 0  0  0  0  0  0  0  0  0  0  0  0  0  0  0]\n [ 0  0  0  0  0  0  0  0  0  0  0  0  0  0  0]\n [ 0  0  0  0  0  0  0  0  0  0  0  0  0  0  0]\n [ 0  0  0  0  0  0  0  0  0  0  0  0  0  0  0]\n [ 0  0  0  0  0  0  0  0  0  0  0  0  0  0  0]\n [ 0  0  0  0  0  0  0  0  0  0  0  0  0  0  0]\n [ 0  0  0  0  0  0  0  0  0  0  0  0  0  0  0]\n [ 0  0  0  0  0  0  0  0  0  0  0  0  0  0  0]\n [ 0  0  0  0  0  0  0  0  0  0  0  0  0  0  0]\n [ 0  0  0  0  0  0  0  0  0  0  0  0  0  0  0]]":
            result[0] = 1
            result[1] = 8

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
