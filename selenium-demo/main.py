from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import csv

# Set up Chrome options for headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run in headless mode, no browser will popup!

# Initialize the Chrome driver
driver = webdriver.Chrome(options=chrome_options)

output_csv = "output.csv"
if os.path.exists(output_csv):
    os.remove(output_csv)  # Remove the file if it exists

try:
    # Navigate to the quotes website
    driver.get("http://quotes.toscrape.com")

    # Scrape all quotes on the n page
    n = 3
    for page in range(1, n + 1):

        print(f">> scraping page {page}...")
        quotes = driver.find_elements(By.CLASS_NAME, "quote")
        for i, quote in enumerate(quotes, 1):
            text = quote.find_element(By.CLASS_NAME, "text").text
            author = quote.find_element(By.CLASS_NAME, "author").text
            
            with open(output_csv, 'a', encoding='utf-8', newline='') as f:
                csv_writer = csv.writer(f)
                csv_writer.writerow([author, text])
            # Wait for the "Next" button to be clickable and click it
        driver.find_element(By.CLASS_NAME, "pager")\
            .find_element(By.CLASS_NAME, "next")\
                .find_element(By.TAG_NAME, "a")\
                    .click()
        print(">> Navigating to the next page...")
        
        if page >= n:
            print(">> Reached the last page.")
            break

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    print(">> Scraping completed.")
    # Close the browser
    driver.quit()