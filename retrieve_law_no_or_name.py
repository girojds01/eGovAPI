
class RetrieveLaw:
    def __init__(self):
        import requests
        url = "https://laws.e-gov.go.jp/api/1/lawlists/1"
        self.response = requests.get(url,verify = True)
        # レスポンスのステータスコードを確認
        if self.response.status_code == 200:
            # レスポンスのJSONデータを取得
            self.data = self.response.text #大した量でもないので、全部取得している
            # print(data)
        else:
            print(f"Error: {self.response.status_code}")

    
    def get_law_name_or_no(self,key_tag, key_string):
        #key_tagはLawNoかLawNameのどちらかを指定。それに応じて、key_stringは法令番号か法令名を指定
        #keyがNoならNameを取得、NameならNoを取得
        import xml.etree.ElementTree as ET
        # Parse the XML content
        root = ET.fromstring(self.data)
        
        # Find all LawNameListInfo elements
        law_name_list_infos = root.findall(".//LawNameListInfo")

        if key_tag == "LawName":
            target_tag = "LawNo"
        else:
            target_tag = "LawName"

        # Iterate through each LawNameListInfo element
        for law_info in law_name_list_infos:
            key_found = law_info.find(key_tag).text
            if  key_found == key_string:
                target_text = law_info.find(target_tag).text
                return target_text
        
        return None

if __name__ == "__main__":
    # Example usage
    retriever = RetrieveLaw()
    
   # Retrieve law number by law name
    law_name = "建築基準法施行令"
    law_no = retriever.get_law_name_or_no("LawName", law_name)
    print(f"Law No for '{law_name}': {law_no}")
    
    # Retrieve law name by law number
    law_no = "昭和二十五年政令第三百三十八号"
    law_name = retriever.get_law_name_or_no("LawNo", law_no)
    print(f"Law Name for '{law_no}': {law_name}")