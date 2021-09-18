import copy

import matplotlib.pyplot as plt
import random
import math

POINTS_NUMBER = 8
QUALITY_SOLUTION = 1.55


# random.seed(0)

# calculate the total distance
def cal_distance(passed_point):
    total_distance = 0
    for k in range(0, POINTS_NUMBER):
        if k == POINTS_NUMBER - 1:
            total_distance = total_distance + distance[passed_point[k]][passed_point[0]]
        else:
            total_distance = total_distance + distance[passed_point[k]][passed_point[k + 1]]

    return total_distance


# randomly generate points
def generate_point():
    result = []
    while len(result) < POINTS_NUMBER:
        x = random.randint(0, 10)
        y = random.randint(0, 10)
        if [x, y] in result:
            continue
        else:
            result.append([x, y])

    return result


# plot figure
def plot_figure(figure_num, optimal_result, passed_point, first_point):
    plt.figure(figure_num)

    for x, y in optimal_result:
        plt.scatter(x, y, c='r')

    plt.xlim(-1, 11, 1)
    plt.ylim(-1, 11, 1)

    for k in range(0, POINTS_NUMBER):
        x_start = optimal_result[passed_point[k]][0]
        y_start = optimal_result[passed_point[k]][1]
        if k == 1:
            print(x_start)
        if k == POINTS_NUMBER - 1:
            x_end = optimal_result[passed_point[0]][0]
            y_end = optimal_result[passed_point[0]][1]
        else:
            x_end = optimal_result[passed_point[k + 1]][0]
            y_end = optimal_result[passed_point[k + 1]][1]

        plt.quiver(x_start, y_start, x_end - x_start, y_end - y_start, angles='xy', scale=1, scale_units='xy')
        k = k + 1

    plt.scatter(optimal_result[first_point][0], optimal_result[first_point][1], c='g', s=500)
    #plt.xlabel('optimal result')

    plt.grid()
    plt.show()


# calculate distance between every two points
def distance_between_points(result):
    distance = [[0 for i in range(POINTS_NUMBER)] for i in range(POINTS_NUMBER)]
    for i in range(0, POINTS_NUMBER):
        for j in range(0, POINTS_NUMBER):
            distance[i][j] = math.sqrt((result[i][0] - result[j][0]) ** 2 + (result[i][1] - result[j][1]) ** 2)
    return distance


# main
optimal_result = []
optimal_passed_point = []
worst_passed_point = []
optimal_first_point = 0
worst_first_point = 0

while True:
    result = generate_point()
    distance = distance_between_points(result)
    optimal_distance = 999
    worst_distance = 0

    for first_point in range(0, POINTS_NUMBER):
        temp_dis = copy.deepcopy(distance)
        passed_point = []
        current_point = first_point
        passed_point.append(current_point)

        # omit the passed point
        while len(passed_point) < POINTS_NUMBER:
            for point_index in passed_point:
                temp_dis[current_point][point_index] = 99

            current_point = temp_dis[current_point].index(min(temp_dis[current_point][:]))  # 更新current_point到下一个点
            passed_point.append(current_point)

        if cal_distance(passed_point) < optimal_distance:
            optimal_distance = cal_distance(passed_point)
            optimal_passed_point = passed_point
            optimal_first_point = first_point

        if cal_distance(passed_point) > worst_distance:
            worst_distance = cal_distance(passed_point)
            worst_passed_point = passed_point
            worst_first_point = first_point

    quality = worst_distance / optimal_distance

    if quality > QUALITY_SOLUTION:
        optimal_result = result
        break


plot_figure(1, optimal_result, optimal_passed_point, optimal_first_point)
plot_figure(2, optimal_result, worst_passed_point, worst_first_point)


print('optimal distance is ', optimal_distance)
print('worst distance is ', worst_distance)
print('optimal result is ', optimal_result)
print('quality is ', quality)
print('optimal passed point is ', optimal_passed_point)
print('worst passed point is ', worst_passed_point)
