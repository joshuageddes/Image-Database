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


def zara_scraper(link, num_pages, gender, item_type, brand):

    id_count = 0
    
    item_id = ["ww", "xx", "yy", "zzzz"]
    brand_dict = {"Zara" : "04"}
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

    recent_links = []




    

    browser.get(f'{link}')

    time.sleep(20)
    #time to set view
    print('ready!')


    item_count = len(browser.find_elements_by_class_name('product-grid-product'))


    for i in range(1, item_count+1) :

        run_script = True

        try:
            item_link = browser.find_element_by_xpath(f'/html/body/div[2]/div[1]/div[1]/div/div/div[2]/main/article/div[2]/section[1]/ul/li[{i}]/div[1]/div/div/div/a').get_attribute('href')

            if item_link in recent_links :
                run_script = False

            
        except:
            try:
                item_link = browser.find_element_by_xpath(f'/html/body/div[2]/div[1]/div[1]/div/div/div[2]/main/article/div[2]/section[1]/ul/li[{i}]/a').get_attribute('href')

                if item_link in recent_links :
                    run_script = False
            except:
                run_script = False


        if len(recent_links) > 10:
            recent_links.pop(0)
            


        
        



        

        

        if run_script :

            recent_links.append(item_link)

            id_count +=1

            browser.execute_script(f'window.open("{item_link}","_blank");')
            browser.switch_to.window(browser.window_handles[1])

            time.sleep(1)



            #item_name

            item_name = browser.find_element_by_class_name('product-detail-info__name').text


            #item_price

            item_price = browser.find_element_by_class_name('price__amount-current').text

            #item_color

            try:
                    color = browser.find_element_by_xpath('/html/body/div[2]/div[1]/div[1]/div/div/div[2]/main/article/div[1]/div[2]/div[1]/p').text

                    color = color.split(' ')

                    item_color = color[1]

            except:
                item_color = "Unknown"

            

            formatted_id = item_id[:-1]
            formatted_id.append(str(id_count))
            formatted_id = "".join(formatted_id)

            

            try:
                        data.insert_row([f"{formatted_id}", f"{item_name}", f"{item_link}",
                                 f"{item_price}", f"{item_color}", gender, item_type, brand, i], id_count+21605)
            except:
                        time.sleep(30)
                        data.insert_row([f"{formatted_id}", f"{item_name}", f"{item_link}",
                                 f"{item_price}", f"{item_color}", gender, item_type, brand, i], id_count+21605)

            time.sleep(1)



            #item_pictures
            
            pic_count = len(browser.find_elements_by_xpath('/html/body/div[2]/div[1]/div[1]/div/div/div[2]/main/article/div[1]/div[1]/section/div/ul/li'))



            for p in range (1, pic_count):

                try:

                    

                    picture = browser.find_element_by_xpath(f'/html/body/div[2]/div[1]/div[1]/div/div/div[2]/main/article/div[1]/div[1]/section/div/ul/li[{p}]/button/div/div/img')
                    

                    src = picture.get_attribute('src')

                    urllib.request.urlretrieve(src, f"item{formatted_id} ({p}).jpg")
                    upload_file_(f"item{formatted_id} ({p}).jpg")

                        

                    try:
                            os.remove(f"item{formatted_id} ({p}).jpg")
                    except:
                            pass

                
                except:
                    pass
            
            browser.close()
            browser.switch_to.window(browser.window_handles[0])

            
        
zara_scraper("https://www.zara.com/ca/en/woman-dresses-l1066.html", 1, "Female", "Dresses", "Zara")



