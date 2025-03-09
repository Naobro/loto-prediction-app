import pandas as pd
import requests
from bs4 import BeautifulSoup
import streamlit as st

# **ページのタイトル**
st.title("ナンバーズ AI予想サイト")

# **① 最新の当選番号**を表示
st.header("①最新の当選番号")

# **最新の当選番号をスクレイピングしてテーブルを生成**
def scrape_numbers_result():
    url = "https://ts4-net.com/result01.html"
    response = requests.get(url)
    
    # HTMLの解析
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 最新の当選番号を取得するためのHTMLを検索
    try:
        table = soup.find('table', {'class': 'table01'})
        rows = table.find_all('tr')
        
        # 最新の当選番号を格納するリスト
        latest_result = []

        # 1行目（ヘッダー行）はスキップ
        for row in rows[1:]:
            cols = row.find_all('td')
            if len(cols) >= 4:
                round_number = cols[0].get_text(strip=True)
                date = cols[1].get_text(strip=True)
                winning_numbers = cols[2].get_text(strip=True)
                bonus_numbers = cols[3].get_text(strip=True)
                
                latest_result.append([round_number, date, winning_numbers, bonus_numbers])

        # DataFrameに変換
        df = pd.DataFrame(latest_result, columns=["回号", "抽選日", "本数字", "ボーナス数字"])
        return df
    except Exception as e:
        return f"エラーが発生しました: {e}"

# スクレイピングしたデータを表示
df_latest_numbers = scrape_numbers_result()

# ストリームリットで表示
if isinstance(df_latest_numbers, pd.DataFrame):
    st.write(df_latest_numbers)
else:
    st.write("データの取得に失敗しました")