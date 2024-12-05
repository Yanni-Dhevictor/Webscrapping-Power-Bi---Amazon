#Importando as bibliotecas e pacotes

from urllib.request import urlopen
import time
from bs4 import BeautifulSoup
import bs4
import requests
import pandas as pd
import numpy as np




# Function to extract Product Title
def get_title(soup):
    try:
        title = soup.find("span", attrs={"id":'productTitle'})
        title_value = title.text
        title_string = title_value.strip()
    except AttributeError:
        title_string = ""
    return title_string

# Function to extract Product Price
def get_price(soup):
    try:
        price = soup.find("span", attrs={'class':'a-price-whole'}).text.strip('.').replace(',', '')
        price_decimal = soup.find("span", attrs={'class':'a-price-fraction'}).text
        price = price + price_decimal
    except AttributeError:
        try:
            price = soup.find("span", attrs={'id':'priceblock_dealprice'}).text.strip().replace(',', '')
        except AttributeError:
            try:
                price = soup.find("span", attrs={'id':'priceblock_ourprice'}).text.strip().replace(',', '')
            except:
                price = ""
    return price

# Function to extract Product Rating
def get_rating(soup):
    try:
        rating = soup.find("i", attrs={'class':'a-icon a-icon-star a-star-4-5'}).string.strip()
    except AttributeError:
        try:
            rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
        except:
            rating = ""
    return rating

# Function to extract Number of User Reviews
def get_review_count(soup):
    try:
        review_count = soup.find("span", attrs={'id':'acrCustomerReviewText'}).string.strip()
    except AttributeError:
        review_count = ""
    return review_count

# Function to extract Availability Status
def get_availability(soup):
    try:
        available = soup.find("div", attrs={'id':'availability'})
        available = available.find("span").string.strip()
    except AttributeError:
        available = "Not Available"
    return available

# Função para verificar se há mais páginas
def has_next_page(soup):
    next_page = soup.find("li", attrs={'class': 'a-last'})
    if next_page and next_page.find("a"):
        return True
    return False




if __name__ == '__main__':
    # add your user agent 
    HEADERS = ({'User-Agent':'', 'Accept-Language': 'pt-BR, en;q=0.5'})
    
    for i in range(2,5):

        # The webpage URL
        URL = "https://www.amazon.com.br/s?k=CPUs&i=computers&rh=n%3A16364803011%2Cp_72%3A17833786011&page="+str(i)

        # HTTP Request
        webpage = requests.get(URL, headers=HEADERS)

        # Soup Object containing all data
        soup = BeautifulSoup(webpage.content, "html.parser")

        # Fetch links as List of Tag Objects
        links = soup.find_all("a", attrs={'class':'a-link-normal s-no-outline'})

        # Store the links
        links_list = []

        # Loop for extracting links from Tag Objects
        for link in links:
            links_list.append(link.get('href'))

        d = {"title":[], "price":[], "rating":[], "reviews":[],"availability":[]}

        # Loop for extracting product details from each link 
        for link in links_list:
            new_webpage = requests.get("https://www.amazon.com.br" + link, headers=HEADERS)
            new_soup = BeautifulSoup(new_webpage.content, "html.parser")

            # Function calls to display all necessary product information
            d['title'].append(get_title(new_soup))
            d['price'].append(get_price(new_soup))
            d['rating'].append(get_rating(new_soup))
            d['reviews'].append(get_review_count(new_soup))
            d['availability'].append(get_availability(new_soup))

            time.sleep(2)

    amazon_df_page2 = pd.DataFrame.from_dict(d)
    amazon_df_page2['title'].replace('', np.nan, inplace=True)
    amazon_df_page2 = amazon_df_page2.dropna(subset=['title'])
    amazon_df_page2.to_csv("amazon_data.csv", header=True, index=False)
