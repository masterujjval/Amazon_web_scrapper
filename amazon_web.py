import requests
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np
import warnings
import pandas as pd

# Suppress FutureWarning messages
warnings.simplefilter(action='ignore', category=FutureWarning)

d = {"title":[], "price":[], "rating":[], "reviews":[]}

# GET titles
def get_title(soup):

    try:
        # Outer Tag Object
        title = soup.find("span", attrs={"id":'productTitle'})
        
        # Inner NavigatableString Object
        title_value = title.text

        # Title as a string value
        title_string = title_value.strip()
        
        print(f"Product-> {title_string}")

    except AttributeError:
        title_string = ""

    return title_string

# GET product price
def get_price(soup):

    try:
        price = soup.find("span",attrs={"class":"a-price-whole"}).text.strip()
        print(f"Price-> {price}")

    except AttributeError:

        try:
            # If there is some deal price
            price = soup.find("span",attrs={"class":"a-price-whole"}).text.strip()
            print(f"Price-> {price}")

        except:
            price = ""
    
    return price

# Get Product Rating
def get_rating(soup):

    try:
        rating = soup.find("i", attrs={'class':'a-icon-alt'}).text.strip()
        print(f"Ratings-> {rating}")
    except AttributeError:
        try:
            rating = soup.find("span", attrs={'class':'a-icon-alt'}).text.strip()
            print(f"Ratings-> {rating}")
        except:
            rating = ""	
    
    return rating

# GET reviews count
def get_review_count(soup):
    try:
        review_count = soup.find("span", attrs={'id':'acrCustomerReviewText'}).text.strip()
        print(f"Reviews-> {review_count}")
    except AttributeError:
        review_count = ""	
    
    return review_count

# driver or heres the main code

try:

    # IMPORTANT to add user, as for not letting this ip mark as bot
    HEADERS = ({'User-Agent':'', 'Accept-Language': 'en-US, en;q=0.5'})

    # Requesting and getting webpage
    user=input("Enter product name: ")
    URL = "https://www.amazon.in/s?k="+user

    # HTTP Request
    webpage = requests.get(URL, headers=HEADERS)

    # after getting webpage we will change its content to html so that we can use the information for finding particular stuff
    soup = BeautifulSoup(webpage.content, "html.parser")

    # to get all the products 
    links = soup.find_all("a", attrs={'class':'a-link-normal s-no-outline'})

    # Store the links
    links_list = []

    # so that we dont have to run the loop it will run till the number os products available
    for link in links:
            links_list.append(link.get('href'))

    
    
    # getting each prodcut details
    for link in links_list:
        new_webpage = requests.get("https://www.amazon.in" + link, headers=HEADERS)

        new_soup = BeautifulSoup(new_webpage.content, "html.parser")

        # Function calls to display all necessary product information
        d['title'].append(get_title(new_soup))
        d['price'].append(get_price(new_soup))
        d['rating'].append(get_rating(new_soup))
        d['reviews'].append(get_review_count(new_soup))
        print("\n")
       
   
    
except KeyboardInterrupt:
    print("File saved in the Home folder")
    
amazon_df = pd.DataFrame.from_dict(d)
amazon_df['title'].replace('', np.nan, inplace=True)
amazon_df = amazon_df.dropna(subset=['title'])
amazon_df.to_csv("amazon_data.csv", header=True, index=False)
    
    
