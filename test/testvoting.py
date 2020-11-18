# voting 的简单实现


from collections import deque, Counter
import os, time

# [1,1][0,1][1,2]
# test_q = [(1, 1), (0, 1), (0, 1), (1, 1), (1, 2)]
test_q = [('nohand', 'nohand'), ('nohand', 'nohand'), ('ok', 'nohand'), ('nohand', 'nohand')]

qsize = 3

predict_q = deque(maxlen=qsize)
res = 0

index = 1
for i in test_q:
    predict_q.append(i)
    print(predict_q)
    # res = Counter(predict_q).most_common(1)
    res = Counter(predict_q).most_common(1)[0][0]
    print(str(index) + ':' + str(res))
    index += 1
