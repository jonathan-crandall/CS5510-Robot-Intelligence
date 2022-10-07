# Changing things
from math import inf, radians, sin, cos, sqrt
import random

x_goal = 1.2
y_goal = 0.8
z_goal = 0.5

t_1_int = t_1 = radians(0)
d_2_int = d_2 = 0.2
d_3_int = d_3 = 0.3
t_4_int = t_4 = radians(-90)
t_5_int = t_5 = radians(90)

# Constant
t_6 = radians(40)
d_6 = 0.2

# Arbitrary
d_1 = 3
threshold = 0.0001

x = (
    (cos(t_1) * cos(t_4) * sin(t_5) * d_6)
    - (sin(t_1) * cos(t_5) * d_6)
    - (sin(t_1) * d_3)
)
y = (
    (sin(t_1) * cos(t_4) * sin(t_5) * d_6)
    + (cos(t_1) * cos(t_5) * d_6)
    + (cos(t_1) * d_3)
)
z = (sin(t_4) * sin(t_5) * d_6) + d_1 + d_2


def dist(x1, x2, y1, y2, z1, z2):
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2)


n = 1
while n > 0:
    change_to_beat = inf
    dist_to_beat = inf
    solution = tuple()
    factor = dist(x, x_goal, y, y_goal, z, z_goal) * 2

    # Please dont look to close at this code it needs to be super refactored
    for i in range(100 + int(100 * factor)):
        print(f"running {n}:{i} at {factor=}")
        t_1_tmp = t_1 - (random.random() - 0.5) * factor
        t_4_tmp = t_4 - (random.random() - 0.5) * factor
        t_5_tmp = t_5 - (random.random() - 0.5) * factor
        d_2_tmp = d_2 - (random.random() - 0.5) * factor
        d_3_tmp = d_3 - (random.random() - 0.5) * factor

        x_tmp = (
            (cos(t_1_tmp) * cos(t_4_tmp) * sin(t_5_tmp) * d_6)
            - (sin(t_1_tmp) * cos(t_5_tmp) * d_6)
            - (sin(t_1_tmp) * d_3_tmp)
        )
        y_tmp = (
            (sin(t_1_tmp) * cos(t_4_tmp) * sin(t_5_tmp) * d_6)
            + (cos(t_1_tmp) * cos(t_5_tmp) * d_6)
            + (cos(t_1_tmp) * d_3_tmp)
        )
        z_tmp = (sin(t_4_tmp) * sin(t_5_tmp) * d_6) + d_1 + d_2_tmp

        change = sum(
            [
                abs(t - i)
                for i, t in zip(
                    (t_1_int, t_4_int, t_5_int, d_2_int, d_3_int),
                    (t_1_tmp, t_4_tmp, t_5_tmp, d_2_tmp, d_3_tmp),
                )
            ]
        )

        d_goal = dist(x_goal, x, y_goal, y, z_goal, z)
        d_tmp = dist(x_goal, x_tmp, y_goal, y_tmp, z_goal, z_tmp)
        if d_goal > d_tmp and change < change_to_beat and d_tmp < dist_to_beat:
            print("Better solution found: ", n)
            solution = (
                t_1_tmp,
                t_4_tmp,
                t_5_tmp,
                d_2_tmp,
                d_3_tmp,
                x_tmp,
                y_tmp,
                z_tmp,
            )

    print(solution[-3:], change, end="\r")

    if not solution:
        print(f"No solution found for iter {n}")
        continue

    t_1_tmp, t_4_tmp, t_5_tmp, d_2_tmp, d_3_tmp, x_tmp, y_tmp, z_tmp = solution

    if (
        abs(x_tmp - x_goal) < threshold
        and abs(y_tmp - y_goal) < threshold
        and abs(z_tmp - z_goal) < threshold
    ):
        print("success\n")
        print(f"Final XYZ {x_tmp:.4}, {y_tmp:.4}, {z_tmp:.4}")
        print(
            f"Final thetas {t_1_tmp=:.4} {t_4_tmp=:.4} {t_5_tmp=:.4} {d_2_tmp=} {d_3_tmp=}"
        )
        change = sum(
            [
                abs(initial - temporary)
                for initial, temporary in zip(
                    (t_1_int, t_4_int, t_5_int, d_2_int, d_3_int),
                    (t_1_tmp, t_4_tmp, t_5_tmp, d_2_tmp, d_3_tmp),
                )
            ]
        )
        print(f"Change: {change}")
        print("num iter {}".format(n))
        break

    if dist(x_goal, x, y_goal, y, z_goal, z) < dist(
        x_goal, x_tmp, y_goal, y_tmp, z_goal, z_tmp
    ):
        pass
    else:
        t_1 = t_1_tmp
        t_4 = t_4_tmp
        t_5 = t_5_tmp
        d_2 = d_2_tmp
        d_3 = d_3_tmp

        x = x_tmp
        y = y_tmp
        z = z_tmp

    n += 1
