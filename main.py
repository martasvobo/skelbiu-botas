import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import os

# MODIFY    url with ad filters
url = "https://www.skelbiu.lt/skelbimai/?autocompleted=1&keywords=&cost_min=299&cost_max=801&type=1&condition=&cities=0&distance=0&mainCity=0&search=1&category_id=82&user_type=1&ad_since_min=0&ad_since_max=0&visited_page=1&orderBy=-1&detailsSearch=0"

# MODIFY    bot token
token = "5612856470:AAFXMf_FVDuhSthox08TSKQq5W2-Q7tH3ZU"
bot_url = f"https://api.telegram.org/bot{token}"

# MODIFY    your chat id
chat_id = "69420"

# MODIFY    keywords to avoid
keywords = ["macbook", "gtx", "rtx", "rx", "gaming", "zaidimu", "nvidia"]

user_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36"

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_argument(f"user-agent={user_agent}")

driver = webdriver.Chrome(
    executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options
)

driver.get(url)

# set which stores ad ids to prevent duplicates
seen = set()

while True:

    # scraps new ad information from page html
    soup = BeautifulSoup(driver.page_source, features="html5lib")
    ads = soup.findAll("li", {"class": "simpleAds"})
    ads = filter(lambda ad: ad["id"] not in seen, ads)

    # gets the link, title and price of every ad
    message = ""
    for ad in ads:
        seen.add(ad["id"])
        # filters out macbooks
        if not any(keyword in ad.a["href"].lower() for keyword in keywords):
            item_review = ad.find("div", {"class": "itemReview"})
            item_price = item_review.find("div", {"class": "adsPrice"}).span.text
            item_link = "https://www.skelbiu.lt" + ad.a["href"]
            item_title = item_review.h3.a.text.strip()
            message += f"{item_title}\nPrice: {item_price}\n{item_link}\n\n"

    # checks whether new ads are present and sends them through telegram
    if message:
        # send notification
        params = {"chat_id": chat_id, "text": message[:4095]}
        requests.get(bot_url + "/sendMessage", params=params)

    # delay after page refresh
    time.sleep(30)
    driver.refresh()
