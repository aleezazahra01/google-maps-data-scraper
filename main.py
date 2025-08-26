from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.common.exceptions import TimeoutException 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import pandas as pd
from playwright.sync_api import sync_playwright
from dataclasses import dataclass,asdict,field
import argparse
import numpy as np
import playwright as pw

@dataclass #contains data of each business
#Provides more feature than a dictionary
class Business:
    name:str=None
    address:str=None
    website:str=None
    phone:str=None

@dataclass  #all instnance from prev class will be appende to this
class Businesslist:
    business_list:list[Business]=field(default_factory=list)

    def dataframe(self):
        #json_normalize is used when api returns data in a nested structure and this functuon flattens that data to make it eaiser to work with ,it is easier to loa and use in a database
        return pd.json_normalize([asdict(business)for business in self.business_list]),sep=""
    def save_to_excel(self,filename):
        self.dataframe().to_excel(f'{filename}.xlsx',index=False)
    def save_to_csv(self,filename):
        self.dataframe().to_csv(f'{filename}.csv',index=False)

def main():
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=False)
        page=browser.new_page()

        page.goto('https://www.google.com/maps',timeout=60000)
        page.wait_for_timeout(50000) #wait for five seconds 

        page.locator('input[@id="searchboxinput"]').fill(search_for)
        page.wait_for_timeout(3000)  #sleep for 3 seconds

        page.keyboard.press('Enter')
        page.wait_for_timeout(10000)  #wait for 10 seconds

        listings=page.locator('//div[@role="article"]').all()
        print(len(listings))





        browser.close()

if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument('-s','--search',type=str)
    parser.add_argument('-l','--location',type=str)
    args=parser.parse_args()

    if args.location and args.search:
        search_for=f'{args.search}--{args.location}'
    else:
        search_for='dentist new york'
'''Created the main functions only it doesnt work right now just some basic args and declarations '''
