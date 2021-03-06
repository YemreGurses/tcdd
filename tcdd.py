from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from win10toast import ToastNotifier
from datetime import datetime
from platform import system
import time
import os

path = os.getcwd()
path += '/chromedriver'
driver = webdriver.Chrome(path)

string0 = 'Konya YHT'
string1 = 'ERYAMAN YHT'
date = '16.10.2020' #Gidis tarihi eger bugunse None, degilse '22.11.2019' formatinda yaz
fullness = '2' #Kapasite bu sayidan farkli olursa bana bildirim at
hour = '18:15' #Sefer saati format '14:35'
# index = 5 #Sefer listesinde trenin gozuktugu sira

def notify_mac(title, text):
    os.system("""
              osascript -e 'display notification "{}" with title "{}" sound name "default"'
              """.format(text, title))

def notify_windows(title, text):
    toast = ToastNotifier()
    toast.show_toast(title,text,duration=20)

i = 0
while True:
    try:
        driver.get("https://ebilet.tcddtasimacilik.gov.tr/view/eybis/tnmGenel/tcddWebContent.jsf")
        os_type = system()
        wait = WebDriverWait(driver, 10)

        from_x = '//*[@id="nereden"]'
        from_box = wait.until(EC.presence_of_element_located((By.XPATH, from_x)))
        from_box.clear()
        from_box.send_keys(string0)

        to_x = '//*[@id="nereye"]'
        to_box = wait.until(EC.presence_of_element_located((By.XPATH, to_x)))
        to_box.clear()
        to_box.send_keys(string1)

        if date:
            date_x = '//*[@id="trCalGid_input"]'
            date_box = wait.until(EC.presence_of_element_located((By.XPATH, date_x)))
            date_box.clear()
            date_box.send_keys(date)

            date_close_x = '//*[@id="ui-datepicker-div"]/div[2]/button[2]'
            date_close_button = wait.until(EC.presence_of_element_located((By.XPATH, date_close_x)))
            date_close_button.click()

            time.sleep(1)

        #Ornek kapasite yazanin listesi
        # //*[@id="mainTabView:gidisSeferTablosu:0:j_idt105:0:somVagonTipiGidis1_label"]
        # //*[@id="mainTabView:gidisSeferTablosu:1:j_idt105:0:somVagonTipiGidis1_label"]
        # //*[@id="mainTabView:gidisSeferTablosu:2:j_idt105:0:somVagonTipiGidis1_label"]
        
        #Ornek sefer saati listesi
        # //*[@id="mainTabView:gidisSeferTablosu_data"]/tr[1]/td[1]/span
        # //*[@id="mainTabView:gidisSeferTablosu_data"]/tr[2]/td[1]/span
        # //*[@id="mainTabView:gidisSeferTablosu_data"]/tr[3]/td[1]/span

        search = '//*[@id="btnSeferSorgula"]'
        search_box = wait.until(EC.presence_of_element_located((By.XPATH, search)))
        search_box.click()

        time.sleep(5)
        
        trip_table_x = '//*[@id="mainTabView:gidisSeferTablosu_data"]'
        trip_table =  driver.find_element_by_xpath(trip_table_x)
        
        for it, row in enumerate(trip_table.find_elements_by_xpath(".//tr/td[1]/span")):
            if hour == row.text:
                index = it
        
        trip_capacity_x = '//*[@id="mainTabView:gidisSeferTablosu:{}:j_idt109:0:somVagonTipiGidis1_label"]'.format(str(index))
        #xpath degisebiliyor kontrol et
        trip_capacity = wait.until(EC.presence_of_element_located((By.XPATH, trip_capacity_x)))
        
        # trip_hour_x = '//*[@id="mainTabView:gidisSeferTablosu_data"]/tr[{}]/td[1]/span'.format(str(index+1))
        # trip_hour = wait.until(EC.presence_of_element_located((By.XPATH, trip_hour_x)))

        capa = trip_capacity.text.split(' ')[-1]
        capacity = capa.replace('(','').replace(')','')
        if capacity != fullness:
            if os_type == "Windows":
                notify_windows("Tren boşaldı", "HEMEN BİLETİNİ KAP")
            elif os_type == "Darwin":
                notify_mac("Tren boşaldı", "HEMEN BİLETİNİ KAP")
            # elif os_type == "Linux":
                #TO-DO
                #notify_linux() 
            else:
                print("Error: Couldnt get OS information")
            now = datetime.now()
            print(capacity + " - Time: " + now.strftime("%m/%d/%Y, %H:%M:%S"))
            
        i += 1
    except Exception as exc:
        print(exc)
        continue
