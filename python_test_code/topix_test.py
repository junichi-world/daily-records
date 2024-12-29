import requests
from bs4 import BeautifulSoup

#現在時点での配当利回りを取得する
#その上でどこまで評価されるかを考える
url = 'https://finance.yahoo.co.jp/stocks/ranking/dividendYield?market=all&term=daily&page=1'
res = requests.get(url)

#soup = BeautifulSoup(res.text)
#特定の要素のみを取り出す
print(res.text)
#BeautifulSoupでは取り出せない
print("stop")