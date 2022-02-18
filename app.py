import json
from re import L
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())

def list_books_from_wishlist(link):
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
    return link_list

    
final = list_books_from_wishlist("https://www.goodreads.com/review/list/29695889-shreyas?ref=nav_mybooks&shelf=to-read")
with open("data.txt", "w") as f:
    f.write(json.dumps(final))