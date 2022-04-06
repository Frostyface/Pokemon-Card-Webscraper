#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import json
import time
import random
import smtplib, ssl
from selenium.webdriver.chrome.options import Options


# In[2]:


#Declare necessary variables ---------------------

boxes = ['Shining fates','champions path', 'vivid voltage']
stores = ['GameStop', 'BestBuy','Walmart']
GSSfAvail,GSCpAvail,GSVvAvail,BBAvail,WAvail = False,False,False,False,False
GSRaw,BBRaw,WRaw = ['Not Available','Not Available','Not Available'],['Sold Out'],['Out of Stock']
gamestopSFURL = "https://www.gamestop.com/toys-collectibles/games-puzzles/trading-card-games/products/pokemon-trading-card-game-shining-fates-elite-trainer-box/11112932.html"
gamestopCPURL = "https://www.gamestop.com/toys-collectibles/games-puzzles/trading-card-games/products/pokemon-trading-card-game-champions-path-elite-trainer-box/11104961.html"
gamestopVVURL = "https://www.gamestop.com/toys-collectibles/games-puzzles/trading-card-games/products/pokemon-trading-card-game-sword-and-shield-vivid-voltage-elite-trainer-box/11107433.html"
bestbuySFURL = "https://www.bestbuy.com/site/pokemon-pokemon-tcg-shining-fates-elite-trainer-box-/6445827.p?skuId=6445827"
walmartCPURL = "https://www.walmart.com/grocery/ip/Pokemon-TCG-Sword-Shield-3-5-Champions-Path-Elite-Trainer-Box/463291638"
killFlag = False

#setup email--------------------------

port = 465
password = input("Password: ")

context = ssl.create_default_context()

#Setup browser arguments
    
option = webdriver.ChromeOptions()
option.add_argument('--ignore-certificate-errors')
option.add_argument("--test-type")
option.add_argument("--headless")
option.add_argument("--disable-gpu")
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'    
option.add_argument('user-agent={0}'.format(user_agent))
option.binary_location = "/Users/tinov/AppData/Local/Chromium/Application/chrome.exe"
    
#Initiate Chrome Drivers with Selenium
    
driver1 = webdriver.Chrome("/Users/tinov/Desktop/Python Stuff/Pokemon Card scanner/ChromeDriver/chromedriver",options=option)
driver1.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
#Begin Loop --------------------------------------

while(killFlag==False):
    
    #Grab SF data from GameStop
    
    try:
        driver1.get(gamestopSFURL)
        content1 = driver1.page_source
        soup1 = BeautifulSoup(content1)
        time.sleep(random.uniform(1,3))
        GSdata = soup1.find('button', attrs={'class':'add-to-cart btn btn-primary'})
        GSRaw[0]=GSdata.text
    except AttributeError as ae_error:
        print(ae_error)
        print("Unable to find GS SF data")
        
    #Check if found
    
    if(GSRaw[0]!='Not Available'):
        killFlag = True
        GSSfAvail = True
        availURL = gamestopSFURL
    
    #Grab CP data from GameStop
    
    try:
        driver1.get(gamestopCPURL)
        content1 = driver1.page_source
        soup1 = BeautifulSoup(content1)
        time.sleep(random.uniform(1,3))
        GSdata = soup1.find('button', attrs={'class':'add-to-cart btn btn-primary'})
        GSRaw[1]=GSdata.text
    except AttributeError as ae_error:
        print(ae_error)
        print("Unable to find GS CP data")
    
    #Check if found
    
    if(GSRaw[1]!='Not Available'):
        killFlag = True
        GSCpAvail = True
        availURL = gamestopCPURL
    
    #Grab VV data from GameStop
    
    try:
        driver1.get(gamestopVVURL)
        content1 = driver1.page_source
        soup1 = BeautifulSoup(content1)
        time.sleep(random.uniform(1,3))
        GSdata = soup1.find('div', attrs={'class':'store-inventory-unavailable'})
        GSRaw[2]=GSdata.text  
    except AttributeError as ae_error:
        print(ae_error)
        print("Unable to find GS VV data")
        
    #Check if found
    
    if(GSRaw[2]!='Item out of stock in your store'):
        killFlag = True
        GSVv = True
        availURL = gamestopVVURL
    
    #Grab data from BestBuy
    
    try:
        driver1.get(bestbuySFURL)
        content1 = driver1.page_source
        soup1 = BeautifulSoup(content1)
        time.sleep(random.uniform(1,3))
        BBdata = soup1.find('button', attrs={'class':'btn btn-disabled btn-lg btn-block add-to-cart-button'})
        BBRaw[0]=BBdata.text
    except AttributeError as ae_error:
        print(ae_error)
        print("Unable to find BB SF data")
        
    #Check if found
    
    if (BBRaw[0]!='Sold Out'):
        killFlag = True
        BBAvail = True
        availURL = bestbuySFURL
    
    #Grab data from Walmart
    
    try:
        driver1.get(walmartCPURL)
        time.sleep(5)
        content1 = driver1.page_source
        soup1 = BeautifulSoup(content1)
        Wdata = soup1.find('div', attrs={'class':'ProductPage__outOfStock___12yxb'})
        WRaw[0]=Wdata.text
        walmartContent = content1
    except AttributeError as ae_error:
        print(ae_error)
        print("Unable to find Wal CP data")
        
    #Check if found
    
    if (WRaw[0]!='Out of stock'):
        killFlag = True
        WAvail = True
        availURL = walmartCPURL
    
    #Refresh browser and loop
    
    driver1.refresh()
    
    #Ask to exit loop *FOR DEBUGGING COMMENT OUT CODE FOR USE*
    
    #cont = input("Would you like to continue?(1=yes,0=no):")
    
    #if(cont == "0"):
        #killFlag = True
        

#EXITED LOOP

#determine which site has availability

availURL = ""

if(GSSfAvail):
    availURL = gamestopSFURL
elif(GSCpAvail):
    availURL = gamestopCPURL
elif(GSVvAvail):
    availURL = gamestopVVURL
elif(BBAvail):
    availURL = bestbuySFURL
elif(WAvail):
    availURL = walmartCPURL

#email contents

sender_email = "pokemonavailability@gmail.com"
receiver_email = "tinovelez98@gmail.com"
message = """Subject: Pokemon Available

Pokemon available at: """ + availURL

#send email

with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
    server.login("pokemonavailability@gmail.com", password)
    server.sendmail(sender_email, receiver_email, message)


# In[ ]:





# In[ ]:




