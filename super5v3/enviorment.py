import GetDataFromDB
from RateOfNum import rateOfNumEachTime
import numpy as np

class Environment:
    def __init__(self):
        self.Data = GetDataFromDB.getData()
        self.rateET = rateOfNumEachTime()
        self.nums = None # 全部号码
        self.n_data_nums = None # n_data_nums 格式 [当前期-4，当前期-3，当前期-2，当前期-1，当前期，当前各号码出现频率]

        self._pre()

    def _pre(self):
        self.nums = []
        for data in self.Data:
            self.nums.append(data['num'])

        # n_data_nums 格式 [当前期-4，当前期-3，当前期-2，当前期-1，当前期，当前各号码出现频率]
        n_data_nums = []
        for index in range(len(self.nums) - 4):
            n_data_num = []
            for index_ in range(5):
                for num in self.nums[index + index_]:
                    n_data_num.append(num)

            n_data_nums.append(n_data_num)

        # Add Rates to Array
        for index in range(len(n_data_nums)):
            for rate_ in self.rateET[index + 4]:
                n_data_nums[index].append(rate_)
        self.n_data_nums = n_data_nums

    def get_state_result(self):
        '''
        获得 状态 & 结果
        :return:状态, 结果, 数据库id
        '''
        int = np.random.randint(0, len(self.n_data_nums)-1)
        return self.n_data_nums[int], self.nums[int+5], int+6

    def get_reward(self, estimated_nums, reality_nums):
        '''
        比较获得 奖励
        :param estimated_nums:预测号码
        :param reality_nums:实际号码
        :return:奖励
        '''
        reward = -400
        for e_n in estimated_nums:
            for r_n in reality_nums:
                if e_n == r_n:
                    reward += 200
        return reward

    def get_latest_state(self):
        return self.n_data_nums[-1]

if __name__ == '__main__':
    env = Environment()
    state, nums, i = env.get_state_result()
    print(state,'\n', nums, i)
    print(env.get_latest_state())