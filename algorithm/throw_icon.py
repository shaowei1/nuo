import random
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def flip_coin(times):
    data_array = np.empty(times)
    weights_array = np.empty(times)
    weights_array.fill(1 / times)

    for i in range(0, times):  # 抛 times 次的硬币
        data_array[i] = random.randint(0, 1)  # 假设 0 表示正面，1 表示反面

    data_frame = pd.DataFrame(data_array)
    data_frame.plot(kind='hist', legend=False)  # 获取正反面统计次数的直方图
    data_frame.plot(kind='hist', legend=False, weights=weights_array).set_ylabel("Probability")  # 获取正反面统计概率的直方图
    plt.show()


def check_speed(time_gap, speed_gap, total_time, min_speed, max_speed):
    times = (int)(total_time / time_gap)  # 获取读取仪表盘的次数

    data_array = np.empty(times)
    weights_array = np.empty(times)
    weights_array.fill(1 / times)

    for i in range(0, times):
        if (speed_gap < 1):
            data_array[i] = random.random() * max_speed  # 随机生成一个最高速和最低速之间的速度
        else:
            data_array[i] = random.randint(0,
                                           max_speed / speed_gap) * speed_gap  # 随机生成一个最高速和最低速之间的速度，先除以 speed_gap 然后乘以 speed_gap 进行离散化

    data_frame = pd.DataFrame(data_array)
    bin_range = np.arange(0, 200, speed_gap)
    data_frame.plot(kind='hist', bins=bin_range, legend=False)  # 获取时速统计次数的直方图
    data_frame.plot(kind='hist', bins=bin_range, legend=False, weights=weights_array, ).set_ylabel(
        "Probability")  # 获取时速统计概率的直方图
    plt.show()

# flip_coin(10)
# check_speed(1, 5, 60, 0, 200)
# check_speed(0.1, 1, 600, 0, 200)
# check_speed(0.001, 0.01, 600, 0, 200)
