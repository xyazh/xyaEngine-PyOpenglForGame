import time,numpy,math

m = 1
t1 = time.time()
for i in range(5000000):
    i*0.10014141412414
print(time.time()-t1)

m = 1
t1 = time.time()
for i in range(5000000):
    i*0.1
print(time.time()-t1)

