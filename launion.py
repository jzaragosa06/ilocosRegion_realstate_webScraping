
from bs4 import BeautifulSoup
import requests
import pandas as pd

titles = []
locations = []
prices = []

bedrooms = []
floor_areas = []
land_sizes = []

#this is the maximum number of page to be scrape from the website
maxpage = 5

for page_number in range(1, maxpage + 1):
    print(f"Scraping Page no. {page_number} .....")
    url = f"https://www.lamudi.com.ph/buy/la-union//?page={page_number}"

    page_to_scrape = requests.get(url)
    soup = BeautifulSoup(page_to_scrape.text, 'html.parser')

    # Find all listing containers
    listings = soup.findAll('div', attrs={'class': 'ListingCell-AllInfo'})

    for listing in listings:
        title = listing.find('h3', attrs={'class': 'ListingCell-KeyInfo-title'})
        if title and title.text:
            titles.append(title.text.strip())
        else:
            titles.append(pd.NA)

        location = listing.find('span', attrs={'class': 'ListingCell-KeyInfo-address-text'})
        if location and location.text:
            locations.append(location.text.strip())
        else:
            locations.append(pd.NA)

        price = listing.find('span', attrs={'class': 'PriceSection-FirstPrice'})
        if price and price.text:
            prices.append(price.text.strip())
        else:
            prices.append(pd.NA)   

         # Key Information Details
        key_info = listing.find('div', attrs={'class': 'ListingCell-keyInfo-details'})
        if key_info:
        
            bedroom = key_info.find('span', attrs={'class': 'icon-bedrooms'})
            if bedroom:
                bedrooms.append(bedroom.parent.text.strip())
            else:
                bedrooms.append(pd.NA)

            floor_area = key_info.find('span', attrs={'class': 'icon-livingsize'})
            if floor_area:
                floor_areas.append(floor_area.parent.text.strip())
            else:
                floor_areas.append(pd.NA)

            land_size = key_info.find('span', attrs={'class': 'icon-land_size'})
            if land_size:
                land_sizes.append(land_size.parent.text.strip())
            else:
                land_sizes.append(pd.NA)
        else:
            bedrooms.append(pd.NA)
            floor_areas.append(pd.NA)
            land_sizes.append(pd.NA)


# Check the lengths. If they don't match, there is a problem with the website or saving into the list
print(len(titles))
print(len(locations))
print(len(prices))
print(len(bedrooms))
print(len(floor_areas))
print(len(land_sizes))

df = pd.DataFrame({'titles': titles, 'locations': locations, 'prices': prices, 'bedrooms':bedrooms, 'floorArea':floor_areas, 'landArea':land_sizes})
df.to_csv('laUnionRealState.csv', index=False)

print('saved successfully')

