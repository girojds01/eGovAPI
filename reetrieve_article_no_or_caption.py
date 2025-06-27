class RetrieveArticle:
    """
    e-Gov法令APIから、法令番号と条文番号を指定して、条見出しを取得する、或いは条見出しを指定して条文番号を取得するクラス
    """
    def __init__(self, url, LawNo):
        import requests
        url = f"https://laws.e-gov.go.jp/api/1/lawdata/{LawNo};"
        self.response = requests.get(url,verify = False)
        # レスポンスのステータスコードを確認
        if self.response.status_code == 200:
            # レスポンスのJSONデータを取得
            self.data = self.response.text 
            # print(data)
        else:
            print(f"Error: {self.response.status_code}")


#平成二十八年法律第百一号

#law_numとarticle_numを引数にして、APIから条文を取得する関数
#ただし、law_numもarticle_numもそのままapiに与えられる形（law_numは全部全角、article_numは全部半角）
def get_article_content(law_num, article_num):
    import requests
    # APIのエンドポイントURL
    url = f"https://laws.e-gov.go.jp/api/1/articles;lawNum={law_num};article={article_num}"
    response = requests.get(url, verify= False)
    # レスポンスのステータスコードを確認
    if response.status_code == 200:
        # レスポンスのJSONデータを取得
        xml_content = response.text
    else:
        xml_content = str(response.status_code)
        #print(f"Error: {response.status_code}")
    return xml_content


#与えられた条文から、キャプションを取得
def get_article_captions(xml_text):
    import xml.etree.ElementTree as ET
    # tree = ET.parse(xml_file)
    # root = tree.getroot()
    root = ET.fromstring(xml_text)
    
    # 文書内のすべてのArticleCaption要素を見つける
    article_captions = root.findall('.//ArticleCaption')
    
    # 各ArticleCaption要素のテキスト内容を抽出する
    captions = [caption.text for caption in article_captions]
    
    return captions