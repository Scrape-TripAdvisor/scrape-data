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
url = 'https://www.tripadvisor.com/Attractions-g488093-Activities-Dakhla_New_Valley_Governorate.html'
city = "Dakhla"
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
    print('scrape page',i+1)
    container = driver.find_elements(By.XPATH,".//header[contains(@class, 'fFeLV P0')]")
    for j in range(len(container)):
        print('scrape link')
        link = container[j].find_element(By.XPATH,".//a")
        print(link.get_attribute("href")) 
        attraction_links.append(link.get_attribute("href"))
    try:
        driver.find_element(By.XPATH,'.//a[@class="dfuux u j z _F ddFHE bVTsJ emPJr"]').click()
    except:
        break
print(len(attraction_links))
k=1
attractiondata=[]
for link in attraction_links:
  
    print('visiting the url',k)
    print(link)
    driver.get(link)
    data = BeautifulSoup(driver.page_source,'lxml')
    # scrape name
    print('Scrape Name')
    try:
        name_div = data.find('div',{'class','Xewee'})
        if name_div != None:  
            name = name_div.find('h1',{'class':'WlYyy cPsXC GeSzT'}).text.strip()
        else:
            name_div = data.find('div',{'class','bRRXe'})
            name = name_div.find('h1',{'id':'HEADING'}).text.strip()
    except:
        name_div = 'None'
        name = 'None'
    print(name)

    # review number
    print('Scrape review num')
    try:
        reviewnum_span = data.find('span',{'class','WlYyy diXIH bGusc dDKKM'})
        if reviewnum_span != None:
            reviewnum = reviewnum_span.find('span',{'class','cfIVb'}).text.strip() + " reviews"
        else:
            reviewnum = data.find('span',{'class','reviewCount siNVx S4 H3 Ci'}).text.strip()
    except:    
        reviewnum = 'None'
    print(reviewnum)

        
    #working hours
    print('Scrape working hours')
    try:
        workinghours_div=data.find('div',{'class','WlYyy diXIH dTqpp'})
        workinghours=workinghours_div.find('span',{'class','cOXcJ'}).text.strip()
    except: 
        try:
            workinghours_div_2=data.find('div',{'class','ezoMm'})
            more_div=workinghours_div_2.find('div',{'class','zsdhl _S'}) 
            workinghours=more_div.find_previous('div').text.strip().replace('Hours Today: ','')

        except: 
          workinghours = 'None'    
    
    print(workinghours)
        
    #type
    print('Scrape type of attraction')
    try:
        type_div = data.find('div',{'class','hxQKk'})
        if type_div != None:
            for item in type_div:
                find_div = item.find('div',{'class','WlYyy diXIH dDKKM'})
                if find_div != None:
                    typeofattraction = find_div.text.strip()
                else:
                    typeofattraction = 'N'
        else:
            driver.find_element(By.XPATH,".//a[contains(@class,'baeGv _S')]").click()
            typeofattraction = driver.find_element(By.XPATH,".//div[contains(@class,'bpIfl d S4')]").text
    except:    
        typeofattraction = 'None'
    print(typeofattraction)

       
    # about
    print('Scrape About')
    try:
        about_div = data.find('div',{'class','dCitE _d MJ'})
        if about_div != None:
            about = about_div.find('div',{'class','WlYyy diXIH dDKKM'}).text.strip()
        else:
            about_div = data.find('div',{'class','duhwe _T bOlcm dMFkS dMbup'})
            if about_div != None:
                about = about_div.find('div',{'class','pIRBV _T'}).text.strip()
            else:
                about_div = data.find('div',{'class','duhwe _T bOlcm dMFkS'})
                about = about_div.find('div',{'class','pIRBV _T'}).text.strip()
    except:    
        about = 'None'
    print(about)
        

   #suggested duration
    print('Scrape suggested duration')
    try:
        suggestedduration_div=data.find_all('div',{'class','WlYyy cPsXC cspKb dTqpp'})
        suggestedduration = 'None'
        for item in suggestedduration_div:
            if (item.text =="Suggested duration"):
                suggestedduration=item.find_next('div',{'class','egjOk _c'}).text.strip()   
    except:    
        suggestedduration = 'None'
        
    #rate
    print('Scrape rate')
    try:
        rate_div=data.find('div',{'class','bHUDR f u j'})
        rate=rate_div.find('div',{'class','WlYyy cPsXC fksET cMKSg'}).text.strip()
        
    except:    
        rate = 'None'

    # scrape address
    print('Scrape address value')
    try:
        address_button = data.find('button',{'class','bfQwA _G B- _S _T c G_ P0 ddFHE cnvzr bTBvn'})
        address=address_button.find('span',{'class','WlYyy cacGK Wb'}).text
    except:
     try:
        address = data.find('div',{'class':'dIDBU MJ'}).text.strip()
        replace_vlaue = data.find('div',{'class':'NwwFk'}).text.strip()
        if replace_vlaue == None:
            address = address.replace("Address",'')
        else:
            address = address.replace(replace_vlaue,'')
     except:
         try:
          address = data.find('div',{'class':'dIDBU MJ'}).text.strip()
         except:
          address = 'None'

    # scrape images
    print('Scrape image value')
    time.sleep(5)
    images = []
    try:  
        if data.find('div',{'class','bRRXe'}) == None:
            img_div = data.find_all('div',{'class':'eMVst _R w _Z GA'})
            if img_div != None:
                substring = "photo-l"
                for i in range(len(img_div)):
                    print('Collecting image')
                    item_style = img_div[i]['style']
                    item_style = item_style[item_style.rfind("https"):]
                    img_url = item_style[:item_style.rfind(')')]
                    if substring in img_url:
                        img_url = img_url.replace(substring,"photo-o")
                    images.append(img_url)
        else:
            print( 'in else')
            img_div = data.find_all('div',{'class':'qiziU'})
            if img_div != None:
                for i in range(len(img_div)):
                    print('Collecting image')
                    item_style = img_div[i]['style']
                    item_style = item_style[item_style.rfind("https"):]
                    img_url = item_style[:item_style.rfind('"')]
                    images.append(img_url)
            try:
                for i in range(1,5):
                    driver.find_element(By.XPATH,".//div[contains(@class,'fBqFV X0 _S blQNt _U')]").click()
                img_div = driver.find_elements(By.XPATH,".//div[contains(@class,'qiziU')]")
                if img_div != None:
                    for i in range(len(img_div)):
                        print('Collecting image')
                        item_style = img_div[i].get_attribute("style")
                        item_style = item_style[item_style.rfind("https"):]
                        img_url = item_style[:item_style.rfind('"')]
                        images.append(img_url)
            except:
                images = images     
    except:
        img_div = 'None'
        images = 'None'
    print(images)

    attraction_reviews=[]
    #scrape reviews
    try:
        pages_to_scrape = 2
        for i in range(0, pages_to_scrape):
            time.sleep(22)
            print('scrape page',i+1)
            try:
                click = driver.find_element(By.XPATH,".//div[contains(@class,'duhwe _T bOlcm dMbup')]")
                print('click 1')
                try:
                    click.find_element(By.XPATH,".//div[contains(@class,'pIRBV _T')]").click()
                    print('click 1.1')
                except:
                    click.find_element(By.XPATH,".//div[contains(@class,'eIVRK')]").click()
                    print('click 1.2')
            except:
                click = 'None'
            container = driver.find_elements(By.XPATH,".//div[contains(@data-automation,'reviewCard')]")
            if (container==None or container==[]):
                container = driver.find_elements(By.XPATH,".//div[contains(@class,'eVykL Gi z cPeBe MD cwpFC')]")
            print(container)

            for j in range(len(container)):

                print('scrape rate')
                try: 
                    review_rate_div = container[j].find_element(By.XPATH,".//*[local-name()='svg' and @class='RWYkj d H0']")
                    review_rate = review_rate_div.get_attribute("title")
                except:
                    try:
                        review_rate_div_2=container[j].find_element(By.XPATH,".//div[contains(@data-test-target, 'review-rating')]")
                        review_rate=review_rate_div_2.find_element(By.XPATH,".//span[contains(@class, 'ui_bubble_rating')]").get_attribute("class")
                        review_rate=review_rate.replace('ui_bubble_rating bubble_','')
                        review_rate=re.sub(r'(?<!^)(?=(\d{1})+$)', r'.',review_rate)+' of 5 bubbles'    
                    except:
                        review_rate='None'
                print('scrape title')
                try:
                    title_div = container[j].find_element(By.XPATH,".//div[contains(@class, 'WlYyy cPsXC bLFSo cspKb dTqpp')]")
                    title=title_div.find_element(By.XPATH,".//a[contains(@class,'iPqaD _F G- ddFHE eKwUx btBEK fUpii')]").text
                except:
                    try:
                     title_div_2=container[j].find_element(By.XPATH,".//div[contains(@data-test-target, 'review-title')]")
                     title=title_div_2.find_element(By.XPATH,".//a[contains(@class, 'fCitC')]").text
                    except:
                     title = 'None'
                print('scrape review body')
                try:
                    parent_div = container[j].find_element(By.XPATH,".//div[@class='pIRBV _T KRIav']")
                    review_div=parent_div.find_element(By.XPATH,".//div[@class='WlYyy diXIH dDKKM']")
                    review=review_div.find_element(By.XPATH,".//span[@class='NejBf']").text.replace("\n", "  ")
                except:
                    try:
                     review=container[j].find_element(By.XPATH,".//q[@class='XllAv H4 _a']").text.replace("\n", "  ")  
                    except:
                     review = 'None'
                print('scrape profile name')
                try:
                    profilename_div = container[j].find_element(By.XPATH,".//span[contains(@class,'WlYyy cPsXC dTqpp')]")
                    profile_name=profilename_div.find_element(By.XPATH,".//a[contains(@class,'iPqaD _F G- ddFHE eKwUx btBEK fUpii')]").text
                except: 
                    try:    
                     profile_name=container[j].find_element(By.XPATH,".//a[contains(@class,'ui_header_link bPvDb')]").text     
                    except:
                     profile_name = 'None'
                print('scrape Time and Type of Trip')
                try:
                    time_and_typeoftrip = container[j].find_element(By.XPATH,".//div[contains(@class,'eRduX')]").text
                except:
                    try:
                      timeoftrip=container[j].find_element(By.XPATH,".//span[contains(@class,'euPKI _R Me S4 H3')]").text
                      timeoftrip=timeoftrip.replace('Date of experience: ','')
                      try:
                        typeoftrip=container[j].find_element(By.XPATH,".//span[contains(@class,'eHSjO _R Me')]").text
                        typeoftrip=typeoftrip.replace('Trip type: ','')
                        time_and_typeoftrip=timeoftrip+" • "+typeoftrip
                      except:
                        time_and_typeoftrip=timeoftrip
                    except:
                      time_and_typeoftrip = 'None'
                print('scrape date')
                try:
                    dateWritten_div = container[j].find_element(By.XPATH,".//div[contains(@class,'fxays')]")
                    dateWritten=dateWritten_div.find_element(By.XPATH,".//div[contains(@class,'WlYyy diXIH cspKb bQCoY')]").text
                except:
                    try:
                        dateWritten = container[j].find_element(By.XPATH,".//div[contains(@class,'bcaHz')]").text
                        dateWritten=dateWritten.replace(profile_name,'')
                        dateWritten=dateWritten.replace(' wrote a review ','Written ')
                    except:    
                        dateWritten = 'None'
                attraction_review = {
                    'profilename': profile_name,
                    'date': dateWritten,
                    'rate': review_rate,
                    'title': title,
                    'review': review,
                    'time-typeoftrip': time_and_typeoftrip
                    }
                attraction_reviews.append(attraction_review)
                
                
            try:
                  driver.find_element(By.XPATH,'.//a[@class="dfuux u j z _F ddFHE bVTsJ emPJr"]').click()
            except:
                try:
                    print("CCCCCCCCCCCCCCCCCXXXXXXXXxxx")
                    driver.find_element(By.XPATH,'.//a[@class="ui_button nav next primary "]').click()
                    print("CCCCCCCCCCCCCCCCCXXXXXXXXxxx") 
                except: 
                    break
    except:
        attraction_reviews = 'None'
    print('creating object')
    attraction = {
        'city': city,
        'name': name,
        'address': address,
        'reviewnum': reviewnum,
        'workinghours':workinghours,
        'typeofattraction': typeofattraction,
        'about': about,
        'suggestedduration': suggestedduration,
        'rate': rate,
        'images': images,
        'attractionreview': attraction_reviews
        }

    attractiondata.append(attraction)
    print('saving: ', attraction['name'])
    k+=1


print('creating pd')
df = pd.DataFrame(attractiondata)
df.to_excel(f'{city} attractions.xlsx')
print(df)


    