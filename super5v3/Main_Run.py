import Agent
from enviorment import Environment
import tensorflow as tf
import numpy as np
from tqdm import tqdm

def run():
    env = Environment()
    actor = Agent.Actor()
    critic = Agent.Critic()
    menories = []

    with tf.Session() as sess:
        sess.run(tf.global_variables_initializer())
        actor.set_sess(sess)
        critic.set_sess(sess)

        # for index in range(10000+1):
        index = 0
        while True:
            print('Scope:',index)
            index += 1
            state, result, id = env.get_state_result()
            random_str = ''
            if np.random.rand()<0.6:
                action_rate = actor.get_action_rate(state=state)
                action = actor.get_action(action_rate=action_rate)
            else:
                random_str = '【by random】'
                action = np.random.randint(1,45,5)
                action_rate = [0 for _ in range(45)]
                for i in range(5):
                    action_rate[action[i]-1] = 1
            reward_est = critic.get_reward(state=state, action=action_rate)
            reward_rea = env.get_reward(estimated_nums=action, reality_nums=result)
            menories.append(Agent.Menory(state=state, action=action_rate, reward_est=reward_est, reward_rea=reward_rea))
            if index%10 == 0:
                print('action:', action, \
                      '** result', result, \
                      '** reward_rea:', reward_rea,\
                      '** reward_est:', reward_est, random_str)
            if index%100 == 0 and index!=0:
                for menory in tqdm(menories):
                    if menory.reward_rea>0:
                        actor.train(state=menory.state, reward=menory.reward_est)
                        critic.train(state=menory.state, action=menory.action, reward=menory.reward_rea)
                menories = []

        latest_action = actor.get_action(state=env.get_latest_state())
        print('预估最新号码：', latest_action)

if __name__ == '__main__':
    run()
    input('Press anykey to exit...')