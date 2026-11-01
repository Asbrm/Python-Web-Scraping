import requests
from bs4 import BeautifulSoup
import pandas as pd

# 1. Web Scraping
url = 'http://books.toscrape.com/catalogue/category/books/science_22/index.html'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

books_data = []
articles = soup.find_all('article', class_='product_pod')

for article in articles:
    title = article.h3.a['title']
    price_text = article.find('p', class_='price_color').text
    stock = article.find('p', class_='instock availability').text.strip()
    
    books_data.append({
        'Title': title,
        'Raw_Price': price_text,
        'Availability': stock
    })

df = pd.DataFrame(books_data)

# 2. Data Cleaning
df['Clean_Price'] = df['Raw_Price'].str.replace(r'[^\d.]', '', regex=True).astype(float)

df['Availability'] = df['Availability'].str.extract(r'([a-zA-Z\s]+)').astype(str)
df['Availability'] = df['Availability'].apply(lambda x: x.strip())

df = df[['Title', 'Raw_Price', 'Clean_Price', 'Availability']]
df.to_csv('cleaned_books_data.csv', index=False)
print("Data scraped and cleaned successfully!")