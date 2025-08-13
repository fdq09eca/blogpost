from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import csv

# Set up Chrome options for headless mode
options = Options()
options.add_argument("--headless")  # Run in headless mode, no browser will popup!
options.add_argument("--disable-blink-features=AutomationControlled") # Many websites (especially social media like Bluesky, Twitter, etc.) check this property to detect bots or Selenium., By disabling that Blink feature, navigator.webdriver will not be set automatically, which makes automation less detectable.
options.add_argument("--window-size=1920,1080")

# Initialize the Chrome driver
driver = webdriver.Chrome(options=options)
output_csv = "bluesky_output.csv"

if os.path.exists(output_csv):
    os.remove(output_csv)  # Remove the file if it exists

try:
    # Go to Bluesky
    driver.get("https://bsky.app/")
    WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@data-testid='postText']")))

    # get all posts on the page
    posts = driver.find_elements(By.XPATH, "//div[@data-testid='postText']")

    print(f"Found {len(posts)} posts on the page.")

    for post in posts:
    # Post text
        text = post.text.strip()
        # Poster name is in the ancestor chain
        try:
            name_elem = post.find_element(By.XPATH, ".//ancestor::div[@data-testid='contentHider-post']/preceding::a[@aria-label='View profile'][1]")
            name = name_elem.text.strip()
        except:
            name = "Unknown"
        
        try:
            time_elem = post.find_element(
                By.XPATH,
                ".//ancestor::div[@data-testid='contentHider-post']/preceding::a[contains(@aria-label,' at ')]"
            )
            post_time = time_elem.get_attribute("aria-label")
        except:
            post_time = "Unknown"
            
        with open(output_csv, 'a', encoding='utf-8', newline='') as f:
           csv_writer = csv.writer(f)
           csv_writer.writerow([name, post_time, text])
        
        print(f"Poster: {name} | {post_time}\nPost: {text}\n-----")

finally:
    driver.quit()
