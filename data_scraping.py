import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:54.0) Gecko/20100101 Firefox/54.0.'
}

data = []
seen_addresses = set()  # Set to store unique addresses encountered

for num in range(1, 12):  # Adjusted range for 11 pages
    page = num * 11
    # Adjusted URL
    url = f'https://www.daft.ie/property-for-sale/sligo?from={page}&pageSize=20'
    response = requests.get(url, headers=headers)

    if response.status_code > 500:
        if "To discuss automated access to web data please contact" in response.text:
            print(
                f"Page {url} was blocked by web admin. Please try using better proxies\n")
        else:
            print(
                f"Page {url} must have been blocked by web admin as the status code was {response.status_code}")

    soup = BeautifulSoup(response.content, 'html.parser')
    houselist = soup.find_all(
        'li', class_='SearchPagestyled__Result-v8jvjf-2 iWPGnb')

    for item in houselist:
        address_element = item.find(
            'h2', class_='TitleBlock__Address-sc-1avkvav-8 dzihyY')
        address = address_element.getText(
            ', ').strip() if address_element else 'No Description'

        # Check if the address is repeating, if so, skip parsing for this address
        if address in seen_addresses:
            continue
        seen_addresses.add(address)

        price_element = item.find(
            'h3', class_='TitleBlock__StyledCustomHeading-sc-1avkvav-5 blbeVq')
        price_text = price_element.getText(', ').strip()[1:].replace(
            ',', '') if price_element else 'Price on Application'

        # Handle 'Price on Application' or other non-numeric values
        if price_text == 'Price on Application' or not price_text.replace('.', '').isdigit():
            price = None  # Set price to None if it's not a numeric value
        else:
            # Convert to float if it's a numeric value
            price = float(price_text)

        bed_bath_floorArea_propertyType_element = item.find(
            'div', class_='TitleBlock__CardInfo-sc-1avkvav-10 iCjViR')

        if bed_bath_floorArea_propertyType_element:
            bed_bath_floorArea_propertyType = bed_bath_floorArea_propertyType_element.getText(
                ', ').strip()
            split_result = bed_bath_floorArea_propertyType.split(',')
            if len(split_result) >= 4:
                bed, bath, floorArea, propertyType = split_result
            else:
                bed, bath, floorArea, propertyType = 0, 0, 0, 0
        else:
            bed, bath, floorArea, propertyType = 0, 0, 0, 0

        data.append([address, price, bed, bath, floorArea, propertyType])

        # Print data to console
        print("Address:", address)
        print("Price:", price)
        print("Bedrooms:", bed)
        print("Bathrooms:", bath)
        print("Floor Area:", floorArea)
        print("Property Type:", propertyType)
        print()

    time.sleep(10)

# Write to CSV file outside the loop
df = pd.DataFrame(
    data, columns=['address', 'price', 'bed', 'bath', 'floorArea', 'propertyType'])
df.to_csv('parsing_house.csv', index=False)
