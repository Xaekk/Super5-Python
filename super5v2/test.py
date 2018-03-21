import numpy as np
a = np.random.randn(10)
print(a)
print(max(a))
print(np.where(a==max(a))[0][0])
