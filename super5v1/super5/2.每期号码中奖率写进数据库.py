
'''号码频率数组'''
rateOfNum = []

def rateOfNumEachTime(numArray):
    global rateOfNum

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
                print('picking',now_id)
                nums = []
                for re in result:
                    nums.append(re)
                numArray.append(nums)

    return numArray

    finally:
        connection.close()

'''将概率写进数据库'''
def updateRate():
    '''数据库'''
    '''初始化数据库'''
    import pymysql
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='root',
                                 db='superfive')

    try:
        '''概率写入数据库'''
        with connection.cursor() as cursor:
            for index,rate in enumerate(rateOfNum):
                print("writing... id = ", index+1)
                sql = "UPDATE nums SET"
                
                for index2,num in enumerate(numArray[index]):
                    sql = sql + " rate"+str(index2+1)+" = "+str(rate[num-1]) +","

                sql = sql[:-1]
                sql = sql + " WHERE `id` = '"+str(index+1) +"'"
                cursor.execute(sql)
            connection.commit()
    finally:
        connection.close()
