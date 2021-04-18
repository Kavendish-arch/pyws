'''
返回p1和p2的皮尔逊相关系数
prefs是一个二维矩阵字典，如下图所示
    （名字，    电影）
              movie1   movie2
       p1      4.5      5.0
       p2      3.0      1.5
'''
from math import sqrt


def simPearson(prefs, p1, p2):
    #得到双方都曾评价过得物品列表
    si={}
    for item in prefs[p1]:
        for item in prefs[p2]:
            si[item] = 1

    #得到列表元素的个数
    n = len(si)

    #如果两者没有共同之处，则返回1
    if n == 0: return 1

    #对所有偏好求和
    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])

    #求平方和
    sum1Sq = sum([pow(prefs[p1][it], 2) for it in si])
    sum2Sq = sum([pow(prefs[p2][it], 2) for it in si])

    #求乘积之和
    pSum = sum([prefs[p1][it] * prefs[p2][it] for it in si])

    #计算皮尔逊评价值
    num = pSum - (sum1 * sum2) / n
    den = sqrt((sum1Sq-pow(sum1, 2) / n) * (sum2Sq - pow(sum2, 2) / n))

    if den == 0: return 0

    r = num / den

    return r
