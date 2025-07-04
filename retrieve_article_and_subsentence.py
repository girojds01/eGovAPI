class RetrieveArticleAndSubsentence:
    """
    e-Gov法令APIから、法令番号と条文番号を指定して、条見出しを取得する、或いは条見出しを指定して条文番号を取得するクラス
    """
    def __init__(self,LawNo,ArticleNo = None, ParagraphNo = None):
        #初期化クラスはまず条または（かつ）項から、条文を取得する
        import requests
        if ArticleNo is not None and ParagraphNo is None:
            # 条文番号のみを指定する場合
            url = f"https://laws.e-gov.go.jp/api/1/articles;lawNum={LawNo};article={ArticleNo}"
        elif ArticleNo is None and ParagraphNo is not None:
            #条文番号はなく、項番号がある
            url = f"https://laws.e-gov.go.jp/api/1/articles;lawNum={LawNo};paragraph={ParagraphNo}"
        elif ArticleNo is not None and ParagraphNo is not None:
            # 条文番号と項番号の両方を指定する場合        
            url = f"https://laws.e-gov.go.jp/api/1/articles;lawNum={LawNo};article={ArticleNo};paragraph={ParagraphNo}"
        else:
            # 条文番号も項番号も指定しない場合
            url = f"https://laws.e-gov.go.jp/api/1/lawdata/{LawNo}"
            
        print(url)
        self.response = requests.get(url,verify = True)
        # レスポンスのステータスコードを確認
        if self.response.status_code == 200:
            # レスポンスのJSONデータを取得
            self.data = self.response.text 
            # print(data)
        else:
            print(f"Error: {self.response.status_code}")