import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time 
from selenium.webdriver.common.by import By
import re

s = Service('D:\\chromedriver.exe')
driver = webdriver.Chrome(service=s)
print('start scrapping')
baseurl = 'https://www.tripadvisor.com'
print('init baseurl')
url = 'https://www.tripadvisor.com/Restaurants-g297546-Arish_Red_Sea_and_Sinai.html'
city = "Arish"
print('init header')
headeers = {'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36'}
print('init reaponse')
response = requests.get(url,headers=headeers)
print('init soap')
soup = BeautifulSoup(response.content, 'html.parser')
attraction_links = []
# Scrap Links
driver.get(url)
pages_to_scrape = 2
for i in range(0, pages_to_scrape):
    time.sleep(22)
    container = driver.find_elements(By.XPATH,".//div[contains(@class, 'dzomp u F f Ff K')]")
    print(len(container))
    for j in range(len(container)):
        print('scrape link')
        link = container[j].find_element(By.XPATH,".//a")
        attraction_links.append(link.get_attribute("href"))
        print(len(attraction_links))
    try:
        driver.find_element(By.XPATH,'.//a[@class="nav next rndBtn ui_button primary taLnk"]').click()
    except:
        break
print(len(attraction_links))

k = 1
restaurantdata=[]

for link in attraction_links:
  
    print('visiting the url',k)
    print(link)
    driver.get(link)
    data = BeautifulSoup(driver.page_source,'lxml')

    # scrape name
    print('Scrape Name')
    try:
        name_div = data.find('div', {'class', 'eTnlN _W w O'})
        name = name_div.find('h1', {'class': 'fHibz'}).text.strip()
    except:
        name_div = 'None'
        name = 'None'
    print(name)

    # review number
    print('Scrape review num')
    try:
        reviewnum_a = data.find('a', {'class', 'iPqaD _F G- ddFHE eKwUx'})
        reviewnum = reviewnum_a.find('span', {'class', 'eBTWs'}).text.strip()

    except:
        reviewnum = 'None'
    print(reviewnum)

    # scrape address
    print('Scrape address value')
    try:
        address_div = data.find_all('div', {'class','eSAOV H3'})
        for item in address_div[1:]:
            address = item.find('a',{'class','fhGHT'}).text
    except:
        address = 'None'
    print(address)

    # scarpe telephone
    print('Scrape telephone value')
    try:
        tel_span = data.find('span', {'class', 'fhGHT'})
        telephone = tel_span.find('a', {'class', 'iPqaD _F G- ddFHE eKwUx'}).text
    except:
        telephone = 'None'
    print(telephone)

    # scrap menu 
    print("scrape menu ")
    try:
        menu_span = data.find('span',{'class','dyeJW dUpPX fnEzc'})
        menu = menu_span.find('a',{'class','dOGcA Ci Wc _S C fhGHT'})
        menu = menu["href"]
    except:
        menu = 'None'
    print(menu)

    # scrape rate
    print('scrape rate value')
    try:
        rate_div = driver.find_element(By.XPATH,".//div[contains(@class, 'eEwDq')]")
        rate = rate_div.find_element(By.XPATH,".//span[contains(@class, 'fdsdx')]").text.strip()
    except:
        rate = 'None'
    print(rate)

    # scrape working hours
    print('scrape working hours')
    try:
        working_link = driver.find_element(By.XPATH,".//div[contains(@class, 'dauAM')]")
        working_link.click()
        data_update = BeautifulSoup(driver.page_source,'lxml')
        working_div = data_update.find('div',{'class':'cBtAm Za f e'})
        if working_div != None:
            working_hours = data_update.find('div',{'class':'cFfqI'}).text
    except:
        working_hours = 'None'
    print(working_hours)

    # scrape details
    print('Scrape details')
    about = 'None'
    price_range = 'None'
    cuisines = 'None'
    special_diets = 'None'
    meals = 'None'
    features = 'None'
    try:
        expand_link = driver.find_element(By.XPATH,".//a[contains(@class, 'ZlyLX _S b')]")
        # case 1 : pop up details
        if expand_link != None:
            print('link exist')
            expand_link.click()
            data_update = BeautifulSoup(driver.page_source,'lxml')
            find_divs = data_update.find('div',{'class':'dQSnI _Z S2 H2 _f'}) 
            find_ui_column = find_divs.find_all('div',{'class':'ui_column'})
            for i in range(len(find_ui_column)):
                print('scrape about')
                try:
                    find_about = find_ui_column[i].find('div',{'class':'cHXJo _Z'})
                    find_about = find_about.find('div',{'class':'OMpFN'})
                    about = find_about.text.strip()
                except:
                    find_about = 'None'
                try:
                    find_title = find_ui_column[i].find_all('div',{'class':'dMshX b'})
                    for item in find_title:
                        if item.text == "PRICE RANGE":
                            print('scrape price range')
                            price_range = item.find_next('div',{'class':'cfvAV'}).text.strip()
                        elif item.text == "CUISINES":
                            print('scrape cuisines')
                            cuisines = item.find_next('div',{'class':'cfvAV'}).text.strip()
                        elif item.text == "Special Diets":
                            print('scrape special diets')
                            special_diets = item.find_next('div',{'class':'cfvAV'}).text.strip()
                        elif item.text == "Meals":
                            print('scrape meals')
                            meals = item.find_next('div',{'class':'cfvAV'}).text.strip()
                        elif item.text == "FEATURES":
                            print('scrape features')
                            features = item.find_next('div',{'class':'cfvAV'}).text.strip()
                except:
                    find_title = 'None'
    # case 2: details in page        
    except:
        try:
            start = data.find('div',{'class','cfPdu'})
            parent_ui = start.find_all('div',{'class','ui_column'})
            for item in parent_ui:
                try:
                    print('scrape about')
                    about_div = item.find('div',{'class':'byxOG Z _Z PU'})
                    try:
                        about_div.find_next('div', {'class', 'epsEZ'}).click()
                    except:
                        click='None'
                    about = about_div.find('div',{'class':'epsEZ'}).text.strip()
                except:
                    about_div = 'None'
                try:
                    title_label = item.find_all('div',{'class':'csKes Wf b'})
                    for each in title_label:
                        if (each.text == "PRICE RANGE"):
                            print('scrape price range')
                            price_range = each.find_next('div',{'class':'bYIkW'}).text.strip()
                        elif (each.text == "Special Diets"):
                            print('scrape special diets')
                            special_diets = each.find_next('div',{'class':'bYIkW'}).text.strip()
                        elif (each.text == "Meals"):
                            print('scrape meals')
                            meals = each.find_next('div',{'class':'bYIkW'}).text.strip()
                        elif (each.text == "CUISINES"):
                            print('scrape cuisines')
                            cuisines = each.find_next('div',{'class':'bYIkW'}).text.strip()
                        elif (each.text == "FEATURES"):
                            print('scrape features')
                            features = each.find_next('div',{'class':'bYIkW'}).text.strip()
                except:
                    title_label = 'None'
        except:
            print('No details')
    print(about)
    print(price_range)
    print(cuisines)
    print(special_diets)
    print(meals)
    print(features)

    # scrape images
    time.sleep(5)
    print('Scrape images')
    images = []
    try:
        try:
            imgs_div_large = driver.find_elements(By.XPATH,".//div[contains(@class, 'large_photo_wrapper')]")
            for i in range(len(imgs_div_large)):
                img_src = imgs_div_large[i].find_element(By.XPATH,".//img[contains(@class, 'basicImg')]").get_attribute("src")
                print('Collecting images')
                images.append(img_src)
        except:
            images = []
        try:   
            imgs_div_mini = driver.find_elements(By.XPATH,".//div[contains(@class, 'mini_photo_wrap')]")
            for i in range(len(imgs_div_mini)):
                img_src = imgs_div_mini[i].find_element(By.XPATH,".//img[contains(@class, 'basicImg')]").get_attribute("src")
                print('Collecting images')
                if "https" in img_src != None:
                    if "photo-f" in img_src:
                        img_src = img_src.replace("photo-f","photo-s")
                    images.append(img_src)
        except:
            images = []
        if images == []:
            print('No images found')
            images = 'None'
    except:
        img_src = 'Nonne'
        images = 'None'
    print(images)

    #scrape reviews 
    print('scrape reviews')
    restaurants_reviews=[]
    try:
        pages_to_scrape = 2
        for i in range(0, pages_to_scrape):
            time.sleep(22)
            print('scrape page',i+1)
            try:
                driver.find_element(By.XPATH,".//span[contains(@class,'taLnk ulBlueLinks')]").click()
            except:
                click = 'None'      
            time.sleep(10)
            container = driver.find_elements(By.XPATH,".//div[contains(@class,'rev_wrap ui_columns is-multiline')]")
            for j in range(len(container)):
                print('scrape rate')
                try: 
                    review_rate = container[j].find_element(By.XPATH,".//span[contains(@class, 'ui_bubble_rating')]").get_attribute("class")
                    review_rate = review_rate.replace('ui_bubble_rating bubble_','')
                    review_rate = re.sub(r'(?<!^)(?=(\d{1})+$)', r'.',review_rate)+' of 5 bubbles' 
                except:
                    review_rate = 'None'
                print('scrape title')
                try:
                    title_div = container[j].find_element(By.XPATH,".//div[contains(@class,'quote')]")
                    title = title_div.find_element(By.XPATH,".//span[contains(@class,'noQuotes')]").get_attribute("textContent")
                except:
                    title = 'None'
                print('scrape review body')
                try:
                    review_div = container[j].find_element(By.XPATH,".//div[@class='entry']")
                    review = review_div.find_element(By.XPATH,".//p[contains(@class,'partial_entry')]").get_attribute("textContent").replace("\n", "  ")
                except:
                    review = 'None'
                print('scrape profile name')
                try:
                    profile_name = container[j].find_element(By.XPATH,".//div[contains(@class,'info_text pointer_cursor')]")
                    try:
                        extra = profile_name.find_element(By.XPATH,".//div[contains(@class,'userLoc')]").get_attribute("textContent")
                        profile_name = profile_name.get_attribute("textContent").replace(extra,"").rstrip()
                    except:  
                        profile_name = profile_name.get_attribute("textContent")
                except: 
                    profile_name = 'None'         
                print('scrape date of visit ')
                try:
                    date_of_visit = container[j].find_element(By.XPATH,".//div[contains(@class,'prw_rup prw_reviews_stay_date_hsx')]").get_attribute("textContent")
                    date_of_visit=date_of_visit.replace("Date of visit: ","")
                except:
                    date_of_visit = 'None'
                print('scrape Reviewed date')
                try:
                    reviewed_date = container[j].find_element(By.XPATH,".//span[contains(@class,'ratingDate')]").get_attribute("textContent").replace("Reviewed ","")
                except:
                    reviewed_date = 'None'
                restaurant_review = {
                    'profilename': profile_name,
                    'date_of_review': reviewed_date,
                    'rate': review_rate,
                    'title': title,
                    'review': review,
                    'date_of_visit': date_of_visit
                    }
                restaurants_reviews.append(restaurant_review) 
            
            try:
                driver.find_element(By.XPATH,'.//a[@class="nav next ui_button primary"]').click()
            except:
                break
    except:
        restaurants_reviews = 'None' 


    print('creating object')
    restaurant = {
        'city': city,
        'name': name,
        'address': address,
        'reviewnum': reviewnum,
        'rate': rate,
        'workinghours': working_hours,
        'telephone': telephone,
        'menu-link': menu,
        'about': about,
        'price-range': price_range,
        'cuisines': cuisines,
        'special-diets': special_diets,
        'meals': meals,
        'features': features,
        'images': images,
        'attractionreview': restaurants_reviews
        }

    restaurantdata.append(restaurant)
    print('saving: ', restaurant['name'])
    k+=1


print('creating pd')
df = pd.DataFrame(restaurantdata)
df.to_excel(f'{city} restaurant.xlsx')
print(df)


    