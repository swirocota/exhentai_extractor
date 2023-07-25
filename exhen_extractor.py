import re                       #module for regex
import json                     #
from time import time, sleep    #
from requests import Session    #
from bs4 import BeautifulSoup   #module for HTML parsing
import os                       #file and directory

#cookie for login exhentai
#insert cookie informations you have
igneous = "your_igneous"
ipb_member_id = "your_ipb_member_id"
ipb_pass_hash = "your_ipb_pass_hash"
ipb_exhentai_id = "your_ipb_exhentai_id"

#make exhentai for login exhentai
exhentai = Session()
exhentai.headers['User-Agent'] = 'Mozilla/5.0 (compatible; exhentai-extractor;)'
exhentai.cookies.update(
    {
        'igneous': igneous,
        'ipb_exhentai_id': ipb_exhentai_id,
        'ipb_member_id': ipb_member_id,
        'ipb_pass_hash': ipb_pass_hash
    }
)



for ind in range(0,11):                                                                     #Categoty 0 ~ 9, 10 is for all
    
    category = exhentai.get('https://exhentai.org/favorites.php')                           #all favorites
    if ind != 10 :
        category = exhentai.get('https://exhentai.org/favorites.php?favcat=' + str(ind))    #favorite category 

    if category.ok:
        categoryHTML = category.text
    else:
        print("Something Wrong with access with categoty " + str(ind))
        continue                                                           
    page = BeautifulSoup(categoryHTML, "html.parser")                                       #for parse HTML
    galleryList =[]                                                                         #favorites List

    while True:
        for link in page.find_all('a'):                                                     #find all a tag
            glink = str(link.get('href'))                                                   #save href value in a
            pattern = re.compile("https://exhentai.org/g/")                                 #compile regex
            flag = pattern.search(glink)                                                    #check if glink satisfied regex
            if not flag: continue                                                           #skip if not
            if galleryList.count(glink) == 1: continue                                      #also skip if already added
            galleryList.append(glink)                                                       #apped to list
        nextPage = page.find("a", {"id": "unext"})                                          #find next page link  
        if str(nextPage) == 'None' : break                                                  #break when there is no link 
        category = exhentai.get(str(nextPage.get('href')))                                  #get session of next page
        page = BeautifulSoup(category.text, "html.parser")                                  #make BeautifulSoup again
    
    print("Category " + str(ind) +":" + str(len(galleryList)))                              #show count of favorites                              
    if len(galleryList) == 0: galleryList.append("There is no gallery")                     #for file Write when there are no links in category
    
    textFile = None                                                                         #variable declaration
    if ind == 10: textFile = open("./all favorites.txt", 'w')                               #write to all favorites.txt
    else: textFile = open("./favorite Category " + str(ind) + ".txt", 'w')                  #or category txt
    for i in range(len(galleryList)):
        textFile.write(str(galleryList[i]) + "\n")                                          #write gallery links
    textFile.close()                                                                        #close the file

print("writed to path: " + os.getcwd())
