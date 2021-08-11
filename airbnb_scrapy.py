import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as pd

# This is the path where I stored my chromedriver
PATH = "/Users/juanpih19/Desktop/Programs/chromedriver"

class AirbnbBot:

    # Class constructor that takes location, stay (Month, Week, Weekend)
    # Number of guests and type of guests (Adults, Children, Infants)
    def __init__(self, location, stay, number_guests, type_guests):
        self.location = location
        self.stay = stay
        self.number_guests = number_guests
        self.type_guests = type_guests
        self.driver = webdriver.Chrome(PATH)

    # The 'search()' function will do the searching based on user input
    def search(self):

        # The driver will take us to the Airbnb website
        self.driver.get('https://www.airbnb.com')
        time.sleep(1)

        # This will find the location's tab xpath, type the desired location
        # and hit enter so we move the driver to the next tab (check in)
        location = self.driver.find_element_by_xpath('//*[@id="bigsearch-query-detached-query-input"]')
        location.send_keys(Keys.RETURN)
        location.send_keys(self.location)
        location.send_keys(Keys.RETURN)

        # It was difficult to scrape every number on the calendar
        # so both the check in and check out dates are flexible.
        flexible = location.find_element_by_xpath('//*[@id="tab--tabs--1"]')
        flexible.click()

        # Even though we have flexible dates, we can choose if
        # the stay is for the weekend or for a week or month

        # if stay is for a weekend we find the xpath, click it and hit enter
        if self.stay in ['Weekend', 'weekend']:
            weekend = self.driver.find_element_by_xpath('//*[@id="flexible_trip_lengths-weekend_trip"]/button')
            weekend.click()
            weekend.send_keys(Keys.RETURN)

        # if stay is for a  week we find the xpath, click it and hit enter
        elif self.stay in ['Week', 'week']:
            week = self.driver.find_element_by_xpath('//*[@id="flexible_trip_lengths-one_week"]/button')
            week.click()
            week.send_keys(Keys.RETURN)

        # if stay is for a month we find the xpath, click it and hit enter
        elif self.stay in ['Month', 'month']:
            month = self.driver.find_element_by_xpath('//*[@id="flexible_trip_lengths-one_month"]/button')
            month.click()
            month.send_keys(Keys.RETURN)

        else:
            pass

        # Finds the guests xpath and clicks it
        guest_button = self.driver.find_element_by_xpath('/html/body/div[5]/div/div/div[1]/div/div/div[1]/div[1]/div/header/div/div[2]/div[2]/div/div/div/form/div[2]/div/div[5]/div[1]')
        guest_button.click()

        # Based on user input self.type_guests and self.number_guests

        # if type_guests are adults
        # it will add as many adults as assigned  on self.number_guests
        if self.type_guests in ['Adults', 'adults']:
            adults = self.driver.find_element_by_xpath('//*[@id="stepper-adults"]/button[2]')
            for num in range(int(self.number_guests)):
                adults.click()

        # if type_guests are children
        # it will add as many children as assigned  on self.number_guests
        elif self.type_guests in ['Children', 'children']:
            children = self.driver.find_element_by_xpath('//*[@id="stepper-children"]/button[2]')
            for num in range(int(self.number_guests)):
                children.click()

        # if type_guests are infants
        # it will add as many infants as assigned  on self.number_guests
        elif self.type_guests in ['Infants', 'infants']:
            infants = self.driver.find_element_by_xpath('//*[@id="stepper-infants"]/button[2]')
            for num in range(int(self.number_guests)):
                infants.click()

        else:
            pass


        # Guests tab is the last tab that we need to fill before searching
        # If I hit enter the driver would not search
        # I decided to click on a random place so I could find the search's button xpath
        x = self.driver.find_element_by_xpath('//*[@id="field-guide-toggle"]')
        x.click()
        x.send_keys(Keys.RETURN)


        # I find the search button snd click in it to search for all options
        search = self.driver.find_element_by_css_selector('button._sxfp92z')
        search.click()


    # This function will scrape all the information about every option
    # on the first page
    def scraping_aribnb(self):

        # Maximize the window
        self.driver.maximize_window()

        # Gets the current page sourse
        src = self.driver.page_source

        # We create a BeautifulSoup object and feed it the current page source
        soup = BeautifulSoup(src, features='lxml')

        # Find the class that contains all the options and store it
        # on list_of_houses variable
        list_of_houses = soup.find('div', class_ = "_fhph4u")

        # Type of properties list - using find_all function
        # found the class that contains all the types of properties
        # Used a list comp to append them to list_type_property
        type_of_property = list_of_houses.find_all('div', class_="_1tanv1h")
        list_type_property = [ i.text for i in type_of_property]

        # Host description list - using find_all function
        # found the class that contains all the host descriptions
        # Used a list comp to append them to list_host_description
        host_description = list_of_houses.find_all('div', class_='_5kaapu')
        list_host_description = [ i.text for i in host_description]

        # Number of bedrooms and bathrooms - using find_all function
        # bedrooms_bathrooms and other_amenities used the same class
        # Did some slicing so I could append each item to the right list
        number_of_bedrooms_bathrooms = list_of_houses.find_all('div', class_="_3c0zz1")
        list_bedrooms_bathrooms = [ i.text for i in number_of_bedrooms_bathrooms]
        bedrooms_bathrooms = []
        other_amenities = []

        bedrooms_bathrooms = list_bedrooms_bathrooms[::2]
        other_amenities = list_bedrooms_bathrooms[1::2]

        # Date - using find_all function
        # found the class that contains all the dates
        # Used a list comp to append them to list_date
        dates = list_of_houses.find_all('div', class_="_1v92qf0")
        list_dates = [date.text for date in dates]

        # Stars - using find_all function
        # found the class that contains all the stars
        # Used a list comp to append them to list_stars
        stars = list_of_houses.find_all('div', class_ = "_1hxyyw3")
        list_stars = [star.text[:3] for star in stars]

        # Price - using find_all function
        # found the class that contains all the prices
        # Used a list comp to append them to list_prices
        prices = list_of_houses.find_all('div', class_ = "_1gi6jw3f" )
        list_prices = [price.text for price in prices ]


        # putting the lists with data into a Pandas data frame
        airbnb_data = pd.DataFrame({'Type' : list_type_property, 'Host description': list_host_description, 'Bedrooms & bathrooms': bedrooms_bathrooms, 'Other amenities': other_amenities,
                'Date': list_dates,  'Price': list_prices})

        # Saving the DataFrame to a csv file
        airbnb_data.to_csv('Airbnb_data.csv', index=False)


if __name__ == '__main__':
    vacation = AirbnbBot('New York', 'week', '2', 'adults')
    vacation.search()
    time.sleep(2)
    vacation.scraping_aribnb()
