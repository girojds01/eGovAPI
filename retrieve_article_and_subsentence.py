class RetrieveArticleAndSubsentence:
    """
    e-Gov法令APIから、法令番号と条文番号を指定して、条見出しを取得する、或いは条見出しを指定して条文番号を取得するクラス
    """
    def __init__(self,LawNo,ArticleNo, ParagraphNo, ItemNo):
        #初期化クラスはまず条または（かつ）項から、条文を取得する
        import requests
        url = f"https://laws.e-gov.go.jp/api/1/articles;lawNum={LawNo};article={ArticleNo};paragraph={ParagraphNo}"
        print(url)
        self.response = requests.get(url,verify = True)
        # レスポンスのステータスコードを確認
        if self.response.status_code == 200:
            # レスポンスのJSONデータを取得
            self.data = self.response.text 
            # print(data)
        else:
            print(f"Error: {self.response.status_code}")