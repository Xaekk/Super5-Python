import urllib3 as ul3
from bs4 import BeautifulSoup
from tqdm import tqdm
import datetime
import pymysql

#Process Bar Lengh
bar_lengh = 60
#all data
nums_data = []

connection = pymysql.connect(host = 'localhost',
                             user = 'root',
                             password = 'root',
                             db = 'superfive')
try:
    with connection.cursor() as cursor:
        sql = "SELECT `year`, `month`, `day` FROM nums WHERE id = (SELECT MAX(`id`) FROM nums)"
        cursor.execute(sql)
        result = cursor.fetchone()

        y_db = result[0]
        m_db = result[1]
        d_db = result[2]
finally:
    connection.close()

time = datetime.datetime.now()
step = 0
for y in range(y_db, time.year+1):
    for m in range(m_db, 13):
        for d in range(d_db+1, 32):
            step += 1
        d_db = 0
    m_db = 1
if step == 0:
    step = 1

print('Getting Data from Website...')
with tqdm(total=step+1, ncols=bar_lengh) as pbar:
    for y in range(y_db, time.year+1):
        for m in range(m_db, 13):
            for d in range(d_db+1, 32):
                #Proccess Bar
                pbar.update(1)
                
                year = y
                month = m
                day = d

                #super5 numbers
                nums = []

                #numbers map
                num_map = {
                    'year' : year,
                    'month' : month,
                    'day' : day,
                    'nums' : nums
                    }

                ul3.disable_warnings()#Disable the Warning of BeautifulSoup
                url = 'https://www.maltco.com/super/results_draws_dec.php?year='+str(year)+'&month='+str(month)+'&day='+str(day)

                http = ul3.PoolManager()
                r = http.request('GET', url)
                html_doc = r.data

                soup = BeautifulSoup(html_doc, "html.parser")

                def add_nums(num_str):
                    #Add Numbers to Array
                    try:
                        nums.append(int(num_str))
                    except ValueError:
                        pass

                for elem_td in soup.find_all('td'):
                    if elem_td.attrs.get('width', False):
                        width = elem_td.attrs['width']
                        if width == '44':
                            add_nums(elem_td.string.strip())
                        elif width == '43':
                            add_nums(elem_td.string.strip())
                        elif width == '31':
                            add_nums(elem_td.div.strong.string.strip())

                nums.sort()

                if len(nums) == 5:
                    nums_data.append(num_map)

            d_db = 0
        m_db = 1

connection = pymysql.connect(host = 'localhost',
                             user = 'root',
                             password = 'root',
                             db = 'superfive')
try:
    with connection.cursor() as cursor:
        print('Writing into Database...')
        for nums_map in tqdm(nums_data, ncols=bar_lengh):
            value = str(nums_map['year'])+','+str(nums_map['month'])+','+str(nums_map['day'])+','+str(nums_map['nums'][0])+','+str(nums_map['nums'][1])+','+str(nums_map['nums'][2])+','+str(nums_map['nums'][3])+','+str(nums_map['nums'][4])
            sql = """INSERT INTO `nums` (`year`, `month`, `day`, `num1`, `num2`, `num3`, `num4`, `num5`) VALUES ("""+value+""")"""
               
            cursor.execute(sql)
            connection.commit()
        print('Done!')
        input('Press any key to continue...')
finally:
    connection.close()
