from selenium import webdriver  # selenium君からwebdriverをインポート
from selenium.webdriver.common.by import By
from time import sleep

#ここに答えを入れる
text_data = []

driver = webdriver.Chrome()  # webdriverをChromeのヤツで使います。

url = "https://finance.yahoo.co.jp/stocks/ranking/dividendYield?market=all&term=daily&page="

def collect_divide():
    #class_names = driver.find_elements(By.CLASS_NAME, "RankingTable__row__1Gwp")
    #3,7,11,15,19,23,27,...など4つの間隔ごとに配当がある
    #どこに該当するか
    loc_num = 4

    class_divides = driver.find_elements(By.CLASS_NAME, "StyledNumber__value__3rXW")
    sum_count = int(len(class_divides) / loc_num)

    for i in range(sum_count):
        res = class_divides[4*i + 3].text
        text_data.append(res)

def open_url(num):
    for i in range(num):
        wait = driver.implicitly_wait(3)
        driver.get(url + str(i+1))
        collect_divide()

#最終的な答えを出力する
def output_ans():
    for i, text in enumerate(text_data):
        print(i+1, text)

#main関数
def main():
    page_number = 10
    open_url(page_number)
    output_ans()

main()