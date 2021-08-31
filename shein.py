

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




def shein_scraper(link, num_pages, gender, item_type, brand):

    id_count = 5150
    
    item_id = ["ww", "xx", "yy", "zzzz"]
    brand_dict = {"Shein" : "02"}
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

    item_count_ = 0

    placeholder = 62



    for page in range(14, num_pages+1):

        browser.get(f"{link}&page={page}")

        item_count = len(browser.find_elements_by_xpath(
            f'/html/body/div/div/div[2]/div[2]/section/div/section'))



        if page == 15:
            placeholder = 1


        
        

      


        for i in range(placeholder, item_count+1):

            try:
                sublink = browser.find_element_by_xpath(
                    f'/html/body/div/div/div[2]/div[2]/section/div/section[{i}]/div/a').get_attribute('href')





                browser.execute_script(f'window.open("{sublink}","_blank");')
                browser.switch_to.window(browser.window_handles[1])

                item_count_ +=1


                #click on x if color not accessible
                try :
                    browser.find_element_by_xpath(f'/html/body/div[1]/div[3]/div[1]/div/div/i').click()

                except:
                    pass



                colors = browser.find_elements_by_class_name('product-intro__color-radio')


                

               




                if len(colors) == 0 :

                    item_color = "No Color"
                    item_name = browser.find_element_by_class_name('product-intro__head-name').text
                    item_price = browser.find_element_by_class_name('product-intro__head-price').text[2:]
                        
                    #try:
                    #    item_price = browser.find_element_by_xpath(
                    #    '/html/body/div[1]/div[1]/div/div[1]/div/div[2]/div[2]/div/div[1]/div[3]/div/div/span').text[2:]
                        
                    #except:
                     #   item_price = "Unknown"
                            
                    item_link = browser.current_url
                    id_count += 1

                    formatted_id = item_id[:-1]
                    formatted_id.append(str(id_count))
                    formatted_id = "".join(formatted_id)

                    
                    try:
                        data.insert_row([f"{formatted_id}", f"{item_name}", f"{item_link}",
                                 f"{item_price}", "No Color", gender, item_type, brand, i], id_count)
                    except:
                        time.sleep(30)
                        data.insert_row([f"{formatted_id}", f"{item_name}", f"{item_link}",
                                 f"{item_price}", "No Color", gender, item_type, brand, i], id_count)
                        

                    time.sleep(1)

                    image_count = len(browser.find_elements_by_xpath(
                            '/html/body/div[1]/div[1]/div/div[1]/div/div[2]/div[1]/div[1]/div[1]/div/div'))

                    


                    for j in range (1, image_count+1):

                            
                        src = browser.find_element_by_xpath(
                            f'/html/body/div[1]/div[1]/div/div[1]/div/div[2]/div[1]/div[1]/div[1]/div/div[{j}]/img').get_attribute('src')

                        urllib.request.urlretrieve(src, f"item{formatted_id} ({j}).jpg")
                        upload_file_(f"item{formatted_id} ({j}).jpg")

                        

                        try:
                                os.remove(f"item{formatted_id} ({j}).jpg")
                        except:
                                pass


                        



                        
                        

                    
                    
                    
                else :
                    for c in colors:

                        
                        
                        c.click()
                        time.sleep(1)
                        

                        
                        item_color = c.get_attribute('aria-label')
                        item_name = browser.find_element_by_class_name('product-intro__head-name').text
                        
                       #    item_price = browser.find_element_by_xpath(
                        #    '/html/body/div[1]/div[1]/div/div[1]/div/div[2]/div[2]/div/div[1]/div[3]/div/div/span').text[2:]
                            
                        #except:
                        #    item_price = "Unknown"

                        item_price = browser.find_element_by_class_name('product-intro__head-price').text[2:]
                            
                        item_link = browser.current_url
                        id_count += 1
                        formatted_id = item_id[:-1]
                        formatted_id.append(str(id_count))
                        formatted_id = "".join(formatted_id)

                        try:
                            data.insert_row([f"{formatted_id}", f"{item_name}", f"{item_link}",
                                 f"{item_price}", f"{item_color}", gender, item_type, brand, i], id_count)
                        except:
                            time.sleep(30)
                            data.insert_row([f"{formatted_id}", f"{item_name}", f"{item_link}",
                                 f"{item_price}", f"{item_color}", gender, item_type, brand, i], id_count)

                        

                        

                        
                        
                        

                        image_count = len(browser.find_elements_by_xpath(
                            '/html/body/div[1]/div[1]/div/div[1]/div/div[2]/div[1]/div[1]/div[1]/div/div'))

                        for j in range (1, image_count+1):

                            
                            src = browser.find_element_by_xpath(
                            f'/html/body/div[1]/div[1]/div/div[1]/div/div[2]/div[1]/div[1]/div[1]/div/div[{j}]/img').get_attribute('src')

                            urllib.request.urlretrieve(src, f"item{formatted_id} ({j}).jpg")
                            upload_file_(f"item{formatted_id} ({j}).jpg")

                            

                            try:
                                os.remove(f"item{formatted_id} ({j}).jpg")
                            except:
                                pass





                            

                        

            


                


                

                    


                    
                    
                

                browser.close()
                browser.switch_to.window(browser.window_handles[0])

            except:
                browser.close()
                browser.switch_to.window(browser.window_handles[0])
    





shein_scraper("https://ca.shein.com/women-dresses-c-1727.html?sort=7", 40, "Female", "Dresses", "Shein")
        

        
        

    




    


