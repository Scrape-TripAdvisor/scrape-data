
import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time 
from selenium.webdriver.common.by import By

s = Service('D:\\chromedriver.exe')
driver = webdriver.Chrome(service=s)

print('start scrapping')
baseurl = 'https://www.tripadvisor.com'
print('init baseurl')
url = 'https://www.tripadvisor.com/Hotels-g668835-Mansoura_Ad_Daqahliyah_Governorate-Hotels.html'
city = "Mansoura"
print('init header')
headeers = {'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36'}
print('init reaponse')
response = requests.get(url,headers=headeers)
print('init soap')
soup = BeautifulSoup(response.content, 'html.parser')
hotellinks = []
print('find all a')
hotellist = soup.find_all('a', {'class': 'property_title'})
for item in hotellist:
    print('finding url')
    hotellinks.append(baseurl + item['href'])
print(len(hotellinks))


hoteldata = []
languagespoken = []
k = 1

for link in hotellinks:

    print('visiting the url',k)
    print(link)
    r = requests.get(link, headers=headeers)
    soup = BeautifulSoup(r.content, 'html.parser')
    # scrape name
    print('name value')
    try:
        name = soup.find('h1', {'class': 'fkWsC b d Pn'}).text.strip()
    except:
        name = 'None'
    # scrape review
    print('review value')
    try:
        reviewsnum = soup.find('span',{'class':'HFUqL'}).text.strip()
    except:
        reviewsnum = 'None'
    # scrape address
    print('address value')
    try:
        address = soup.find('span',{'class':'ceIOZ yYjkv'}).text.strip()
    except:
        top = soup.find('span',{'class':'ui_icon map-pin-fill cRwAM S4 H3'})
        down = top.find_next('span')
        address = down.find('span').text.strip()
    # scrape Number of Rooms
    print('no of rooms value')
    noofrooms = 'None'
    try:
        about = soup.find('div', {'class': 'dKfjB','data-section-signature':'about'})
        capacity = about.find_all('div',{'class':'eMwuk Ci b'})
        for item in capacity:
                if(item.text == 'NUMBER OF ROOMS'):
                    noofrooms = item.find_next('div',{'class':'cJdpk Ci'}).text
        print(noofrooms)
    except:
        noofrooms = 'None'

    x = 0
    propertylist = []
    roomfeatures = []
    roomtypes = []
    hotelimg = []
    styles = []
    hotelreview = []
    
    # scrape price
    print('price value')
    try:
        print('finding parent class')
        priceinit = soup.find('div',{'class':'premium_offers_area offers'})
        if priceinit == None:
            print('parent class does not exist')
            price = 'None'
            print('price is None')
        else:
            print('parent class exist')
            print('first case: price inside div')
            finddiv = priceinit.find('div',{'class':'dowyF _S Z offer cpacJ bookableOffer'})
            if finddiv != None:
                print('first case exist')
                price = finddiv['data-pernight']
                print('price from first case is ',price)
            else:
                print('first case does not exist')
                print('second case: price inside a')
                finda = priceinit.find('a',{'class':'bookableOffer'})
                if finda != None:
                    print('second case exist')
                    price = finda['data-pernight']
                    print('price from second case is ',price)
                else:
                    price = 'N'
                    print('second case does not exist')
                    print('third case: price inside a inside div')
                    find_all_div = priceinit.find_all('div')
                    for item in find_all_div:
                        print('looping on divs')
                        find_a_inside_div = item.find(class_= 'dowyF _S Z offer cpacJ bookableOffer')
                        if find_a_inside_div != None:
                            print('third case exist')
                            price = find_a_inside_div['data-pernight']
                            print('price from second case is ',price)         
    except:
        print('try case failed')
        price = 1022
        print('price from except ',price)
        
    # scrape rating  
    print('rating value')
    try:  
        rating = soup.find('span',{'class':'bvcwU P'}).text.strip()
    except:
        rating = 'None'
    # scrape state
    print('state value')
    try:
        state = soup.find('div',{'class':'cNJsa'}).text.strip()
    except:
        state = 'None'
    # scrape description
    print('description value')
    # duhwe _T bOlcm eKpTP Ci Mh ME dMbup // duhwe _T bOlcm bWqJN Ci dMbup \\ pIRBV _T
    driver.get(link)
    try:
        data = BeautifulSoup(driver.page_source,'lxml')
        description_div = data.find('div',{'class':'duhwe _T bOlcm bWqJN Ci dMbup'})
        if description_div != None:
            description = description_div.find('div',{'class','pIRBV _T'}).text.strip()
        else:
            description_div = data.find('div',{'class':'duhwe _T bOlcm eKpTP Ci Mh ME dMbup'})
            if description_div != None:
                description = description_div.find('div',{'class','pIRBV _T'}).text.strip()
            else:
                description = 'None'
        print(description)
    except:
        description = 'None'
        print('description None')
        
    #scrape amenities
    print('amenities value')
    propertyamenities = soup.find_all('div', {'class': 'ccdzg S5 b Pf ME'})
    for item in propertyamenities:
            if(item.text == 'Property amenities'):
                test = item.find_next('div',{'class':'exmBD K'})
                for amenity in test.find_all('div', {'class': 'bUmsU f ME H3 _c'}):
                    propertylist.append(amenity.text) 
            elif(item.text == 'Room features'):
                test = item.find_next('div',{'class':'exmBD K'})
                for amenity in test.find_all('div', {'class': 'bUmsU f ME H3 _c'}):
                    roomfeatures.append(amenity.text)
            
            elif (item.text=='Room types'):
                test = item.find_next('div',{'class':'exmBD K'})
                for amenity in test.find_all('div', {'class': 'bUmsU f ME H3 _c'}):
                    roomtypes.append(amenity.text)
    if (roomtypes == []):
        roomtypes='None' 
    if(roomfeatures == []):
        roomfeatures="None"
    if(propertylist == []):
        propertylist="None"


    # scrape hotel class
    print('hotel class')
    try:
        hotelclass = soup.find('svg',{'class':'TkRkB d H0'})
        starnum = hotelclass['aria-label']
        print(starnum)
    except:
        starnum = 'None'

    # scarpe hotel style
    print('hotel style value')
    try:
        upper = soup.find_all('div', {'class': 'ui_columns is-mobile'})
        data=upper[0]
        length=len(upper)
        if (length==2):
            data=upper[1]
        div = data.find('div', {'class': 'ui_column is-6'})
        hotelstyle = div.find_all('div', {'class': 'drcGn _R MC S4 _a H'})
        if ( starnum == 'None'):
            for each in hotelstyle:
                styles.append(each.text.strip())
        else:
            for each in hotelstyle[1:]:
                styles.append(each.text.strip())
            if (styles==[]):
                styles = 'None'
    except:
        styles = 'None'


    # scrape languages spoken
    print('language spoken value')
    try:
        languages = soup.find_all('div',{'class':'ssr-init-26f'})
        for lang in languages:
            target = lang.find('div',{'class':'drcGn _R MC S4 _a H'})
            if target !=None:
                child = lang.find('span',{'class':'gajVz _S'})
                if child != None:
                    Data = target.text.strip()
                    childdata = child.text.strip()
                    Data = Data.replace(childdata,"")
                else:
                    Data = target.text.strip()
        languagespoken = Data
    except:
        languagespoken = 'None'

    # scrape telephone
    print('telephone value')
    try:
        telephone = soup.find('span',{'class':'eeFQx ceIOZ yYjkv'}).text.strip()
    except:
        telephone = 'None'

    # scrape images
    print('image value')
    try:
        data = BeautifulSoup(driver.page_source,'lxml')
        for img in data.find_all('img',{'class':'bMGfJ _Q t _U s l bnegk'}):
            params = '?w=600&h=500&s=1'
            imgurl = img['src']
            res = imgurl[:imgurl.rfind('?')]
            src = res + params
            hotelimg.append(src)
            print('collecting image')
    except:
        hotelimg = 'None'

    
    # scrape reviews
    print('scrape reviews')
    try:
        pages_to_scrape = 3
        for i in range(0, pages_to_scrape):
            time.sleep(22)
            print('scrape page',i+1)
            driver.find_element(By.XPATH,".//div[contains(@class, 'duhwe _T bOlcm dMbup')]").click()
            container = driver.find_elements(By.XPATH,".//div[contains(@data-test-target, 'HR_CC_CARD')]")

            for j in range(len(container)):

                print('scrape rate')
                try:
                    rate = container[j].find_element(By.XPATH,".//span[contains(@class, 'ui_bubble_rating bubble_')]").get_attribute("class").split("_")[3]
                except:
                    rate = 'None'
                print('scrape title')
                try:
                    title = container[j].find_element(By.XPATH,".//div[contains(@data-test-target, 'review-title')]").text
                except:
                    title = 'None'
                print('scrape review')
                try:
                    review = container[j].find_element(By.XPATH,".//q[@class='XllAv H4 _a']").text.replace("\n", "  ")
                except:
                    review = 'None'
                print('scrape profile name')
                try:
                    profile_name = container[j].find_element(By.XPATH,".//a[contains(@class, 'ui_header_link bPvDb')]").text
                except:
                    profile_name = 'None'
                print('scrape dateofstay')
                try:
                    dateofstay = container[j].find_element(By.XPATH,".//span[contains(@class, 'euPKI _R Me S4 H3')]").text
                except:
                    dateofstay = 'None'
                print('scrape date')
                try:
                    date = container[j].find_element(By.XPATH,".//div[contains(@class, 'bcaHz')]//span").text
                    if(date == None):
                        date = 'None'
                    else:
                        date = date.replace(profile_name, '')
                except:
                    date = 'None'

                hotel_review = {
                    'profilename': profile_name,
                    'date': date,
                    'rate': rate,
                    'title': title,
                    'review': review,
                    'dateofsaty': dateofstay
                }
                hotelreview.append(hotel_review)
            try:
                driver.find_element(By.XPATH,'.//a[@class="ui_button nav next primary "]').click()
            except:
                break
    except:
        hotelreview = 'None'


    print(len(hotelreview))



    print('creating object')
    hotel = {
        'city': city,
        'name': name,
        'address': address,
        'reviewsnum': reviewsnum,
        'price': price,
        'Numofrooms': noofrooms,
        'description': description,
        'rating': rating,
        'state': state,
        'Propertyamenities': propertylist,
        'roomfeatures' : roomfeatures,
        'roomtypes': roomtypes,
        'starnum': starnum,
        'hotelstyle': styles,
        'languagespoken': languagespoken,
        'telephone': telephone,
        'images': hotelimg,
        'hotelreviews': hotelreview
    }

    hoteldata.append(hotel)
    print('saving: ', hotel['name'])
    k+=1


print('creating pd')
df = pd.DataFrame(hoteldata)
df.to_excel(f'{city}.xlsx')
print(df)
""" print(len(hotellinks))
print(*hotellinks, sep = "\n") """