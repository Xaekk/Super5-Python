import tensorflow as tf
import numpy as np
import GetDataFromDB as gd

#Training Params
batch_size = 5
show_step = 100
epoch = 25

#Network Params
#数据量
data_num  = 5  #上期号码
data_num += 45 #上期全频率
data_num += 1  #上期均值
data_num += 1  #近5期均值
data_num += 1  #上期奇偶比
data_num += 4  #上期间隔差

weights = {
    'gen_hidden1' : tf.Variable(tf.random_normal([data_num, 25])),
    'gen_hidden2' : tf.Variable(tf.random_normal([25, 5])),
    'disc_hidden1' : tf.Variable(tf.random_normal([5,10])),
    'disc_hidden2' : tf.Variable(tf.random_normal([10,1]))
    }
biases = {
    'gen_hidden1' : tf.Variable(tf.zeros([25])),
    'gen_hidden2' : tf.Variable(tf.zeros([5])),
    'disc_hidden1' : tf.Variable(tf.zeros([10])),
    'disc_hidden2' : tf.Variable(tf.zeros([1]))
    }

#Generator
def generator(x):
    x = tf.matmul(x, weights['gen_hidden1'])
    x = tf.add(x, biases['gen_hidden1'])
    x = tf.nn.relu(x)
    x = tf.matmul(x, weights['gen_hidden2'])
    x = tf.add(x, biases['gen_hidden2'])
    x = tf.nn.sigmoid(x)
    return x

#Discriminator
def discriminator(x):
    x = tf.matmul(x, weights['disc_hidden1'])
    x = tf.add(x, biases['disc_hidden1'])
    x = tf.nn.relu(x)
    x = tf.matmul(x, weights['disc_hidden2'])
    x = tf.add(x, biases['disc_hidden2'])
    x = tf.nn.sigmoid(x)
    return x

#Sigmoid Method
import math
def sigmoid(x):
    return 1 / (1 + math.exp(-x))    

#Build Networks
#Network Input
gen_input = tf.placeholder(tf.float32, shape = [None, data_num], name = 'Datas')
disc_input = tf.placeholder(tf.float32, shape = [None, 5], name = 'Disc_input')

'''#Build Targets
#True:1 False:0
gen_target = tf.placeholder(tf.int32, shape = [None], name = 'Gen_target')
disc_target = tf.placeholder(tf.int32, shape = [None], name = 'Disc_target')'''

#Build Generator Network
gen_sample = generator(gen_input)

#Build 2 Discriminator Networks
disc_fake = discriminator(gen_sample)
disc_real = discriminator(disc_input)
'''disc_concat = tf.concat([disc_real, disc_fake], axis=0)'''

#Build the stacked generator/discriminator
'''stacked_gen = discriminator(gen_sample)'''

#Build Loss
'''disc_loss = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(logits=disc_concat, labels=disc_target))
gen_loss = tf.reduce_mean(tf.nn.sparse_softmax_cross_entropy_with_logits(logits=stacked_gen, labels=gen_target))'''
gen_loss = -tf.reduce_mean(tf.log(disc_fake))
disc_loss = -tf.reduce_mean(tf.log(disc_real) + tf.log(1. - disc_fake))

#Build Optimizers
optimizer_gen = tf.train.AdamOptimizer(learning_rate = 0.001)
optimizer_disc = tf.train.AdamOptimizer(learning_rate = 0.001)

#Generator Network Variables
gen_vars = [weights['gen_hidden1'], weights['gen_hidden2'],
            biases['gen_hidden1'], biases['gen_hidden2']]
#Discriminator Network Variables
disc_vars = [weights['disc_hidden1'], weights['disc_hidden2'],
             biases['disc_hidden1'], biases['disc_hidden2']]

#Create training operations
train_gen = optimizer_gen.minimize(gen_loss, var_list=gen_vars)
train_disc = optimizer_disc.minimize(disc_loss, var_list=disc_vars)

#Initialize the variables
init = tf.global_variables_initializer()

#Start Training
with tf.Session() as sess:
    sess.run(init)

    #获取总数据
    data = gd.getData()
    #每期频率数据
    import RateOfNum as rn
    rate = rn.rateOfNumEachTime()

    for epoch_index in range(epoch):
        #for-in batch:batch_size+1
        for index in range(0, len(data)-1):
            #准备数据(最后一个数据为被预测号码对比的真实号码)
            batch_data = []
            batch_rate = []
            if len(data)-index < batch_size:
                batch_data = data[index : ]
                batch_rate = rate[index : ]
            else:
                batch_data = data[index : index+batch_size]
                batch_rate = rate[index : index+batch_size]
                
            #上期号码[]
            latest = batch_data[-2]['num']
            #上期号码当前期全频率
            latest_rate = batch_rate[-2]
            for i in range(len(latest_rate)):
                latest_rate[i] = sigmoid(latest_rate[i])
            #上期号码总值
            total_latest = 0
            for num in latest:
                total_latest += num
            #上期号码均值
            mean_latest = float(total_latest)/5
            #最近5期均值
            total_five = 0
            for five_nums in batch_data[:-1]:
                for num in five_nums['num']:
                    total_five += num
            mean_five = float(total_five)/25
            #上期奇偶比
            avb = 0
            amount_a = 0
            amount_b = 0
            for num in latest:
                if num%2 == 0:
                    amount_b += 1
                else:
                    amount_a += 1
            if amount_a == 0 : amount_a = 1
            if amount_b == 0 : amount_b = 1
            avb = float(amount_a)/float(amount_b)
            #上期间隔差
            min_sum = []
            min_sum.append(latest[4]-latest[3])
            min_sum.append(latest[3]-latest[2])
            min_sum.append(latest[2]-latest[1])
            min_sum.append(latest[1]-latest[0])

            mean_latest = [mean_latest]
            total_five = [total_five]
            avb = [avb]

            #总数据
            num_refer = np.concatenate([latest, latest_rate,
                                        mean_latest, total_five,
                                        avb, min_sum], axis=0)

            '''#辨别目标值
            batch_disc_y = np.concatenate(
                [np.ones([batch_size]), np.zeros([batch_size])], axis=0)
            #生成目标值
            batch_gen_y = np.ones([batch_size])'''
            
            #Trainning
            feed_dict = {gen_input:[num_refer], disc_input:[batch_data[-1]['num']]}
            ''',disc_target:batch_disc_y, gen_target:batch_gen_y}'''

            _, _, gl, dl = sess.run([train_gen, train_disc,
                                     gen_loss, disc_loss],
                                    feed_dict=feed_dict)
            if index % show_step == 0 or index == 1:
                print('Epoch %i -- Step %i: Generator Loss: %f, Discriminator Loss: %f' % (epoch_index, index, gl, dl))

#输出最终预测
    #最新期号码[]
    latest = data[-1]['num']
    #最新期号码当前期全频率
    latest_rate = rate[-1]
    for i in range(len(latest_rate)):
        latest_rate[i] = sigmoid(latest_rate[i])
    #最新期号码总值
    total_latest = 0
    for num in latest:
        total_latest += num
    #最新期号码均值
    mean_latest = float(total_latest)/5
    #最近5期均值
    total_five = 0
    for five_nums in batch_data[-5:-1]:
        for num in five_nums['num']:
            total_five += num
    mean_five = float(total_five)/25
    #最新期奇偶比
    avb = 0
    amount_a = 0
    amount_b = 0
    for num in latest:
        if num%2 == 0:
            amount_b += 1
        else:
            amount_a += 1
    if amount_a == 0 : amount_a = 1
    if amount_b == 0 : amount_b = 1
    avb = float(amount_a)/float(amount_b)
    #最新期间隔差
    min_sum = []
    min_sum.append(latest[4]-latest[3])
    min_sum.append(latest[3]-latest[2])
    min_sum.append(latest[2]-latest[1])
    min_sum.append(latest[1]-latest[0])

    mean_latest = [mean_latest]
    total_five = [total_five]
    avb = [avb]

    #总数据
    num_refer = np.concatenate([latest, latest_rate,
                                mean_latest, total_five,
                                avb, min_sum])
    #预测值
    pre_nums = sess.run(gen_sample, feed_dict = {gen_input:[num_refer]})

    #打印预测值
    print(pre_nums)





    
