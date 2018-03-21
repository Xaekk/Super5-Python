'''
返回值：rateOfNum(期数索引--零开始, 索引期每个对应号码已中概率,i.e. 每期45个概率)
使用方法:rateOfNum[索引-1]
'''
def rateOfNumEachTime():
    '''号码频率数组'''
    rateOfNum = []

    '''提取数据'''
    numArray = getData()

    '''初始化每期每个号码频次'''
    ratenumOfNum = []
    for i in range(45):
        ratenumOfNum.append(0)

    '''每期循环'''
    for nums in numArray:
        '''每期频次'''
        for num in nums:
            ratenumOfNum[num-1] += 1

        '''每期总频次'''
        totalNum = 0
        for am in ratenumOfNum:
            totalNum += am

        '''每期总频率'''
        rateOfNumEachTime = []
        for i in range(45):
            rateOfNumEachTime.append(float(0))

        for index,num in enumerate(ratenumOfNum):
            rateOfNumEachTime[index] = float(num)/float(totalNum)

        '''每期频率加入数组'''
        rateOfNum.append(rateOfNumEachTime)

    return rateOfNum

'''从数据库中提取数据'''
def getData():
    '''数据库'''
    '''初始化数据库'''
    import pymysql
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='root',
                                 db='superfive')

    '''数据库'''
    '''号码数组'''
    numArray = []
    try:
        '''从数据库中提取数据'''
        with connection.cursor() as cursor:
            now_id = 0
            sql = "select num1,num2,num3,num4,num5 from nums"
            cursor.execute(sql)
            while True:
                now_id += 1
                result = cursor.fetchone()
                if result == None:
                    break
                #TODO : Progress Bar
                
                nums = []
                for re in result:
                    nums.append(re)
                numArray.append(nums)
        return numArray
    finally:
        connection.close()
