import tensorflow as tf

state_demention = 5*5 # Latest 5 scope [Numbers]
state_demention += 45 # Perhaps Rate

class Agent:
    def __init__(self):
        self.state = tf.placeholder(tf.float32, [None, state_demention])
        self.reward = tf.placeholder(tf.float32, [None, 1])

        self.a_net = self.built_actor_net()
        self.a_t_net = self.built_actor_net()
        self.c_net = self.built_critic_net()
        self.c_t_net = self.built_critic_net()

    def built_actor_net(self):
        W = tf.Variable(tf.zeros([state_demention, 45]))
        B = tf.Variable(tf.zeros([45]))
        return tf.add(tf.multiply(self.state, W), B)

    def built_critic_net(self):
        W_s = tf.Variable(tf.zeros([state_demention, 1]))
        B_s = tf.Variable(tf.zeros([1]))
        net_s = tf.add(tf.multiply(self.state, W_s), B_s)

        W_a = tf.Variable(tf.zeros([5, 1]))
        B_a = tf.Variable(tf.zeros([1]))
        net_a = tf.add(tf.multiply(self.a_net, W_a), B_a)
        return tf.add(net_s, net_a)