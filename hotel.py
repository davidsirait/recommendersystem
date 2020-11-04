from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time

# menjalankan selenium dengan metode headless 
options = Options()
options.headless = True
driver = webdriver.Chrome(executable_path="static/chromedriver",options=options)

# list dari alamat url yang akan di crawl
list_url=['https://www.pegipegi.com/hotel/jakarta/daftar-alamat-hotel.html']
for i in range(2,17):
    url = 'https://www.pegipegi.com/hotel/jakarta/daftar-alamat-hotel' + '-' + str(i) + '.html'
    list_url.append(url)
print(list_url)

# list kosong untuk menampung nama dan kota lokasi hotel 
hotel_name = []
hotel_city = []


for html in list_url:
    driver.get(html)
    content = driver.page_source
    soup = BeautifulSoup(content)
    for a in soup.find_all('div',attrs={'class':'listContent','itemprop':'itemListElement'}):

        name = a.find('div',attrs={'class':'title'})
        for span in name('span'):
            span.decompose()
        hotel_name.append(name.get_text(strip=True))

        city = a.find('div',attrs={'class':'address'})
        for span in city('span'):
            span.decompose()
        hotel_city.append(city.get_text(strip=True))
    time.sleep(1)
driver.quit()

# memasukkan data nama hotel dan lokasi kota ke dalam dataframe
df = pd.DataFrame({'Hotel Name':hotel_name,'City':hotel_city})
df['Kota'] = df['City'].str.split(',',expand=True)[0]
df = df.drop(columns="City")

# simpan ke dalam file .csv
df.to_csv('Hotel Name.csv',index=True,encoding='utf-8')

