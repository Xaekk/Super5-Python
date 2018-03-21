import test2 as t
help(t)
##import pymysql
##
##connection = pymysql.connect(host='localhost',
##                             user='root',
##                             password='root',
##                             db='superfive')
##n=[10, 12, 29, 41, 45]
##for index,m in n:
##print(index,m)
##
##
##try:
##    with connection.cursor() as cursor:
##        
##        sql = "INSERT INTO `test` (`num1`, `num2`) VALUES (5, 6)"
##        cursor.execute(sql)
##
##    connection.commit()
##finally:
##    connection.close()

##try:
##    with connection.cursor() as cursor:
##        sql = "select num1,num2 from test"
##        cursor.execute(sql)
##
##        result = cursor.fetchone()
##        print(result)
##        result = cursor.fetchone()
##        print(result)
##        result = cursor.fetchone()
##        print(result)
##        print(result[1])
##
##finally:
##    connection.close()
