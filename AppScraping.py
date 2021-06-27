# web scraping

# import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

def iserror(func_name, args):
    try:
        func_name(args)
        return False
    except:
        return True

driver = webdriver.Chrome('./linux-chromedriver')

driver.get('https://apps.apple.com/in/app/steps-step-counter-activity/id719208154')
results = []

WebDriverWait(driver,10).until(ec.element_to_be_clickable((By.XPATH,"/html/body/div[4]/div/main/div[2]/section[6]/div[1]/div/div/button")))
see_details = driver.find_element_by_xpath("/html/body/div[4]/div/main/div[2]/section[6]/div[1]/div/div/button")
see_details.click()
i=3
WebDriverWait(driver,10).until(ec.presence_of_element_located((By.XPATH,f"/html/body/div[5]/div/div/div/div[{i}]/div/h2")))
while i<=5:
    head = driver.find_element_by_xpath(f"/html/body/div[5]/div/div/div/div[{i}]/div/h2")
    print("*************************************************")
    print(head.text)
    j=2
    while iserror(driver.find_element_by_xpath,f"/html/body/div[5]/div/div/div/div[{i}]/div/div[{j}]/div[2]")==False:
        div = driver.find_element_by_xpath(f"/html/body/div[5]/div/div/div/div[{i}]/div/div[{j}]/div[2]")
        div_text_list = div.text.split('\n')
        print("Category: ",div_text_list[0],"\t","sub-category: ",div_text_list[1])
        j+=1
    i+=1

# content = driver.page_source
# soup = BeautifulSoup(content)
# for element in soup.findAll(attrs={'selfclear is-apps-theme'}):
#     name = element.find('privacy-type__items')
#     if name not in results:
#         results.append(name.text)
# print(results)


