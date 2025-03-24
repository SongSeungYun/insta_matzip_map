#crawling.py
#참고한 사이트
#https://velog.io/@xodbs6/Practice-%EC%9D%B8%EC%8A%A4%ED%83%80-%ED%81%AC%EB%A1%A4%EB%A7%81-%EC%B9%B4%EC%B9%B4%EC%98%A4-API-Counter
#https://lightbakery.tistory.com/208

#크롬 드라이버 자동으로 다운받는 webdriver-manager 설치.
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import random
import json
import time
import requests
import re

def get_insta_elements():
    selector={
        "post_count":'span.html-span.xdj266r',
        "first_post":'._ac7v.xzboxd6.xras4av.xgc1b0m div a ._aagu > ._aagv + ._aagw',
        "reels":'div._ac7v > div.x1lliihq > a.x1i10hfl',
        "text": 'a > div._aagu > div._aagv > img'
    }

    #브라우저 꺼짐 방지 
    chrome_options = Options()
    chrome_options.add_experimental_option("detach", True)

    #불필요한 에러 메시지 없애기
    chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"]) #셀레니움 로그 무시

    #서비스랑 드라이버 객체 생성. 세팅은 아니지만, 이거 안하면 어차피 진행이 안되서. 
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    #인스타로 이동
    driver.get('https://instagram.com')
    time.sleep(3)

    with open ("../data/secret.json", "r") as f:
        data = json.load(f)
        INSTA_ID=data["Insta_ID"]
        INSTA_PW=data["Insta_PW"]
        API_KEY=data["AI_API_KEY"]

    #인스타 로그인
    driver.implicitly_wait(10)
    login_id = driver.find_element(By.CSS_SELECTOR, 'input[name="username"]')
    login_id.send_keys(INSTA_ID) #아이디
    login_pwd = driver.find_element(By.CSS_SELECTOR, 'input[name="password"]')
    login_pwd.send_keys(INSTA_PW) #비번
    driver.implicitly_wait(10)
    login_pwd.submit()
    time.sleep(2)
    login_id.send_keys(Keys.ENTER)
    time.sleep(2)

    account_id=["hotdor_s"]#크롤링할 계정들

    #기존에 얼마만큼의 게시물을 가져왔는지 체크
    with open('../data/post_count.json', 'r', encoding='utf-8') as file:
        post_count = json.load(file)

    #신규 id가 있다면 post_count에 추가
    for id in account_id:
        if id not in post_count:
            post_count[id]=0

    def get_url(id):#특정 id의 url 얻기
        url = 'https://www.instagram.com/' + id
        return url

    def click_nxt():
        next_btn = driver.find_element(By.CSS_SELECTOR, selector['next_btn'])
        next_btn.click()
        time.sleep(0.5)

    reels_link=[]
    texts=[]

    for id in account_id:

        #몇 개의 게시물을 가져와야할지 체크하기
        old_post_count=post_count[id]#기존에 크롤링했던 게시물의 개수
        driver.get(get_url(id))#링크 접속
        time.sleep(2+random.random()*2)#랜덤하게 sleep
        new_post_count=int(driver.find_element(By.CSS_SELECTOR, selector["post_count"]).text)
        get_post_count=new_post_count-old_post_count#새로 가져와야할 게시물의 수
        if get_post_count==0:#가져올게 없으면 continue
            continue
        print("가져와야할 게시물의 개수 :",get_post_count)
        
        #릴스링크, 본문 가져오기
        reels_elements=driver.find_elements(By.CSS_SELECTOR,selector["reels"])[:get_post_count]
        text_elements=driver.find_elements(By.CSS_SELECTOR,selector["text"])[:get_post_count]
        for i in range(len(reels_elements)):
            elements_reels_link=reels_elements[i].get_attribute('href')
            elements_text=text_elements[i].get_attribute('alt')
            reels_link.append(elements_reels_link)
            texts.append(elements_text)
            print("get",len(reels_link)-1,"elements")

        #만약 가져올게 남았다면 더 가져오기
        while len(reels_link)!=get_post_count:
            driver.execute_script("window.scrollBy(0, 1000)")
            temp_reels_link=[]
            temp_texts=[]
            reels_elements=driver.find_elements(By.CSS_SELECTOR,selector["reels"])[:get_post_count]
            text_elements=driver.find_elements(By.CSS_SELECTOR,selector["text"])[:get_post_count]
            for i in range(-1,-len(reels_elements)-1,-1):
                elements_reels_link=reels_elements[i].get_attribute('href')
                if reels_link[-1]==elements_reels_link:
                    break
                elements_text=text_elements[i].get_attribute('alt')
                temp_reels_link.append(elements_reels_link)
                temp_texts.append(elements_text)
            for i in range(-1,-len(temp_reels_link)-1,-1):
                reels_link.append(temp_reels_link[i])
                texts.append(temp_texts[i])
                print("get",len(reels_link)-1,"elements")
        post_count[id]=new_post_count
        
    print(len(reels_link),"개의 릴스 링크를 가져옴")
    print(len(texts),"개의 게시물을 가져옴")
    print("good crawling & post_count.json update")
    with open('../data/post_count.json', 'w') as file:
        json.dump(post_count, file, indent=4)
    return [reels_link,texts]