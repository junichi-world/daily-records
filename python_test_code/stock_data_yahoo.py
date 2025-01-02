from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep

import numpy as np
import matplotlib.pyplot as plt
import csv
from datetime import datetime
import os

#ここではクラスを作成する
#その後、取得したデータをヒストグラムで表す
class Yahoo_Web():
    #取得するデータのページ数を決める
    def __init__(self, save_path, url, page_num, name):
        self.save_path = save_path
        self.url = url
        self.content_word = "StyledNumber__value__3rXW"
        self.content_loc = 4
        self.page_num = page_num
        self.name = name
        self.result = []
        self.driver = webdriver.Chrome()

    #ページ数が範囲内かどうか
    def check_page(self):
        if self.page_num < 1:
            self.page_num = 1
        elif self.page_num > 64:
            self.page_num = 64
    
    #データを取って来る
    def get_web_data(self):
        divides = self.driver.find_elements(By.CLASS_NAME, self.content_word)
        count = int(len(divides) / self.content_loc)
        for i in range(count):
            res = divides[self.content_loc*i + 3].text
            #ここの数字のプラスは除いて、数値にする
            self.result.append(float(res.replace('+', '')))

    #webを開いてデータを取得する
    def open_web(self):
        #数のチェック
        self.check_page()
        #ページごとに
        for i in range(self.page_num):
            wait = self.driver.implicitly_wait(3)
            self.driver.get(self.url + str(i+1))
            self.get_web_data()
    
    #重複をなくし、整列する
    def remove_duplicates(self, lst):
        new_list = list(set(lst))
        sorted_list = sorted(new_list)
        return sorted_list

    #数がいくつあるのかを数える
    def count_num(self, rounded_result):
        #この中の重複をなくす
        num_list = self.remove_duplicates(rounded_result)
        #数がいくつあるのかを数える
        count_list = []
        for num in num_list:
            count = 0
            for rou in rounded_result:
                if num == rou:
                    count += 1
            count_list.append([num, count])
        return count_list

    #カウントする関数
    def count_divide(self):
        rounded_result = []
        for res in self.result:
            rounded_result.append(round(res, 1))
        return self.count_num(rounded_result)

    #テキストファイルで結果を分類したものを保存する
    def write_text(self):
        #保存する前に分類分けをする
        #0.1ずつで分けてカウントできないか？
        count_list = self.count_divide()
        # 現在時刻を取得
        dt = datetime.now()
        # datetime型から文字列に変換
        datetime_str = self.save_path + "\\" + dt.strftime("%Y-%m-%d") + "_" + self.name +".csv"
        #csvファイル
        with open(datetime_str, 'w', newline="") as f:
            writer = csv.writer(f)
            writer.writerows(count_list)

    #ヒストグラム画像を保存する
    def save_hist(self):
        #少数点を1桁にする
        rounded_result = []
        for res in self.result:
            rounded_result.append(round(res, 1))
        
        divide_np = np.array(rounded_result)
        # ヒストグラムをプロットする
        plt.hist(divide_np, bins = 50)
        # タイトルとラベルを入れる
        plt.title(self.name + '_freqency')
        plt.xlabel(self.name)
        plt.ylabel('freqency')
        plt.grid(True)
        # 現在時刻を取得
        dt = datetime.now()
        # datetime型から文字列に変換
        datetime_str = dt.strftime("%Y-%m-%d")
        #ヒストグラムをpng形式で保存する
        plt.savefig(self.save_path + "\\" + datetime_str + '_' + self.name + '.png')
        plt.close()
    
    #散布図画像を保存する
    def save_scatter(self):
        x = []
        y = []
        count_list = self.count_divide()

        for count in count_list:
            x.append(count[0])
            y.append(count[1])

        np_x = np.array(x)
        np_y = np.array(y)

        plt.scatter(x, y)
        plt.title(self.name + ' vs freqency', fontsize=20) # タイトル
        plt.xlabel(self.name, fontsize=20) # x軸ラベル
        plt.ylabel("freqency", fontsize=20) # y軸ラベル
        plt.grid(True) # 目盛線の表示

        # 現在時刻を取得
        dt = datetime.now()
        # datetime型から文字列に変換
        datetime_str = dt.strftime("%Y-%m-%d")
        #ヒストグラムをpng形式で保存する
        plt.savefig(self.save_path + "\\" + datetime_str + '_' + self.name + '.png')
        plt.close()

def make_save_folder():
    # 現在時刻を取得
    dt = datetime.now()
    # datetime型から文字列に変換
    datetime_str = dt.strftime("%Y-%m-%d")
    date_path = './' + datetime_str
    if os.path.isdir(date_path):
        pass
    else:
        os.makedirs(date_path)
    return date_path

#main関数
def main():
    #出力した散布図、ヒストグラムの画像を保存する
    date_path = make_save_folder()
    #perのデータを収集する
    per_url = "https://finance.yahoo.co.jp/stocks/ranking/lowPer?market=all&term=daily&page="
    per_num = 60
    per_name = "per"
    per_instance = Yahoo_Web(date_path, per_url, per_num, per_name)
    per_instance.open_web()
    per_instance.write_text()
    per_instance.save_scatter()

    #pbrのデータを収集する
    pbr_url = "https://finance.yahoo.co.jp/stocks/ranking/lowPbr?market=all&term=daily&page="
    pbr_num = 60
    pbr_name = "pbr"
    pbr_instance = Yahoo_Web(date_path, pbr_url, pbr_num, pbr_name)
    pbr_instance.open_web()
    pbr_instance.write_text()
    #pbr_instance.save_hist()
    pbr_instance.save_scatter()

    #配当利回り
    divide_url = "https://finance.yahoo.co.jp/stocks/ranking/dividendYield?market=all&term=daily&page="
    divide_num = 60
    divide_name = "divide"
    divide_instance = Yahoo_Web(date_path, divide_url, divide_num, divide_name)
    divide_instance.open_web()
    divide_instance.write_text()
    #divide_instance.save_hist()
    divide_instance.save_scatter()

#処理
if __name__ == '__main__':
    main()
    print("per pbr divie Done")
