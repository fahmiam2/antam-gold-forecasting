from pathlib import Path
import sys

# Get the root directory (two levels up from the src directory)
root_directory = Path(__file__).resolve().parents[1]
sys.path.append(str(root_directory))

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time

def _open_in_new_tab(driver, url):
    # Open a new tab
    driver.execute_script("window.open();")

    # Switch to the new tab
    driver.switch_to.window(driver.window_handles[-1])

    # Navigate to the URL in the new tab
    driver.get(url)

def _parse_token(driver, page_source):
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find the meta tag with name="_token"
    tag_meta = soup.find('meta', {'name': '_token'})

    # Extract the value of the content attribute
    token_value = tag_meta['content']

    return token_value
    

def _parse_raw_data(driver, token: str):
    # Construct the URL with the token
    url = f"https://www.logammulia.com/data-base-price/gold/sell?_token={token}"

    # Open the URL in a new tab
    _open_in_new_tab(driver, url)

    # Wait for the page to load
    time.sleep(3)

    # Get the page source
    page_source = driver.page_source

    # Process the raw data as needed
    soup = BeautifulSoup(page_source, 'html.parser')

    # Pilih elemen body dan ambil teks di dalamnya
    body_content = soup.body.get_text()

    # Proses data yang diambil
    data = eval(body_content)

    return data

def get_raw_data(url: str) -> pd.DataFrame:
    service = Service(executable_path=r"C:\Users\Fahmi Maulana\Documents\chromedriver-win64\chromedriver-win64\chromedriver.exe")
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)

    time.sleep(5)

    # get token value
    token_value = _parse_token(driver=driver, page_source=driver.page_source)

    # get raw data
    raw_data = _parse_raw_data(driver=driver, token=token_value)

    # convert into datafrae
    df = pd.DataFrame(raw_data, columns=['Timestamp', 'Gold Price'])

    # convert unix time to datetime format
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], unit="ms")
    df["Date"] = df["Timestamp"].dt.date
    return df[["Timestamp", "Date", "Gold Price"]]

df = get_raw_data("https://www.logammulia.com/id/harga-emas-hari-ini")
df.to_csv(str(root_directory) + "/data/harga-emas-antam.csv", index=False)

