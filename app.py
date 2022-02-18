import json
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import requests
from bs4 import BeautifulSoup
import concurrent.futures

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


# final = list_books_from_wishlist("https://www.goodreads.com/review/list/29695889-shreyas?ref=nav_mybooks&shelf=to-read")
with open("data.txt", "r") as f:
    final = json.loads(f.read())
with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    result = executor.map(find_amazon_link, final)
print(list(result))
# for l in final:
#     print("\n\n\nBook Link:",l)
#     print("Amazon Link:", find_amazon_link(l))

# with open("data.txt", "w") as f:
#     f.write(json.dumps(final))