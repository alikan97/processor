import math
from sklearn.linear_model import LinearRegression
import numpy as np

def pythag_distance(pt1, pt2):
    """
    Calculates the pythagoras distance between two pts
    """
    a = (pt2[0] - pt1[0]) ** 2
    b = (pt2[1] - pt1[1]) ** 2
    return math.sqrt(a + b) #c2 = a2 + b2

def local_min_max(pts):
    """
    Finds the local min & values of a given list of Closing prices
    Loops through the pts list, if current point is greater than next point and previous point, append to local max
    """
    local_min = []
    local_max = []
    
    prev_pts = [(0, pts[0]), (1, pts[1])]

    for i in range(1, len(pts) - 1):
        append_to = ''
        if pts[i-1] > pts[i] < pts[i+1]:
            append_to = 'min'
        elif pts[i-1] < pts[i] > pts[i+1]:
            append_to = 'max'
        if append_to:
            if local_min or local_max:
                prev_distance = pythag_distance(prev_pts[0], prev_pts[1]) * 0.5
                curr_distance = pythag_distance(prev_pts[1], (i, pts[i]))
                if curr_distance >= prev_distance:
                    prev_pts[0] = prev_pts[1]
                    prev_pts[1] = (i, pts[i])
                    if append_to == 'min':
                        local_min.append((i, pts[i]))
                    else:
                        local_max.append((i, pts[i]))
            else:
                prev_pts[0] = prev_pts[1]
                prev_pts[1] = (i, pts[i])
                if append_to == 'min':
                    local_min.append((i, pts[i]))
                else:
                    local_max.append((i, pts[i]))
    return local_min, local_max

def regression_coefficient(pts):
    """
    Use a simple linear regression model to find line of best fit & y intercept
    """
    X = np.array([pt[0] for pt in pts])
    Y = np.array([pt[1] for pt in pts])

    X = X.reshape(-1,1)

    model = LinearRegression()
    model.fit(X, Y)
    return model.coef_[0], model.intercept_

def get_support_resistance(closing_prices):
    """ Gets the support and resistance for a symbol """
    local_min, local_max = local_min_max(closing_prices)

    local_min_slope, local_min_intercept = regression_coefficient(local_min) 
    local_max_slope, local_max_intercept = regression_coefficient(local_max) 

    support = (local_min_slope * np.array(closing_prices.index)) + local_min_intercept
    resistance = (local_max_slope * np.array(closing_prices.index)) + local_max_intercept

    return support, resistance