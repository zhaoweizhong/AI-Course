import numpy as np
import random
import time

COLOR_BLACK = -1
COLOR_WHITE = 1
COLOR_NONE = 0
random.seed(0)


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
        start = time.time()  # Time Calculation Start
        # ==================================================================
        # Write your algorithm here
        # Here is the simplest sample:Random decision
        indexes = np.where(chessboard == COLOR_NONE)
        indexes = list(zip(indexes[0], indexes[1]))

        chess_Value = [[0 for i in range(size+1)] for i in range(size+1)]
        code = ""
        dic = {"0": 0, "1": 8, "2": 10, "11": 50, "22": 1000, "111": 2500, "222": 3000, "1111": 5000, "2222": 10000,
               "21": 4, "12": 2, "211": 25, "122": 20, "11112": 3000, "112": 30, "1112": 3000, "221": 500, "2221": 4000,
               "22221": 10000}
        chess_color = 0
        for index in indexes:
            for x in range(index[0] + 1, self.chessboard_size + 1):
                if chessboard[x, index[1]] == COLOR_NONE:
                    break
                else:
                    if chess_color == 0:
                        code += str(chessboard[x, index[1]])
                        chess_color = chessboard[x, index[1]]
                    else:
                        if chess_color == chessboard[x, index[1]]:
                            code += str(chessboard[x, index[1]])
                        else:
                            code += str(chessboard[x, index[1]])
                            break
        value = dic.get(code)
        if value:
            chess_Value += value
        code = ""
        chess_color = 0

        # pos_idx = random.randint(0, len(idx)-1)
        # new_pos = idx[pos_idx]
        run_time = (time.time() - start)  # Time Calculation Stop
        # ==============Find new pos========================================
        # Make sure that the position of your decision in chess board is empty.
        # If not, return error.
        assert chessboard[new_pos[0], new_pos[1]] == COLOR_NONE
        # Add your decision into candidate_list, Records the chess board
        self.candidate_list.append(new_pos)
