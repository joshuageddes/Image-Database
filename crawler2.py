import time
from typing import Counter
import urllib.request
from datetime import time

import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import gspread
import urllib.request
import time
import os

#import pyttsx3
#engine = pyttsx3.init()





gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('apiKey.json', scope)

client = gspread.authorize(creds)

data = client.open("Apollo Assets").worksheet('Data')
global counter
counter = 0


def uploadFile(counter):
    gfile = drive.CreateFile(
        {'parents': [{'id': '-'}]})
    upload_file = f"item{counter}.jpg"
    gfile.SetContentFile(upload_file)
    gfile.Upload()
    gfile = None


def adidasScraper(link, numPages, gender, itemType, brand):
    global counter
    counter = 0

    itemID = ["ww", "xx", "yy", "zzzz"]
    brandMatrix = [["Adidas", "01"]]
    typeMatrix = [["Shirts", "01"], ["Pants", "02"], ["Sweaters", "03"], ["Shorts", "04"], [
        "Jackets", "05"], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""], ["", ""]]

    for i in brandMatrix:
        if brand == i[0]:
            itemID[0] = i[1]

    if gender == "Male":
        itemID[1] = "00"
    else:
        itemID[1] = "01"

    for i in typeMatrix:
        if itemType == i[0]:
            itemID[2] = i[1]

    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    # options.add_argument("--headless")
    options.add_argument("--disable-notifications")
    browser = webdriver.Chrome(options=options)
    browser.set_window_size(1920, 1080)
    browser.maximize_window()
    browser.get(link)

    for b in range(1, numPages+1):
        print(f"    Page #{b}")
        for i in range(1, 49):
            counter += 1
            itemID2 = itemID[:-1]

            itemID2.append(str(counter))
            itemID2 = "".join(itemID2)

            print(f"Item #{i}")
            browser.execute_script("window.scrollBy(0,300)", "")
            item = browser.find_element_by_xpath(
                f'/html/body/div[2]/div/div[1]/div/div/div/div[2]/div/div[2]/div/div/div[2]/div[1]/div/div[{i}]/div/div/div/div/div/div[1]/a/img[1]')

            src = item.get_attribute('src')
            urllib.request.urlretrieve(src, f"item{itemID2}.jpg")

            try:
                item_name = browser.find_element_by_xpath(
                    f"/html/body/div[2]/div/div[1]/div/div/div/div[2]/div/div[2]/div/div/div[2]/div[1]/div/div[{i}]/div/div/div/div/div/div[3]/p[1]").text
                print("1", item_name)
            except:
                try:
                    item_name = browser.find_element_by_xpath(
                        f"/html/body/div[2]/div/div[1]/div/div/div/div[2]/div/div[2]/div/div/div[2]/div[1]/div/div[{i}]/div/div/div/div/div/div[2]/p[1]").text
                    print("2", item_name)
                except:
                    item_name = "Not Found"
            print("3", item_name)
            try:
                item_link = browser.find_element_by_xpath(
                    f"/html/body/div[2]/div/div[1]/div/div/div/div[2]/div/div[2]/div/div/div[2]/div[1]/div/div[{i}]/div/div/div/div/div/div[1]/a").get_attribute("href")
            except:
                item_link = "Not Found"
            try:
                item_price = browser.find_element_by_xpath(
                    f"/html/body/div[2]/div/div[1]/div/div/div/div[2]/div/div[2]/div/div/div[2]/div[1]/div/div[{i}]/div/div/div/div/div/div[1]/div[2]/div/div/div").text
            except:
                item_price = "Not Found"

            uploadFile(itemID2)
            data.insert_row([f"{itemID2}", f"{item_name}", f"{item_link}",
                             f"{item_price}", gender, itemType, brand], counter + 1)
            time.sleep(1.25)
            os.remove(f"item{itemID2}.jpg")

        browser.execute_script("window.scrollBy(0,-300)", "")
        browser.get(f"{link}?start={b*48}")
        time.sleep(10)

# men shirts
# adidasScraper("https://www.adidas.ca/en/men-shirts-clothing",11, "Male", "Shirts", "Adidas")
# speak("Finished men shirts")

# women shirts
# adidasScraper("https://www.adidas.ca/en/women-shirts-clothing", 10, "Female","Shirts","Adidas")
# speak("Finished women shirts")

# men pants
# adidasScraper("https://www.adidas.ca/en/men-pants-clothing", 4, "Male","Pants","Adidas")
# speak("Finished men pants")

# women pants
# adidasScraper("https://www.adidas.ca/en/women-pants-clothing", 4, "Female","Pants","Adidas")
# speak("Finished women pants")

# men sweaters
# adidasScraper("https://www.adidas.ca/en/men-hoodies%7Csweatshirts-clothing", 6, "Male","Sweaters","Adidas")
# speak("Finished women sweaters")

# women sweaters
# adidasScraper("https://www.adidas.ca/en/women-hoodies%7Csweatshirts-clothing", 4, "Female", "Sweaters", "Adidas")
# speak("Finished women sweaters")

# men jackets
# adidasScraper("https://www.adidas.ca/en/men-jackets-clothing", 5, "Male","Jackets","Adidas")
# speak("Finished women jackets")

# women jackets
# adidasScraper("https://www.adidas.ca/en/women-jackets-clothing", 4, "Female","Jackets","Adidas")
# speak("Finished women jackets")

# men shorts
# adidasScraper("https://www.adidas.ca/en/men-shorts-clothing", 4, "Male", "Shorts", "Adidas")
# speak("Finished men shorts")

# women shorts
# adidasScraper("https://www.adidas.ca/en/women-shorts-clothing", 3, "Female", "Shorts", "Adidas")
# speak("Finished women shorts")
