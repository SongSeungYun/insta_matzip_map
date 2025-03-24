#data_analyzing.py
import requests
import json
from geopy.geocoders import Nominatim

with open ("../data/secret.json", "r") as f:
    data = json.load(f)
    API_KEY=data["AI_API_KEY"]
# Perplexity API 설정

def extract_restaurant_info(input_text):#ai response 받아오기
    url = "https://api.perplexity.ai/chat/completions"
    
    payload = {
        "model": "llama-3.1-sonar-small-128k-online",
        "messages": [
            {
                "role": "system",
                "content": "텍스트에서 식당의 name, address, main_menu, type(밥집, 술집, 카페 중 하나)\
                    을 key로 가지는 json을 반환 main_menu의 value는 list이고 안내사항 및 부연설명없이 오로지 json만 반환"
            },
            {
                "role": "user",
                "content": input_text
            }
        ],
        "max_tokens": 150,
        "temperature": 0.8,
        "top_p": 0.9,
        "search_domain_filter": ["perplexity.ai"],
        "return_images": False,
        "return_related_questions": False,
        "search_recency_filter": "month",
        "top_k": 0,
        "stream": False,
        "presence_penalty": 0,
        "frequency_penalty": 1
    }
    
    headers = {
        "Authorization": "Bearer "+API_KEY,
        "Content-Type": "application/json"
    }
    
    response = requests.request("POST", url, json=payload, headers=headers)

    result = json.loads(response.text)
    extracted_info = result['choices'][0]['message']['content']
    
    return extracted_info

def address_to_latlog(add):#주소 입력 -> 위도 경도 반환
    add_split=add.split(" ")
    try:
        while add_split[-1][-1].isdigit()==False:
            add_split.pop()
    except IndexError as e:
        return (0,0)

    geoloc = Nominatim(user_agent = 'South Korea', timeout=None)    # 사용자 에이전트를 설정
    geo = geoloc.geocode(" ".join(add_split))     # 주소로 위치 정보 가져오기
    if geo:
        lat = geo.latitude
        log = geo.longitude
        return (lat,log)
    else:
        return (0,0)

def parse_custom_json(input_string):#api response 문자열 입력 -> 식당 정보 json 변환
    # 문자열을 ```json과 ``` 기준으로 분리
    parts = input_string.split('```json')
    if len(parts) > 1:
        json_part = parts[1].split('```')[0]
        
        # JSON 문자열 파싱
        try:
            result = json.loads(json_part)
            if "name" in result and "address" in result:
                result["latitude"],result["longitude"]=address_to_latlog(result["address"])
                return result
        except json.JSONDecodeError as e:
            return None
    else:
        return None

def get_restaurant_info(reels_link,texts):
    with open('../data/restaurants_infos.json', 'r', encoding='utf-8') as f:
        old_restaurant_infos = json.load(f)
    for i,text in enumerate(texts):
        temp=extract_restaurant_info(text)
        print(i,"api 답변 결과",type(temp),temp)
        data = parse_custom_json(temp)
        if data:
            data["reels_link"]=reels_link[i]
            old_restaurant_infos["restaurants"].append(data)
        else:
            print(text,"\n 본문의 json 추출 실패")
        # with open('restaurants_infos.json', 'w', encoding='utf-8') as f:
        #     json.dump(old_restaurant_infos, f, ensure_ascii=False, indent=2)
        print(i,data)
    with open('../data/restaurants_infos.json', 'w', encoding='utf-8') as f:
        json.dump(old_restaurant_infos, f, ensure_ascii=False, indent=2)
    ("식당 정보 json 작성 끝")