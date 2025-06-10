import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import re


google_sheet = "https://docs.google.com/forms/d/e/1FAIpQLSd1ZjPtpp42rlJ2v-t6f2KXhSx7Z8gxd09rTGFs0KeQuSPbqg/viewform?usp=dialog/"
web_site_url = "https://appbrewery.github.io/Zillow-Clone/"

response = requests.get(web_site_url)
soup = BeautifulSoup(response.text , 'html.parser')
search = soup.find_all("article" , attrs = {"data-test":"property-card"})
data = {"address":[] , "price":[] , "link":[]}
for element in search:
    data["address"].append(element.find_next('address', attrs={'data-test': 'property-card-addr'}).get_text(strip = True))
    a_link = element.find_next('a', attrs={'data-test': 'property-card-link'})
    href_link = ''
    if a_link and 'href' in a_link.attrs:
        href_link = a_link['href']
    data["price"].append(element.find_next('span', attrs={'data-test': 'property-card-price'}).get_text(strip = True))
    data["link"].append(href_link)

data["price"]
x = []
for item in data["price"]:
    price = ""
    for letter in item:
        if letter == "/" or letter == "+":
            x.append(price)
            break
        if letter != "/" or letter != "+":
            price += letter
data["price"] = x
print(data["price"])
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach",True)
driver = webdriver.Chrome(options=chrome_options)
driver.get(google_sheet)
time.sleep(1)
nsubmit = len(data["address"])
for i in range(nsubmit):
    time.sleep(1)
    driver.find_element(By.XPATH,
                        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(
        data["address"][i])
    driver.find_element(By.XPATH,
                        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(
        data["price"][i])
    driver.find_element(By.XPATH,
                        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input').send_keys(
        data["link"][i])

    driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span').click()
    # print(driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div/span/span').text)
    time.sleep(1)
    driver.find_element(By.XPATH , '/html/body/div[1]/div[2]/div[1]/div/div[4]/a').click()
driver.quit()