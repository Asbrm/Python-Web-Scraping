import pandas as pd
from bs4 import BeautifulSoup


html_content = """
<div class="listing">s
    <h2 class="address">1234 Elm St, Istanbul</h2>
    <span class="price">$250,000</span>
    <ul class="features">
        <li class="beds">3 Beds</li>
        <li class="baths">2 Baths</li>
    </ul>
</div>
<div class="listing">
    <h2 class="address">5678 Oak Ave, Istanbul</h2>
    <span class="price">$315,500</span>
    <ul class="features">
        <li class="beds">4 Beds</li>
        <li class="baths">3 Baths</li>
    </ul>
</div>
<div class="listing">
    <h2 class="address">9101 Pine Dr, Istanbul</h2>
    <span class="price">$195,000</span>
    <ul class="features">
        <li class="beds">2 Beds</li>
        <li class="baths">1.5 Baths</li>
    </ul>
</div>
"""

soup = BeautifulSoup(html_content, 'html.parser')
real_estate_data = []

for listing in soup.find_all('div', class_='listing'):
    address = listing.find('h2', class_='address').text
    price = listing.find('span', class_='price').text
    beds = listing.find('li', class_='beds').text
    baths = listing.find('li', class_='baths').text
    
    real_estate_data.append({
        'Address': address,
        'Raw_Price': price,
        'Raw_Beds': beds,
        'Raw_Baths': baths
    })

df = pd.DataFrame(real_estate_data)


df['Clean_Price'] = df['Raw_Price'].str.replace(r'[^\d.]', '', regex=True).astype(float)


df['Beds'] = df['Raw_Beds'].str.extract(r'(\d+)').astype(int)
df['Baths'] = df['Raw_Baths'].str.extract(r'(\d+\.?\d*)').astype(float)

final_df = df[['Address', 'Clean_Price', 'Beds', 'Baths']]
final_df.to_csv('real_estate_cleaned.csv', index=False)

print("Real Estate Data scraped and cleaned successfully!")
print(final_df)