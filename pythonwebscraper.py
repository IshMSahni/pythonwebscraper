from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import requests
import os

def searchable():
    print("Hello, This is a simple bing web scraper.\nThis will scrape bing data for your desired search information.\nThere is a choice between two different types of data that can be scraped. Which one would you like to scrape. \n1. Links \n2. Images\n" )
    x = True;
    while x == True:
        options = int(input("Please enter the corresponding number to the type of data that you would like to scrape:"))
        if options in [1, 2]:
            break
        else:
            print("Please enter a valid input")
    search = input("What are you searching for?")
    if options == 1: #scrapes for links
        query = {"q": search}
        r = requests.get("https://www.bing.com/search", params=query)
        soup = BeautifulSoup(r.text, 'lxml')
        
        #looks for the search engine results thats appear in the form of an ordered list
        allresults = soup.find("ol", {"id": "b_results"})  # find ol(orderedlist) with id b_results 
        
        #looks through the results ol list and finds all the different results
        seperatelinks = allresults.findAllNext("li", {"class": "b_algo"}) 
        
        #sorting and printing method
        for item in seperatelinks:
            item_text = item.find("a").text
            item_href = item.find("a").attrs["href"]

            if item_text and item_href:
                print(item_text)
                print(item_href)
                print("Summary:", item.find("a").parent.parent.find("p").text)
                print("\n")

    if options == 2: #scrapes for images
        query = {"q": search}
        dir_name = search.replace(" ", "_").lower() #remove spaces for downloading purposes of a folder with the name of your search

        if not os.path.isdir(dir_name):
            os.mkdir(dir_name)
            
        r = requests.get("http://www.bing.com/images/search", params=query)
        
        soup = BeautifulSoup(r.text, "lxml")
        links = soup.findAll("a", {"class": "thumb"})#looks for all thumbnails in image search
        for item in links:
            try:
                img_obj = requests.get(item.attrs["href"])
                print("Getting ", item.attrs["href"])
                title = item.attrs["href"].split("/")[-1]
            except:
                print("Something is wrong with the image")
            try:
                img = Image.open(BytesIO(img_obj.content))
            except IOError:
                print("Image cannot be downloaded")
                continue

            print("Image Name: " + title)
            print("Format: " + img.format + "\n")

            if (title.endswith(("jpg", "png", "gif"))):
                img.save("./" + dir_name + "/" + title, img.format)
            else:
                print("Aw, poop the image file corrupted, could not download :(")
    searchable()
    
    
searchable()