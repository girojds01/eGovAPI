import requests
url = f"https://laws.e-gov.go.jp/api/1/lawdata/平成二十八年法律第百一号"
print(url)
response = requests.get(url,verify = True)
# レスポンスのステータスコードを確認
if response.status_code == 200:
    # レスポンスのJSONデータを取得
    data = response.text 
    print(data)
else:
    print(f"Error: {response.status_code}")