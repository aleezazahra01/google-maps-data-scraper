from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import pandas as pd
from dataclasses import dataclass, asdict, field
import time

# user config
#customize this if needed

search_config = {
    "keyword": "karachi hotels",
    "listings_to_scrape": 20  # change this number as needed
}

@dataclass
class Business:
    name: str = None
    reviews: str = None
    address: str = None
    website: str = None
    phone: str = None

@dataclass
class Businesslist:
    business_list: list[Business] = field(default_factory=list)
    
    def dataframe(self):
        return pd.json_normalize([asdict(business) for business in self.business_list])
    
    def save_to_excel(self, filename):
        self.dataframe().to_excel(f'{filename}.xlsx', index=False)
    
    def save_to_csv(self, filename):
        self.dataframe().to_csv(f'{filename}.csv', index=False)

def main():
    options = Options()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 30)

    driver.get("https://www.google.com/maps")

    # search keyword
    search_box = wait.until(EC.presence_of_element_located((By.ID, "searchboxinput")))
    search_box.send_keys(search_config["keyword"])
    search_box.send_keys(Keys.ENTER)
    time.sleep(10)  # wait for results to load

    # get listings
    listings = driver.find_elements(By.XPATH, '//div[@role="article"]')
    print(f"Found {len(listings)} listings")

    business_list = Businesslist()

    for listing in listings[:search_config["listings_to_scrape"]]:
        try:
            listing.click()
            time.sleep(5)

            title_path = '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div[1]/h1'
            reviews_path = '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[2]/div/div[1]/div[2]/div/div/div[2]/span[1]/span[1]'
            address_path = '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[11]/div[3]/button/div/div[2]/div[1]'
            website_path = '//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[11]/div[4]/a/div/div[2]/div[1]'

            business = Business()

            try:
                business.name = wait.until(EC.presence_of_element_located((By.XPATH, title_path))).text
            except:
                business.name = None

            try:
                business.reviews = driver.find_element(By.XPATH, reviews_path).text
            except:
                business.reviews = None

            try:
                business.address = driver.find_element(By.XPATH, address_path).text
            except:
                business.address = None

            try:
                business.website = driver.find_element(By.XPATH, website_path).text
            except:
                business.website = None

            business_list.business_list.append(business)

        except Exception as e:
            print(f"Error while scraping listing: {e}")
            continue

    business_list.save_to_excel("business_data")
    business_list.save_to_csv("business_data")

    driver.quit()

if __name__ == "__main__":
    main()
