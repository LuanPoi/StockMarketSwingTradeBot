import numpy as np

from pandas import Series


def average(x: Series, h: int) -> np.ndarray:
    # x : time serie data
    # h : number of future predictions
    # equation : Ŷ = (Y1 + ... + Yt) / t
    result = np.full(h, x.mean())
    return Series(result)


def seasonal_naive(x: Series, s: int, h: int) -> np.ndarray:
    # x : time serie data
    # s : seasonal period
    # h : number of future predictions
    # equation : Ŷt+h|t = Yt+h-s(k+1), k = (h-1)/s
    tail = x.tail(s).values
    result = []
    for t in range(h):
        result.append(tail[t % s])
    return Series(np.array(result))


def drift(x: Series, h: int) -> np.ndarray:
    # x : time serie data
    # h : number of future predictions
    # equation : Ŷt+h|t = Yt + h * ((Yt - Y1) / (t - 1))
    diffRate = (x.get(x.last_valid_index()) - x.get(x.first_valid_index())) / (len(x.values) - 1)
    result = []
    for t in range(h):
        result.append(x.get(x.last_valid_index()) + ((t + 1) * diffRate))
    return Series(np.array(result))
