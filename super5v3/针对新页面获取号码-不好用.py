import urllib3 as ul3
from bs4 import BeautifulSoup

array = []

for day in range(30):
    print('Now is {}'.format(day))
    map = {'date':'2018-02-{}'.format(day)}
    data = {"SelectedDay": '2018-02-{}'.format(day)}

    url = 'https://www.maltco.com/super/results/do_results.php'
    http = ul3.PoolManager()
    r = http.request('POST', url=url, fields=data)
    html_doc = r.data

    html_doc = BeautifulSoup(html_doc, 'html.parser')

    map['Draw'] = html_doc.find(attrs={'id':'draw_holder'}).text

    nums = html_doc.find_all(attrs={'id':'number_style'})
    for i in range(len(nums)):
        nums[i] = nums[i].text.replace('\n\t\t', '')
    map['Nums'] = nums
    array.append(map)

for a in array:
    print(a)