def retrieve_url(law_no, article_no, paragraph_no, item_no):
    """
    e-Gov法令APIから、法令番号と条文番号を指定して、条文の内容を取得する。
    :param law_no: 法令番号
    :param article_no: 条文番号
    :param paragraph_no: 段落番号
    :param item_no: 項目番号
    :return: 条文の内容
    """
    import pandas as pd
    if pd.isna(item_no) == False: #号チェック
        target = "item"
        if pd.isna(article_no) and pd.isna(paragraph_no):
            #なしなしあり
            url = f"https://laws.e-gov.go.jp/api/1/articles;lawNum={law_no}"
        elif pd.isna(article_no) and pd.isna(paragraph_no)==False:
            #なしありあり
            url = f"https://laws.e-gov.go.jp/api/1/articles;lawNum={law_no};paragraph={paragraph_no}"
        elif pd.isna(article_no)==False and pd.isna(paragraph_no):
            #ありなしあり
            url = f"https://laws.e-gov.go.jp/api/1/articles;lawNum={law_no};article={article_no}"
        elif pd.isna(article_no)==False and pd.isna(paragraph_no)==False:
            #ありありあり
            url = f"https://laws.e-gov.go.jp/api/1/articles;lawNum={law_no};article={article_no};paragraph={paragraph_no}"
            
    elif pd.isna(paragraph_no) == False: #項チェック
        target = "paragraph"
        if pd.isna(article_no):
        #なしありなし
            url = f"https://laws.e-gov.go.jp/api/1/articles;lawNum={law_no};paragraph={paragraph_no}"
        else:
        #ありありなし
            url = f"https://laws.e-gov.go.jp/api/1/articles;lawNum={law_no};article={article_no};paragraph={paragraph_no}"
            
    else:
        #無意味または不要
        target = None
        url = None
        
    return target, url


def exists_item( url, item_no):
    #号取得の例
    import requests

    response = requests.get(url,verify = True)
    data = response.text

    import xml.etree.ElementTree as ET
    # パース
    root = ET.fromstring(data)

    # Item Num="item_no" を探す
    item = root.find(f".//Item[@Num='{item_no}']")

    # 下位要素を含む XML 文字列として取得
    if item is not None:
        return True
    else:
        return False

def exists_paragraph(url):
    
    import requests
    response = requests.get(url,verify = True)
    data = response.text
    
    import xml.etree.ElementTree as ET
    # XMLをパース
    root = ET.fromstring(data)

    # <Code> 要素の値を取得して判断
    code_element = root.find(".//Code")

    # 真偽値を返すロジック
    if code_element is not None and code_element.text == "0":
        return True
    elif code_element is not None and code_element.text == "1":
        return False
    else:
        # 意図しないコード値や欠損への対応
        return None
    
def check_item_or_paragraph(law_no, article_no, paragraph_no, item_no):
    target, url = retrieve_url(law_no, article_no, paragraph_no, item_no)
    if target == "item":  # 号チェック
        return exists_item(url, item_no)
    elif target == "paragraph":  # 項チェック
        return exists_paragraph(url)
    else:
        # 無意味または不要
        return  None


