def __check_advance_chessboard(self):
        # win
        chessboard = np.zeros(
            (self.chessboard_size, self.chessboard_size), dtype=np.int)
        chessboard[0, 0:4] = -1
        chessboard[1, 0:4] = 1
        if not self.__check_result(chessboard, [[0, 4]]):
            return False
        # 斜赢
        chessboard = np.zeros(
            (self.chessboard_size, self.chessboard_size), dtype=np.int)
        chessboard[0, 4:6] = 1
        chessboard[0, 7] = 1
        chessboard[1, 3] = -1
        chessboard[2, 4] = -1
        chessboard[3, 5] = -1
        chessboard[4, 6] = -1
        if not self.__check_result(chessboard, [[0, 2], [5, 7]]):
            print('#斜赢')
            return False

        # defense 5 inline
        chessboard = np.zeros(
            (self.chessboard_size, self.chessboard_size), dtype=np.int)
        chessboard[0, 0:2] = -1
        chessboard[0, 7] = -1
        chessboard[1, 1:4] = 1
        if not self.__check_result(chessboard, [[1, 4], [1, 0], [1, 5]]):
            print('# defense 5 inline')
            return False
        # 斜defense 5
        chessboard = np.zeros(
            (self.chessboard_size, self.chessboard_size), dtype=np.int)
        chessboard[2:5, 8] = -1
        chessboard[1, 1] = -1
        chessboard[2, 2] = 1
        chessboard[3, 3] = 1
        chessboard[4, 4] = 1
        chessboard[5, 5] = 1
        if not self.__check_result(chessboard, [[6, 6]]):
            print('# 斜defense 5')
            return False

        # two three
        chessboard = np.zeros(
            (self.chessboard_size, self.chessboard_size), dtype=np.int)
        chessboard[1, 1:3] = -1
        chessboard[2:4, 3] = -1
        chessboard[1, 6:8] = 1
        chessboard[2:4, 8] = 1
        if not self.__check_result(chessboard, [[1, 3]]):
            print('# two three')
            return False
        # 斜攻双三
        chessboard = np.zeros(
            (self.chessboard_size, self.chessboard_size), dtype=np.int)
        chessboard[0, 0:2] = 1
        chessboard[0:2, self.chessboard_size - 1] = 1
        chessboard[1, 6] = -1
        chessboard[2, 7] = -1
        chessboard[4, 7] = -1
        chessboard[5, 6] = -1
        if not self.__check_result(chessboard, [[3, 8]]):
            print('# 斜攻双三1')
            return False
        chessboard = np.zeros(
            (self.chessboard_size, self.chessboard_size), dtype=np.int)
        chessboard[0, 0:2] = 1
        chessboard[0:2, self.chessboard_size - 1] = 1
        chessboard[1, 6] = -1
        chessboard[2, 5] = -1
        chessboard[4, 5] = -1
        chessboard[5, 6] = -1
        if not self.__check_result(chessboard, [[3, 4]]):
            print('# 斜攻双三2')
            return False
        # defense

        # 斜防双三
        chessboard = np.zeros(
            (self.chessboard_size, self.chessboard_size), dtype=np.int)
        chessboard[0, 0:2] = -1
        chessboard[0:2, self.chessboard_size - 1] = -1
        chessboard[1, 6] = 1
        chessboard[2, 7] = 1
        chessboard[4, 7] = 1
        chessboard[5, 6] = 1
        if not self.__check_result(chessboard, [[3, 8], [0, 5], [6, 5]]):
            print(' # 斜防双三1')
            return False
        chessboard = np.zeros(
            (self.chessboard_size, self.chessboard_size), dtype=np.int)
        chessboard[0, 0:2] = -1
        chessboard[0:2, self.chessboard_size - 1] = -1
        chessboard[1, 6] = 1
        chessboard[2, 5] = 1
        chessboard[4, 5] = 1
        chessboard[5, 6] = 1
        if not self.__check_result(chessboard, [[3, 4], [0, 7], [6, 7]]):
            print(' # 斜防双三2')
            return False

        return True
