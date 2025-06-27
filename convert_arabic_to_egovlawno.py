#main_string:チェック対象　この場合約款本文
#target_char：検索する対象　この場合法令番号
#registered_string：検索する対象の手前にあって、マッチするかどうかを確認する対象　この場合、法令名


#全角数字を半角数字に変換
def zen2han(text):
    import unicodedata
    return unicodedata.normalize('NFKC', text)

#条番号からapi用条番号を取得
def convert_article_no_for_api(article_no):
    import re
    pattern = r"第([0-9０-９]+)条(?:の([0-9０-９]+))?"
    match = re.search(pattern,article_no)
    article_no_for_api = zen2han(match.group(1))
    if match.group(2) is not None:
        article_no_for_api += "_" + zen2han(match.group(2))

    return article_no_for_api

#算用数字を漢数字に
def arabic_to_kanji(number):
    number = zen2han(number)
    kanji_digits = ["〇", "一", "二", "三", "四", "五", "六", "七", "八", "九"]
    kanji_units = ["", "十", "百", "千", "万"]
    
    result = ""
    num_str = str(number)
    #print(num_str)
    length = len(num_str)
    
    for i, digit in enumerate(num_str):
        if digit != '0':
            if digit != '1' or i == length - 1 : #1でない、或いは末尾の桁である
                result += kanji_digits[int(digit)] + kanji_units[length - i - 1]
            else: #1かつ末尾でない
                result += kanji_units[length - i - 1]
    return result


#文中の算用数字を漢数字に
def convert_arabic_to_kanji_in_string(input_string):
    import re
    pattern = re.compile(r'\d+')
    
    def replace_with_kanji(match):
        return arabic_to_kanji(match.group())
    
    return pattern.sub(replace_with_kanji, input_string)

#条文番号からそれに対応する法令名を取得
def get_law_name_by_law_no(xml_lawlists_content, target_law_no):
    import xml.etree.ElementTree as ET
    # Parse the XML content
    root = ET.fromstring(xml_lawlists_content)
    
    # Find all LawNameListInfo elements
    law_name_list_infos = root.findall(".//LawNameListInfo")
    
    # Iterate through each LawNameListInfo element
    for law_info in law_name_list_infos:
        law_no = law_info.find("LawNo").text
        if law_no == target_law_no:
            law_name = law_info.find("LawName").text
            return law_name
    
    return None

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




if __name__ == '__main__':
    print(convert_arabic_to_kanji_in_string("大正11年法律第70号"))
    print(convert_article_no_for_api("第44条の３"))


