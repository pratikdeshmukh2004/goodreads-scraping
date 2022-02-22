from selenium.webdriver.common.by import By
from selenium import webdriver
import time
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import os

load_dotenv()
webdriver_m = ChromeDriverManager().install()

def list_books_from_wishlist(link):
    driver = webdriver.Chrome(webdriver_m)
    driver.get(link)
    def load_pages():
        while True:
            load_text = driver.find_element(By.ID,value="infiniteStatus").text.split(' ')
            if load_text[0] == load_text[2]:
                return driver
            else:
                driver.execute_script("window.scrollBy(0,1000)", "")
                time.sleep(2)
    load_pages()
    tr_list = driver.find_elements_by_css_selector("td.shelves")
    link_list = []
    for tr in tr_list:
        link = tr.find_element(By.CLASS_NAME, value="stars").get_attribute("data-resource-id")
        link_list.append(link)
    driver.quit()
    return link_list

def get_book_detail(book_ids):
    result_list = []
    driver = webdriver.Chrome(webdriver_m)
    for b_id  in book_ids:
        try:
            data = {}
            driver.get("https://www.goodreads.com/buy_buttons/14/follow?book_id="+b_id)
            buttons = driver.find_element(By.XPATH,value='//*[@id="tmmSwatches"]/ul')
            buttons = buttons.find_elements(By.TAG_NAME, value="li")
            data['price'] = []
            for button in buttons:
                price_list = button.text.split("\n\n")
                for p in price_list:
                    if len(p)>0:
                        data['price'].append({str(p.split("\n")[0]).strip(): str(p.split("\n")[1]).strip()})
            data['title'] = driver.find_element(By.XPATH,value='//*[@id="productTitle"]').text
            data['product_link'] = driver.current_url
            result_list.append(data)
        except Exception as e:
            print(b_id,"Product Not Found", e)
    driver.quit()
    return result_list

def gift_book(url):
    email = os.environ.get("PHONE")
    password = os.environ.get("PASSWORD")
    driver = webdriver.Chrome(webdriver_m)
    driver.get(url)
    print(email, password)
    buttons = driver.find_element(By.XPATH,value='//*[@id="tmmSwatches"]/ul')
    buttons = buttons.find_elements(By.TAG_NAME, value="li")
    for button in buttons:
        if "Kindle Edition" in button.text:
            button.click()
            break
    driver.find_element(By.ID, value="buy-for-others-buy-button").click()
    driver.find_element_by_id("ap_email").send_keys(email)
    driver.find_element_by_id("ap_password").send_keys(password)
    driver.find_element_by_id("signInSubmit").click()
    time.sleep(100000)
    



print(gift_book("https://www.amazon.in/gp/product/0143442279/ref=x_gr_w_bb?ie=UTF8&tag=x_gr_w_bb_in-21&linkCode=as2&camp=3626&creative=24790"))