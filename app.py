import json
from pprint import pprint
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import requests
from bs4 import BeautifulSoup
import concurrent.futures

def list_books_from_wishlist(link):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(link)
    def load_pages():
        while True:
            load_text = driver.find_element_by_id("infiniteStatus").text.split(' ')
            print(load_text)
            if load_text[0] == load_text[2]:
                return driver
            else:
                driver.execute_script("window.scrollBy(0,1000)", "")
                time.sleep(2)
    load_pages()
    tr_list = driver.find_elements_by_class_name("bookalike")
    link_list = []
    for tr in tr_list:
        link = tr.find_element_by_tag_name("a").get_attribute("href")
        link_list.append(link)
    driver.quit()
    return link_list


def find_amazon_link(book_link):
    for i in range(5):
        try:
            resp=requests.get(book_link)
            soup=BeautifulSoup(resp.content,"html.parser")
            main=soup.find('a',class_="buttonBar")
            return "https://www.goodreads.com"+main.attrs['href']
        except Exception as e:
            print(e)
            print(i,"Didn't Work...\n\n")
            continue
    else:
        print(book_link, i, "Not working at all........................\n\n\n")

def get_book_detail(amazon_link):
    data = {}
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(amazon_link)
        buttons = driver.find_element_by_xpath('//*[@id="tmmSwatches"]/ul')
        print([buttons.text], "text\n\n\n")
        buttons = buttons.find_elements_by_tag_name("li")
        data['price'] = []
        for button in buttons:
            price_list = button.text.split("\n\n")
            for p in price_list:
                if len(p)>0:
                    data['price'].append({p.split("\n")[0]: p.split("\n")[1]})
        data['title'] = driver.find_element_by_xpath('//*[@id="productTitle"]').text
        data['product_link'] = driver.current_url
        data['available'] = ""
        driver.quit()
    except Exception as e:
        print("Product Not Found", e)
    return data

# get_book_detail("https://www.goodreads.com/buy_buttons/14/follow?book_id=56627&page_type=book&page_type_id=56627&ref=x_gr_w_bb_sout&sub_page_type=show&tag=x_gr_w_bb_sout-20%27", '441907')

final = list_books_from_wishlist("https://www.goodreads.com/review/list/80018703-sai-bhaskar-devatha?shelf=to-read")

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    result = executor.map(find_amazon_link, final)

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    result = executor.map(get_book_detail, list(result))

with open("data.txt", "w") as f:
   f.write(json.dumps(list(result)))
