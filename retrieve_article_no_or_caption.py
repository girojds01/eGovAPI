class RetrieveArticle:
    """
    e-Gov法令APIから、法令番号と条文番号を指定して、条見出しを取得する、或いは条見出しを指定して条文番号を取得するクラス
    """
    def __init__(self,LawNo):
        #初期化クラスはまず法令番号を引数にとって、その法令自体を取得する
        import requests
        url = f"https://laws.e-gov.go.jp/api/1/lawdata/{LawNo}"
        print(url)
        self.response = requests.get(url,verify = False)
        # レスポンスのステータスコードを確認
        if self.response.status_code == 200:
            # レスポンスのJSONデータを取得
            self.data = self.response.text 
            # print(data)
        else:
            print(f"Error: {self.response.status_code}")

    def get_article_no(self,article_caption):
        """
        条見出しを指定して、条文番号を取得するメソッド
        :param article_caption: 条見出しの文字列
        :return: 条文番号のリスト
        """
        import xml.etree.ElementTree as ET
        root = ET.fromstring(self.data)
        
        # 条見出しに一致するArticleCaption要素を検索
        article_captions = root.findall('.//ArticleCaption')
        
        # 一致する条文番号を格納するリスト
        article_numbers = []
        
        for caption in article_captions:
            if caption.text == article_caption:
                # 親要素のArticleNoから条文番号を取得
                article_no = caption.find('ArticleNo').text
                article_numbers.append(article_no)
        
        return article_numbers
    
    def get_article_caption(self,article_no):
        """
        条文番号を指定して、条見出しを取得するメソッド
        :param article_no: 条文番号の文字列
        :return: 条見出しのリスト
        """
        import xml.etree.ElementTree as ET
        root = ET.fromstring(self.data)
        
        # <ArticleTitle>がarticle_noの<Article>要素を探す
        for article in root.findall('.//Article'):
            title = article.find('ArticleTitle')
            # print(title.text)
            if title is not None and title.text == article_no:
                caption = article.find('ArticleCaption')
                if caption is not None:
                    return caption.text 



    def exists_article_caption(self,article_caption):
        """
        条見出しが存在するかどうかを確認するメソッド
        :param article_caption: 条見出しの文字列
        :return: 存在する場合はTrue、存在しない場合はFalse
        """
        article_numbers = self.get_article_no(article_caption)
        return len(article_numbers) > 0
    
    def exists_article_no(self,article_no):
        """
        条文番号が存在するかどうかを確認するメソッド
        :param article_no: 条文番号の文字列
        :return: 存在する場合はTrue、存在しない場合はFalse
        """
        article_captions = self.get_article_caption(article_no)
        return len(article_captions) > 0


if __name__ == "__main__":
    # 使用例
    law_num = "平成二十八年法律第百一号"
    article_no = "第四十二条"
    article_caption = "aaa"
    
    retriever = RetrieveArticle(law_num)
    # print(retriever.data)  # 法令データの表示
    
    # # 条見出しから条文番号を取得
    # article_numbers = retriever.get_article_no(article_caption)
    # print(f"条見出し '{article_caption}' に対応する条文番号: {article_numbers}")
    
    # 条文番号から条見出しを取得
    article_captions = retriever.get_article_caption(article_no)
    print(f"条文番号{article_no}に対応する条見出し: {article_captions}")
    
    # # 条見出しの存在確認
    # exists_caption = retriever.exists_article_caption(article_caption)
    # print(f"条見出し '{article_caption}' は存在するか: {exists_caption}")
    
    # # 条文番号の存在確認
    # exists_no = retriever.exists_article_no("1")
    # print(f"条文番号 '1' は存在するか: {exists_no}")
    

# #平成二十八年法律第百一号

# #law_numとarticle_numを引数にして、APIから条文を取得する関数
# #ただし、law_numもarticle_numもそのままapiに与えられる形（law_numは全部全角、article_numは全部半角）
# def get_article_content(law_num, article_num):
#     import requests
#     # APIのエンドポイントURL
#     url = f"https://laws.e-gov.go.jp/api/1/articles;lawNum={law_num};article={article_num}"
#     response = requests.get(url, verify= False)
#     # レスポンスのステータスコードを確認
#     if response.status_code == 200:
#         # レスポンスのJSONデータを取得
#         xml_content = response.text
#     else:
#         xml_content = str(response.status_code)
#         #print(f"Error: {response.status_code}")
#     return xml_content


# #与えられた条文から、キャプションを取得
# def get_article_captions(xml_text):
#     import xml.etree.ElementTree as ET
#     # tree = ET.parse(xml_file)
#     # root = tree.getroot()
#     root = ET.fromstring(xml_text)
    
#     # 文書内のすべてのArticleCaption要素を見つける
#     article_captions = root.findall('.//ArticleCaption')
    
#     # 各ArticleCaption要素のテキスト内容を抽出する
#     captions = [caption.text for caption in article_captions]
    
#     return captions