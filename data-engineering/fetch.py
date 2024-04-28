from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pandas as pd
import time

def open_in_new_tab(driver, url):
    # Open a new tab
    driver.execute_script("window.open();")

    # Switch to the new tab
    driver.switch_to.window(driver.window_handles[-1])

    # Navigate to the URL in the new tab
    driver.get(url)

def get_token(url: str) -> str:
    service = Service(executable_path=r"C:\Users\Fahmi Maulana\Documents\chromedriver-win64\chromedriver-win64\chromedriver.exe")
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)

    # Wait for the page to load
    time.sleep(5)  # Adjust the waiting time as needed

    # Get the page source
    page_source = driver.page_source

    # Close the webdriver
    # driver.quit()

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')

    # Find the meta tag with name="_token"
    tag_meta = soup.find('meta', {'name': '_token'})

    # Extract the value of the content attribute
    token_value = tag_meta['content']

    # Use the token to fetch raw data
    get_raw_data(driver, token_value)

    return token_value

def get_raw_data(driver, token: str):
    # Construct the URL with the token
    url = f"https://www.logammulia.com/data-base-price/gold/sell?_token={token}"

    # Open the URL in a new tab
    open_in_new_tab(driver, url)

    # Wait for the page to load
    time.sleep(5)  # Adjust the waiting time as needed

    # Get the page source
    page_source = driver.page_source

    # Process the raw data as needed
    soup = BeautifulSoup(page_source, 'html.parser')
    # Pilih elemen body dan ambil teks di dalamnya
    body_content = soup.body.get_text()

    # Proses data yang diambil
    data = eval(body_content)

    print(data)

    # Convert the data to a DataFrame
    df = pd.DataFrame(data, columns=['Timestamp', 'Value'])

    df["Timestamp"] = pd.to_datetime(df["Timestamp"], unit="ms")

    print(df)

# Get the token
token = get_token("https://www.logammulia.com/id/harga-emas-hari-ini")
print("Token:", token)
