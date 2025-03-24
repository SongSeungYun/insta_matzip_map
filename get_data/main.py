#main.py
import get_data.crawling as crawling
import get_data.data_analyzing as data_analyzing

def main():
    reels_link,texts=crawling.get_insta_elements()
    data_analyzing.get_restaurant_info(reels_link,texts)
    print("gooood")
    
if __name__=='__main__':
    main()