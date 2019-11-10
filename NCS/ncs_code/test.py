import time
import numpy as np

from algorithm_ncs import ncs_c as ncs


def test(_lambda, r, epoch, n):
    p = 12  # args.data
    ncs_para = ncs.NCS_CParameter(tmax=30000, lambda_exp=_lambda, r=r, epoch=epoch, N=n)
    ncs_c = ncs.NCS_C(ncs_para, p)
    ncs_res = ncs_c.loop(quiet=False, seeds=0)
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), end=' ')
    print("ncs_res:" + str(ncs_res))


if __name__ == '__main__':
    random = np.random.RandomState(0)
    for i in range(1, 101):
        print("************ start problem ************")
        # r = round(random.uniform(1, 10), 3)
        epoch = i
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), end=' ')
        print("epoch: " + str(epoch))
        test(1, 0.944, epoch, 9)