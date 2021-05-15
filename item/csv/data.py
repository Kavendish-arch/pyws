print("Hello world")
'''
0 
1 train_len
2 test_len
3 rec_len
4 hit
5 precision
6 recall
7 f1_score
'''
import numpy as np 
precision, recall, f1_score = np.loadtxt('data.csv', delimiter=',',usecols=(5,6,7), unpack=True)
pre = np.where(precision > 0)
rec = np.where(recall > 0)
f1 = np.where(f1_score > 0)
print(len(precision[pre]), len(recall[rec]), len(f1_score[f1]))
def pingjia(*a,**k):
    for i in a:
        print("mean = ",np.mean(i), "len = ",len(i))
        print("max = ",np.max(i), "\nmin = ",
        np.min(i), "\nmedian = ", np.median(i))    
        print()
    # print(k)
pingjia(a,b,c)