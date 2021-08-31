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

data = client.open("Apollo_Data_Test").worksheet('NewData')


opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
urllib.request.install_opener(opener)


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


def lucy_scraper(link, num_pages, gender, item_type, brand):

    id_count = 656
    
    item_id = ["ww", "xx", "yy", "zzzz"]
    brand_dict = {"Lucy in the Sky" : "04"}
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
    
    browser = webdriver.Chrome(options=options)
    browser.set_window_size(1920, 1080)
    browser.maximize_window()


    item_color = ""
    item_price = ""
    item_name = ""
    item_link = ""
    run_script = True

    for page in range (2, num_pages+1):
        browser.get(f"{link}?page={page}")

        item_count = len(browser.find_elements_by_xpath('/html/body/div[1]/div/div[3]/div[3]/div'))


        for i in range (1, item_count+1):

            


            #item link

            try:
                item_link = browser.find_element_by_xpath(f'/html/body/div[1]/div/div[3]/div[3]/div[{i}]/a').get_attribute('href')

            
                run_script = True
            
            except:
                run_script = False

            

            if run_script :

                id_count +=1

                browser.execute_script(f'window.open("{item_link}","_blank");')
                browser.switch_to.window(browser.window_handles[1])

                time.sleep(1)


                #item name

                try:
                    item_name = browser.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div[2]/h1').text

                except:
                    item_name = 'Unknown'

                #item price

                try:
                    item_price = browser.find_element_by_xpath('/html/body/div[1]/div/div/div[1]/div[2]/div[2]/p[2]').text

                except:
                    item_price = 'Unknown'

                #item color


                if item_name != 'Unknown':
                    color = item_name.split(' ')
                    item_color = color[-1]

                else:
                    item_color = 'Unknown'


                formatted_id = item_id[:-1]
                formatted_id.append(str(id_count))
                formatted_id = "".join(formatted_id)

            

                try:
                        data.insert_row([f"{formatted_id}", f"{item_name}", f"{item_link}",
                                 f"{item_price}", f"{item_color}", gender, item_type, brand, i], id_count+22472)
                except:
                        time.sleep(30)
                        data.insert_row([f"{formatted_id}", f"{item_name}", f"{item_link}",
                                 f"{item_price}", f"{item_color}", gender, item_type, brand, i], id_count+22472)
                

                time.sleep(1)


                #pic_count = len(browser.find_elements_by_xpath('/html/body/div[1]/div/div/div[1]/div[1]/div[1]/div[2]/div[1]/div/div[2]/div/div/div'))

                pictures = browser.find_elements_by_class_name('img-fluid')

                pic_count=1

                

                for p in pictures:

                    try:

                        

                        

                        src = p.get_attribute('src')

                        urllib.request.urlretrieve(src, f"item{formatted_id} ({pic_count}).jpg")
                        upload_file_(f"item{formatted_id} ({pic_count}).jpg")
                        

                            

                        try:
                                os.remove(f"item{formatted_id} ({pic_count}).jpg")
                        except:
                                pass

                        pic_count+=1

                    except:
                        pass
                
                browser.close()
                browser.switch_to.window(browser.window_handles[0])

lucy_scraper("https://www.lucyinthesky.com/shop/all-clothes", 42, "Female", "Dresses", "Lucy in the Sky")

