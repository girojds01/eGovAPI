import requests
url = f"https://laws.e-gov.go.jp/api/1/lawdata/昭和二十七年法律第二百三十九号"
print(url)
response = requests.get(url,verify = True)
# レスポンスのステータスコードを確認
if response.status_code == 200:
    # レスポンスのJSONデータを取得
    data = response.text 
    # print(data)
else:
    print(f"Error: {response.status_code}")
    
    
#テキストファイルに出力
with open("旅行業法.txt", "w", encoding="utf-8") as file:
    file.write(data)
    print("法令データを法令データ.txtに保存しました。")