import numpy as np
# Import Data
import GetDataFromDB as gd
data = gd.getData()
data_nums = []
for map_ in data:
    data_nums.append(map_['num'])

# Count the Rate of Each Nums
import RateOfNum as rn
rate = rn.rateOfNumEachTime()
for i,rate_ in enumerate(rate):
    for j,_ in enumerate(rate_):
        rate[i][j] = 1.0/(1+np.exp(-rate[i][j]))
#========== Prepare Configer ==========================
data_num = 5*5 # Latest 5 scope [Numbers]
data_num += 45 # Perhaps Rate

#======== Prepare Training Data =======================
# New Data Nums ( Latest 5 scope )
n_data_nums = []
for index in range(len(data_nums)-4):
    n_data_num = []
    for index_ in range(5):
        for num in data_nums[index + index_]:
            n_data_num.append(num)

    n_data_nums.append(n_data_num)

#Add Rates to Array
for index in range(len(n_data_nums)):
    for rate_ in rate[index+4]:
        n_data_nums[index].append(rate_)

#========== Start Training =============================
# Tools
def nums_2_hot_array(label):
    '''获奖号码 转 hot数组 形式'''
    hot = [0 for _ in range(45)]
    for num in label:
        hot[num-1] = 1
    return hot
def lots_nums_2_hot_array(array):
    '''多期获奖号码 转 多期hot数组 形式'''
    for index,_y in enumerate(array):
        array[index] = nums_2_hot_array(_y)
def pick_nums(y):
    '''获取预测号码'''
    y = y[0]
    out = []
    min_ = np.min(y)
    for _ in range(5):
        index = np.where(y==max(y))[0][0]
        out.append(index+1)
        y[index] = min_
    return sorted(out)
    
#============= Programer ===============================
import tensorflow as tf
from tqdm import trange
x = tf.placeholder(tf.float32, [None, data_num])
W = tf.Variable(tf.zeros([data_num,50]))
b = tf.Variable(tf.ones([50]))
y = tf.add(tf.matmul(x,W), b)
y = tf.sigmoid(y)
y = tf.add(tf.matmul(y,tf.Variable(tf.zeros([50,5]))), tf.Variable(tf.ones([5])))
y = tf.sigmoid(y)
y = tf.add(tf.matmul(y,tf.Variable(tf.zeros([5,45]))), tf.Variable(tf.ones([45])))
y = tf.sigmoid(y)
y_ = tf.placeholder(tf.float32, [None, 45])

cross_entropy = -tf.reduce_sum(y_*tf.log(y))
train_step = tf.train.GradientDescentOptimizer(0.01).minimize(cross_entropy)

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())

    train_x = n_data_nums[:-1]
    train_y = data_nums[5:]
    for s in range(1000):
        print('循环索引:', s)
        for i in range(int(len(train_x)/20)):
            from_ = i*20
            to_ = i*20+20
            if to_ < len(train_x):
                scope_x = train_x[from_ : to_]
                scope_y = train_y[from_ : to_]
            else:
                scope_x = train_x[from_ :]
                scope_y = train_y[from_ :]
            lots_nums_2_hot_array(scope_y)
            sess.run(train_step, feed_dict={x: scope_x, y_: scope_y})

    print('W:', '\n',sess.run(W))
    print('b:', '\n',sess.run(b))
    print('精度测试:', end='')
    print(data_nums[-1], pick_nums(sess.run(y, feed_dict={x: [n_data_nums[-2]]})))

    # Prediction
    print('预测号码:', pick_nums(sess.run(y, feed_dict={x: [n_data_nums[-1]]})))

input('\n任意输入以结束 ...')
