#main.py
import crawling
import data_analyzing

def main():
    reels_link,texts=crawling.get_insta_elements()
    data_analyzing.get_restaurant_info(reels_link,texts)
    print("gooood")
    
if __name__=='__main__':
    main()