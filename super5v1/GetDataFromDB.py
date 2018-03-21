import pymysql

def getData():
    '''获取全部中奖数据'''
    '''中奖数据'''
    nums = []

    connection = pymysql.connect(host='localhost',
                             user='root',
                             password='root',
                             db='superfive')

    try:
        with connection.cursor() as cursor:

          sql = "select * from nums"
          cursor.execute(sql)

          while True:
              result = cursor.fetchone()
              if result == None:
                  break

              num_map = {
                  'id' : result[0],
                  'year' : result[1],
                  'month' : result[2],
                  'day' : result[3],
                  'num' : []
                  }
              num_map['num'].append(result[4])
              num_map['num'].append(result[5])
              num_map['num'].append(result[6])
              num_map['num'].append(result[7])
              num_map['num'].append(result[8])
              num_map['num'].sort()

              nums.append(num_map)

    finally:
        connection.close()

    return nums

