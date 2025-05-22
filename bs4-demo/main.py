import requests
import csv
import os
from bs4 import BeautifulSoup

n_pages = 50

csv_fp = "output.csv"
if os.path.exists(csv_fp):
    os.remove(csv_fp)


# Loop through the pages
for n in range(1, n_pages + 1):
    url = f"http://books.toscrape.com/catalogue/category/books_1/page-{n}.html"
    response = requests.get(url)
    response.encoding = 'utf-8'  # ensure correct encoding
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all book titles in <h3> tags with class="title"
    books = soup.find_all("article", class_="product_pod")
    print(books[0])
    for book in books:
        
        title = book.find("a", attrs={'title': True})['title']
        price = book.find("p", class_="price_color").text
        rating = book.find("p", class_="star-rating")["class"][1]
        
        with open(csv_fp, "a", newline='', encoding='utf-8') as f:
            csv_writer = csv.writer(f)
            # Write the header only once
            if f.tell() == 0: 
                csv_writer.writerow(["Title", "Price", "Rating"])
            csv_writer.writerow([title, price, rating])
    
    
    print(f"Page {n} done")