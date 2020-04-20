import numpy as np
import matplotlib.pyplot as plt

from cluster_analytics import ClusterAnalytics

samples = np.array(
    [[1, 1],
     [2, 1],
     [3, 1],
     [1, 2],
     [2, 2],
     [1, 3],     # 1 part
     [7, 5],
     [8, 5],
     [9, 5],
     [8, 6],
     [9, 6],
     [10, 6]])   # 2 part

samples3 = np.array(
    [[1, 1],
     [2, 1],
     [3, 1],
     [1, 2],
     [2, 2],
     [1, 3],     # 1 part
     [7, 5],
     [8, 5],
     [9, 5],
     [8, 6],
     [9, 6],
     [10, 6],     # 2 part
     [-4, -4],
     [-3, -4],
     [-4, -3],
     [-5, -5],
     [-2, -5]])   # 3 part


def draw_result(result, name):
    fig = plt.figure()

    plt.title(name)
    plt.ylabel('Y label')
    plt.xlabel('X label ')

    plt.grid(True)

    for res in result:
        xy = np.array(res)
        plt.scatter(xy[:, 0], xy[:, 1])

    plt.show()


if __name__ == '__main__':
    cluster_analytics = ClusterAnalytics(samples3)

    draw_result(cluster_analytics.average_K_method(3), 'Метод K-средних')
    draw_result(cluster_analytics.maximin_method(), 'Метод максимина')