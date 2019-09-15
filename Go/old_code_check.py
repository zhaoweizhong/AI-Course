#!/usr/bin/env python3
"""
check the security and functionability of uploaded code
- forbid from importing os
- random chessboard check
- some special case check
"""
import imp
import traceback
import numpy as np


FORBIDDEN_LIST = ['import os', 'exec']


class CodeCheck():
    def __init__(self, script_file_path, chessboard_size):
        self.time_out = 5
        self.script_file_path = script_file_path
        self.chessboard_size = chessboard_size
        self.agent = None
        self.errormsg = 'Error'
        # sys.stdout = open(os.devnull, 'w')
        # sys.stderr = open(os.devnull, 'w')
        # print(self.chessboard)

    # Call this function and get True or False, self.errormsg has the massage
    def check_code(self):
        # check if contains forbidden library
        if self.__check_forbidden_import() is False:
            return False

        # check initialization
        try:
            self.agent = imp.load_source('AI', self.script_file_path).AI(
                self.chessboard_size, 1, self.time_out)
            self.agent = imp.load_source('AI', self.script_file_path).AI(
                self.chessboard_size, -1, self.time_out)
        except Exception:
            self.errormsg = "Fail to init"
            return False

        # # check simple condition
        if not self.__check_simple_chessboard():
            self.errormsg = "Can not pass usability test."
            return False

        # check advance condition, online test contain more test case than this demo
        if not self.__check_advance_chessboard():
            self.errormsg = "Your code is too weak, fail to pass base test."
            return False

        return True

    def __check_forbidden_import(self):
        with open(self.script_file_path, 'r', encoding='UTF-8') as myfile:
            data = myfile.read()
            for keyword in FORBIDDEN_LIST:
                idx = data.find(keyword)
                if idx != -1:
                    self.errormsg = "import forbidden"
                    return False
        return True

    def __check_go(self, chessboard):
        self.agent = imp.load_source('AI', self.script_file_path).AI(
            self.chessboard_size, -1, self.time_out)
        try:
            self.agent.go(np.copy(chessboard))
        except Exception:
            self.errormsg = "Error:" + traceback.format_exc()
            print(self.errormsg)
            return False
        return True

    def __check_result(self, chessboard, result):
        if not self.__check_go(chessboard):
            return False
        print(chessboard)
        # print(self.agent.candidate_list)
        if not self.agent.candidate_list or list(self.agent.candidate_list[-1]) not in result:
            return False
        return True

    def __check_simple_chessboard(self):
        return True
        # empty chessboard
        print("This is Simple Test")
        if not self.__check_go(np.zeros((self.chessboard_size, self.chessboard_size), dtype=np.int)):
            return False

        # only one empty position remain
        chessboard = np.ones((self.chessboard_size, self.chessboard_size))
        chessboard[:, ::2] = -1
        for i in range(0, self.chessboard_size, 4):
            chessboard[i] = -chessboard[i]
        x, y = np.random.choice(self.chessboard_size, 2)
        chessboard[x, y] = 0
        print("Expected: [" + str(x) + ", " + str(y) + "]")
        if not self.__check_result(chessboard, [[x, y]]):
            return False

        return True

    def __check_advance_chessboard(self):
        #
        # print("\nThis is Advanced Test 1")
        # print("Expected: [5, 5]")
        # chessboard = np.zeros((self.chessboard_size, self.chessboard_size), dtype=np.int)
        # chessboard[2, 2] = 1
        # chessboard[3, 3] = 1
        # chessboard[4, 4] = 1
        # chessboard[5, 6] = 1
        # chessboard[5, 8] = 1
        # chessboard[1:3, 11] = -1
        # chessboard[3, 9:11] = -1
        # chessboard[6, 13] = -1
        # if not self.__check_result(chessboard, [[5, 5]]):
        #     self.errorcase = 1
        #     return False

        #
        # print("\nThis is Advanced Test 2")
        # print("Expected: [1, 9]")
        # chessboard = np.zeros((self.chessboard_size, self.chessboard_size), dtype=np.int)
        # chessboard[2, 2:4] = 1
        # chessboard[4, 1:3] = 1
        # chessboard[1, 10:12] = -1
        # chessboard[2, 10] = -1
        # chessboard[4, 12] = -1
        # if not self.__check_result(chessboard, [[1, 9]]):
        #     self.errorcase = 2
        #     return False

        # #
        # print("\nThis is Advanced Test 3")
        # print("Expected: [4, 2]")
        # chessboard = np.zeros((self.chessboard_size, self.chessboard_size), dtype=np.int)
        # chessboard[2, 2] = 1
        # chessboard[2, 4] = 1
        # chessboard[3, 2:4] = 1
        # chessboard[5, 2] = 1
        # chessboard[1, 10:12] = -1
        # chessboard[2, 10] = -1
        # chessboard[4, 12:14] = -1
        # if not self.__check_result(chessboard, [[4, 2]]):
        #     self.errorcase = 3
        #     return False

        # #
        # print("\nThis is Advanced Test 4")
        # print("Expected: [5, 2]")
        # chessboard = np.zeros((self.chessboard_size, self.chessboard_size), dtype=np.int)
        # chessboard[2:5, 2] = 1
        # chessboard[6, 3:5] = 1
        # chessboard[1, 10:12] = -1
        # chessboard[2, 10] = -1
        # chessboard[4, 12:14] = -1
        # if not self.__check_result(chessboard, [[5, 2]]):
        #     self.errorcase = 4
        #     return False

        #
        print("\nThis is Advanced Test 5")
        print("Expected: [1, 8]")
        chessboard = np.zeros((self.chessboard_size, self.chessboard_size), dtype=np.int)
        chessboard[13, 9] = 1
        chessboard[13, 10] = 1
        chessboard[13, 11] = 1
        chessboard[13, 13] = 1
        chessboard[13, 14] = -1
        chessboard[14, 14] = -1
        chessboard[12, 12] = -1
        chessboard[11, 13] = -1
        # chessboard[2, 11:13] = -1
        # chessboard[5, 13] = -1
        if not self.__check_result(chessboard, [[1, 8]]):
            self.errorcase = 5
            return False
        return True
