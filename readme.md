# Introduction

Researchers frequently initiate their data collection by exploring online resources, seeking valuable information from websites. While some data providers offer convenient download options, others provide no such functionality, leaving researchers to rely on manual copying and pasting. This approach, though functional, is time-consuming, error-prone, and inefficient. Automating these repetitive tasks can significantly enhance productivity. This guide introduces web scraping using Python, focusing on three prominent libraries: `requests`, `BeautifulSoup`, and `Selenium`. Written for readers with minimal programming experience, this guide compares these tools and provides practical examples to facilitate effective web scraping. By the end, readers will be equipped to select the most suitable tool for their target website.

# Background

Websites are fundamentally structured in HTML, a standardized markup language that organizes content, such as `<h1>Hello World</h1>`. Accessing this HTML requires adherence to the HTTP protocol to request the file from a web server. This process involves resolving a URL to an IP address, sending a GET request, and receiving the HTML content in response. Modern web browsers handle these interactions seamlessly, enabling users to access content with a single click. Understanding this process is essential for effective web scraping.

# Overview of Web Scraping Libraries

This section introduces three Python libraries commonly used for web scraping: `requests`, `BeautifulSoup`, and `Selenium`. Each library offers distinct capabilities, and their applications are explored below, along with practical examples to illustrate their functionality.

## 1. The `requests` Library: Simplified HTTP Requests

The `requests` library is a lightweight and user-friendly tool designed for sending HTTP requests, such as GET requests, to retrieve raw HTML from a web server. It is ideal for beginners due to its simplicity and efficiency.

```python
import requests

url = "https://example.com"
response = requests.get(url)
print(response.text)  # Outputs the HTML content
```

This example demonstrates how `requests` fetches HTML with minimal code. However, it retrieves only raw HTML, requiring additional tools for parsing and extracting specific data.

## 2. `BeautifulSoup`: Parsing HTML Content

The `BeautifulSoup` library, from the `bs4` package, excels at parsing HTML and extracting specific elements. It is typically used in conjunction with `requests` to process the raw HTML into structured data, enabling users to locate elements by tags, classes, or text content.

### Example: Extracting Book Information from an Online Bookstore

Consider a scenario where the objective is to extract book information (title, price, rating, and availability) from an online bookstore, such as http://books.toscrape.com. Inspecting the website’s HTML reveals that book details are contained within `<article>` tags with the class `product_pod`. The following code demonstrates how to extract this information from the first page:

```python
import requests
from bs4 import BeautifulSoup

url = "http://books.toscrape.com"
response = requests.get(url)
response.encoding = 'utf-8'  # Ensure proper encoding
soup = BeautifulSoup(response.text, "html.parser")

books = soup.find_all("article", class_="product_pod")
for book in books:
    title = book.find("a", attrs={'title': True})['title']
    price = book.find("p", class_="price_color").text
    rating = book.find("p", class_="star-rating")["class"][1]
    print(title, price, rating)
```

To extend this to multiple pages, observe the URL pattern for pagination. For instance, the URLs for pages 1 and 2 are:

- http://books.toscrape.com/catalogue/category/books_1/page-1.html
- http://books.toscrape.com/catalogue/category/books_1/page-2.html

The pattern `page-{n}` allows iteration over multiple pages. The following code scrapes book information across 50 pages and saves it to a CSV file using Python’s `csv` library, which handles special characters and formatting automatically:

```python
import requests
import csv
from bs4 import BeautifulSoup

n_pages = 50
csv_file = "books.csv"

with open(csv_file, "w", newline='', encoding='utf-8') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(["Title", "Price", "Rating"])  # Write header

for n in range(1, n_pages + 1):
    url = f"http://books.toscrape.com/catalogue/category/books_1/page-{n}.html"
    response = requests.get(url)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, "html.parser")

    books = soup.find_all("article", class_="product_pod")
    for book in books:
        title = book.find("a", attrs={'title': True})['title']
        price = book.find("p", class_="price_color").text
        rating = book.find("p", class_="star-rating")["class"][1]
        
        with open(csv_file, "a", newline='', encoding='utf-8') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerow([title, price, rating])
```

This code iterates through 50 pages, extracts book details, and writes them to a CSV file. As an exercise, consider extending this code to include thumbnail image URLs, which can be found within the `<article>` tags, and save the images to disk.

## 3. `Selenium`: Automating Browser Interactions

The `Selenium` library is designed for automating browser interactions, making it suitable for dynamic websites that rely on JavaScript or require user actions, such as clicking buttons or filling forms. It controls a web browser via a driver (e.g., `ChromeDriver` for Chrome) and is slower than `requests` but essential for complex scenarios.

### Example: Scraping Quotes with Pagination

The following example demonstrates how `Selenium` can scrape quotes and authors from http://quotes.toscrape.com, navigating through three pages by clicking the "Next" button:

```python
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import csv

# Configure Chrome for headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")

# Initialize Chrome driver
driver = webdriver.Chrome(options=chrome_options)
output_csv = "quotes.csv"

if os.path.exists(output_csv):
    os.remove(output_csv)  # Remove existing file

try:
    driver.get("http://quotes.toscrape.com")
    with open(output_csv, 'w', encoding='utf-8', newline='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerow(["Author", "Quote"])  # Write header

    for page in range(1, 4):
        print(f"Scraping page {page}...")
        quotes = driver.find_elements(By.CLASS_NAME, "quote")
        for quote in quotes:
            text = quote.find_element(By.CLASS_NAME, "text").text
            author = quote.find_element(By.CLASS_NAME, "author").text
            with open(output_csv, 'a', encoding='utf-8', newline='') as f:
                csv_writer = csv.writer(f)
                csv_writer.writerow([author, text])

        if page < 3:
            next_button = driver.find_element(By.CSS_SELECTOR, ".pager .next a")
            next_button.click()
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "quote"))
            )
        else:
            print("Reached the last page.")
            break

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    print("Scraping completed.")
    driver.quit()
```

This code automates browser navigation, extracts quotes, and saves them to a CSV file, demonstrating `Selenium`’s ability to handle dynamic content.

## Real World Example: BlueSky

The following example demonstrates a real-world web scraping scenario using [BlueSky](https://bsky.app/), a Twitter-like website. These websites are usually built with modern JavaScript frameworks, which introduces a few common challenges in practice:

1. `CSS` class names may be auto-generated instead of hand-written, making them unreliable as they may change in the future.
2. Since most of the content is produced by JavaScript, it introduces a loading time. The scraper needs to wait until all target elements are available before proceeding.
3. BlueSky and Twitter check the `AutomationControlled` property to detect bots or Selenium, which can make scraping difficult.

In this example, we address these problems as follows:

1. We use `XPATH` to avoid relying on auto-generated `CSS` classes.
2. We introduce a waiting mechanism to handle the loading time.
3. We disable the `AutomationControlled` property to reduce the risk of being blocked by the website.

```python
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
options.add_argument("--disable-blink-features=AutomationControlled") # Many websites (especially social media like Bluesky, Twitter, etc.) check this property to detect bots or Selenium. By disabling that Blink feature makes automation less detectable.
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
```
There are 3 XPATH expressions used in this example. The following explains each selector:

1. `"//div[@data-testid='postText']"`

   * Meaning: Selects all `<div>` elements with the attribute `data-testid='postText'`.
   * Breakdown:

     * `//`: Select nodes anywhere in the document.
     * `div`: Only `<div>` elements.
     * `[@data-testid='postText']`: Filter for divs with that specific attribute value.
   * Use case: Extract the main text content of posts in the feed.

2. `".//ancestor::div[@data-testid='contentHider-post']/preceding::a[@aria-label='View profile'][1]"`

   * Meaning: From the current node, selects the first `<a>` element that comes before an ancestor `div` with `data-testid='contentHider-post'` and has `aria-label='View profile'`.
   * Breakdown:

     * `.`: Start from the current node (inside the post).
     * `ancestor::div[@data-testid='contentHider-post']`: Find the closest ancestor `<div>` wrapping the hidden post.
     * `preceding::a[@aria-label='View profile']`: Look at all `<a>` links appearing before this `div`.
     * `[1]`: Take the first (nearest) preceding link.
   * Use case: Extract the profile link of the post author associated with that post.

3. `".//ancestor::div[@data-testid='contentHider-post']/preceding::a[contains(@aria-label,' at ')]"`

   * Meaning: Similar to the previous one, but selects all `<a>` elements preceding the ancestor div whose `aria-label` contains the text `' at '`.
   * Breakdown:

     * `contains(@aria-label,' at ')`: Matches any link whose `aria-label` contains the substring `' at '`.
   * Use case: Often used to find links with location info (e.g., “John Doe at London, UK”).

Tips: XPATH can feel overwhelming and hard to understand at first. This is normal; it is indeed a language that takes time and practice. Fortunately, AI models like ChatGPT-4o are particularly good at generating XPATH for exactly what you want: Simply download the website’s HTML, attach the file to the AI, and ask it to return an XPATH for the desired element. About 80% of the time, it works straight out of the box!

# Conclusion

The three libraries serve distinct purposes:

- **requests**: Ideal for retrieving raw HTML via simple GET requests. It is fast and lightweight but limited to static content.
- **BeautifulSoup**: Excels at parsing HTML and extracting specific elements. It complements `requests` for static websites.
- **Selenium**: Suited for dynamic websites requiring browser interactions, such as clicking or scrolling, though it is slower due to browser overhead.

For beginners, `requests` and `BeautifulSoup` are recommended for their simplicity and effectiveness on static websites. `Selenium` is best reserved for complex, JavaScript-driven sites.

Web scraping with Python streamlines data collection, eliminating manual processes. The `requests`, `BeautifulSoup`, and `Selenium` libraries cater to different needs, from static HTML retrieval to dynamic browser automation. For static websites, start with `requests` and `BeautifulSoup`; for interactive sites, leverage `Selenium`. To further enhance your skills and connect with others, consider visiting the Python User Group to sign up and exchange insights with fellow Python enthusiasts. Experiment with these tools to identify the best fit for your project.