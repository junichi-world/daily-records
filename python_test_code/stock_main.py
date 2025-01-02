import stock_index as STI
from datetime import datetime
import os

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
    per_instance = STI.STOCK_ELEMENT(date_path, per_url, per_num, per_name)
    per_instance.open_web()
    per_instance.write_text()
    per_instance.save_scatter()

    #pbrのデータを収集する
    pbr_url = "https://finance.yahoo.co.jp/stocks/ranking/lowPbr?market=all&term=daily&page="
    pbr_num = 60
    pbr_name = "pbr"
    pbr_instance = STI.STOCK_ELEMENT(date_path, pbr_url, pbr_num, pbr_name)
    pbr_instance.open_web()
    pbr_instance.write_text()
    #pbr_instance.save_hist()
    pbr_instance.save_scatter()

    #配当利回り
    divide_url = "https://finance.yahoo.co.jp/stocks/ranking/dividendYield?market=all&term=daily&page="
    divide_num = 60
    divide_name = "divide"
    divide_instance = STI.STOCK_ELEMENT(date_path, divide_url, divide_num, divide_name)
    divide_instance.open_web()
    divide_instance.write_text()
    #divide_instance.save_hist()
    divide_instance.save_scatter()

    #25日乖離率のデータを収集する
    sep25_url1 = "https://finance.yahoo.co.jp/stocks/ranking/highSeparationRate25plus?market=all&term=daily&page="
    sep25_url2 = "https://finance.yahoo.co.jp/stocks/ranking/highSeparationRate25minus?market=all&term=daily&page="
    sep25_num = 20
    sep25_rate = 50
    sep25_name = "highSeparationRate25"

    sep25_instance = STI.HIGH_SEPARATION(date_path, sep25_url1, sep25_url2, sep25_num, sep25_rate, sep25_name)
    sep25_instance.open_web()
    sep25_instance.write_text()
    sep25_instance.save_scatter()

    #75日乖離率のデータを収集する
    sep75_url1 = "https://finance.yahoo.co.jp/stocks/ranking/highSeparationRate75plus?market=all&term=daily&page="
    sep75_url2 = "https://finance.yahoo.co.jp/stocks/ranking/highSeparationRate75minus?market=all&term=daily&page="
    sep75_num = 20
    sep75_rate = 100
    sep75_name = "highSeparationRate75"

    sep75_instance = STI.HIGH_SEPARATION(date_path, sep75_url1, sep75_url2, sep75_num, sep75_rate, sep75_name)
    sep75_instance.open_web()
    sep75_instance.write_text()
    sep75_instance.save_scatter()

#処理
if __name__ == '__main__':
    print("Start")
    main()
    print("Done")