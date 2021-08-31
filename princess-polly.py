import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import urllib
import time
import os


gauth = GoogleAuth()
gauth.LocalWebserverAuth()
drive = GoogleDrive(gauth)

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('apiKey.json', scope)

client = gspread.authorize(creds)

data = client.open("Apollo Data Test").worksheet('NewData')


def upload_file_(item_id):
    gfile = drive.CreateFile(
        {'parents': [{'id': '-'}]})
    upload_file = item_id
    gfile.SetContentFile(upload_file)
    try:
        gfile.Upload()
    except:
        time.sleep(30)
        gfile.Upload()
    gfile = None



def princess_polly_scraper(link, num_pages, gender, item_type, brand):

    id_count = 0
    
    item_id = ["ww", "xx", "yy", "zzzz"]
    brand_dict = {"Princess Polly" : "03"}
    type_dict = {"Dresses" : "06"}

    if brand in brand_dict:
        item_id[0] = brand_dict[brand]

    if gender == "Male":
        item_id[1] = "00"
    else :
        item_id[1] = "01"


    if item_type in type_dict:
        item_id[2] = type_dict[item_type]


    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("--disable-notifications")
    #options.add_argument("--headless")
    
    browser = webdriver.Chrome(options=options)
    browser.set_window_size(1920, 1080)
    browser.maximize_window()


    item_color = ""
    item_price = ""
    item_name = ""
    item_link = ""


    



    for page in range(1, num_pages+1):

        browser.get(f"{link}?page={page}&sort=title-ascending")

        item_count = len(browser.find_elements_by_class_name('product-tile'))

        for i in range (1, item_count+1):

            id_count+=1

            #item link

            try:
                item_link = browser.find_element_by_xpath(f'/html/body/main/article/div/section/div[1]/div[{i}]/div[2]/a').get_attribute('href')

            except:
                item_link = "Unknown"


            #item color


            try:
                item_color = browser.find_element_by_xpath(f'/html/body/main/article/div/section/div[1]/div[{i}]').get_attribute('data-product-tile-active-color')

            except:
                item_color = "Unknown"

            #item name

            try:
                item_name = browser.find_element_by_xpath(f'/html/body/main/article/div/section/div[1]/div[{i}]/div[2]/a').text

            except:
                item_name = "Unknown"

            #item price

            try:
                item_price = browser.find_element_by_xpath(f'/html/body/main/article/div/section/div[1]/div[{i}]/div[2]/div[2]/span[1]').text
            except:
                item_price = "Unknown"

            
            


            formatted_id = item_id[:-1]
            formatted_id.append(str(id_count))
            formatted_id = "".join(formatted_id)

            

            try:
                        data.insert_row([f"{formatted_id}", f"{item_name}", f"{item_link}",
                                 f"{item_price}", f"{item_color}", gender, item_type, brand, i], id_count+20431)
            except:
                        time.sleep(30)
                        data.insert_row([f"{formatted_id}", f"{item_name}", f"{item_link}",
                                 f"{item_price}", f"{item_color}", gender, item_type, brand, i], id_count+20431)

            time.sleep(1)


            #item pictures

            pic_count = len(browser.find_elements_by_xpath(f'/html/body/main/article/div/section/div[1]/div[{i}]/div[1]/div[1]/div[1]/div'))

            for p in range (1, pic_count +1):

                picture = browser.find_element_by_xpath(f'/html/body/main/article/div/section/div[1]/div[{i}]/div[1]/div[1]/div[1]/div[{p}]/a/figure/img')

                src = picture.get_attribute('data-src')

                if src is None:
                    src = picture.get_attribute('src')

                
                urllib.request.urlretrieve(src, f"item{formatted_id} ({p}).jpg")
                upload_file_(f"item{formatted_id} ({p}).jpg")

                        

                try:
                        os.remove(f"item{formatted_id} ({p}).jpg")
                except:
                        pass


                

princess_polly_scraper("https://us.princesspolly.com/collections/dresses", 20, "Female", "Dresses", "Princess Polly")
                



        
