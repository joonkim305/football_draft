def linear_reg(df_x, df_y, d):
    import pandas as pd
    import numpy as np

    arr = [[0 for x in range(d + 1)] for y in range(d + 1)]



    for i in range(0, d + 1):
        for j in range(0, d + 1):
            arr[i][j] = sum(df_x ** (i + j))

    arr_inv = np.linalg.inv(arr)

    y_arr = [0 for x in range(d + 1)]

    for i in range(0, d + 1):
        y_arr[i] = sum(df_x ** i * df_y)



    coef = [0 for x in range(d + 1)]

    for i in range(0, d + 1):
        coef[i] = sum(y_arr * arr_inv[:][i])

    return coef

