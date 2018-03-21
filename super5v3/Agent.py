import tensorflow as tf
import numpy as np

state_demention = 5*5 # Latest 5 scope [Numbers]
state_demention += 45 # Perhaps Rate

class Actor:
    def __init__(self):
        self.state = tf.placeholder(tf.float32, [None, state_demention])
        self.reward_ = tf.placeholder(tf.float32, [1])

        self.net = self._build_net()
        self._train_op()

    def set_sess(self, sess):
        self.sess = sess

    def _build_net(self):
        self.w = W = tf.Variable(tf.ones([state_demention, 45]))
        self.b = B = tf.Variable(tf.ones([45]))
        return tf.nn.sigmoid(tf.add(tf.matmul(self.state, W), B))

    def _train_op(self):
        loss = tf.reduce_mean(tf.multiply(self.net* self.reward_))
        self.train_op = tf.train.AdamOptimizer(0.01).minimize(-loss)

    def _pick_nums(self, y):
        '''获取预测号码'''
        out = []
        min_ = np.min(y)
        for _ in range(5):
            for index,y_ in enumerate(y):
                if y_ == max(y):
                    out.append(index+1)
                    y[index] = min_ - 9999
                    break
        return sorted(out)

    def get_action_rate(self, state):
        return self.sess.run(self.net, feed_dict={self.state: [state]})[0]

    def get_action(self, action_rate):
        return self._pick_nums(action_rate)

    def train(self, state, reward):
        # print('W:',self.sess.run(self.w))
        # print('B:',self.sess.run(self.b))
        self.sess.run(self.train_op, feed_dict={self.state:[state], self.reward_:[reward]})

class Critic:
    def __init__(self):
        self.state = tf.placeholder(tf.float32, [None, state_demention])
        self.action = tf.placeholder(tf.float32, [None, 45])
        self.reward_ = tf.placeholder(tf.float32, [1])

        self.net = self._build_net()
        self._train_op()

    def set_sess(self, sess):
        self.sess = sess

    def _build_net(self):
        W_s = tf.Variable(tf.ones([state_demention, 1]))
        B_s = tf.Variable(tf.ones([1]))
        net_s = tf.add(tf.matmul(self.state, W_s), B_s)

        W_a = tf.Variable(tf.ones([45, 1]))
        B_a = tf.Variable(tf.ones([1]))
        net_a = tf.add(tf.matmul(self.action, W_a), B_a)

        y = tf.add(net_s, net_a)
        y = tf.nn.relu(y)
        return y

    def _train_op(self):
        loss = tf.reduce_mean(tf.squared_difference(self.net, self.reward_))
        self.train_op = tf.train.AdamOptimizer(0.01).minimize(-loss)

    def get_reward(self, state, action):
        return self.sess.run(self.net, feed_dict={self.state: [state], self.action:[action]})[0][0]

    def train(self, state, action, reward):
        self.sess.run(self.train_op, feed_dict={self.state: [state], self.action:[action], self.reward_: [reward]})

class Menory:
    def __init__(self, state, action, reward_est, reward_rea):
        self.state = state
        self.action = action
        self.reward_est = reward_est
        self.reward_rea = reward_rea

if __name__ == '__main__':
    actor = Actor()
    print(actor._pick_nums([1,2,3,4,5,6,7,8]))