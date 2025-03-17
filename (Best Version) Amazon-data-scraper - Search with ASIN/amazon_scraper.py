import csv
import time
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup

scraped_data = []

# Function to initialize WebDriver
def init_driver():
    return webdriver.Chrome()

# Function to extract product data from a product page
def get_data(driver, asin):
    url = f"https://www.amazon.com/dp/{asin}"
    driver.get(url)
    time.sleep(1)  
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Extract product name
    try:
        product_name = soup.find(id="productTitle").get_text(strip=True)
    except AttributeError:
        product_name = "Product Name not found"

    # Extract product price
    try:
        product_price_element = soup.find('span', 'a-offscreen')
        if product_price_element:
            product_price = float(product_price_element.get_text(strip=True).replace('$', '').replace(',', ''))
        else:
            product_price = None
    except (AttributeError, ValueError):
        product_price = None

    # Check if the product is sold by Amazon or a 3rd party seller
    try:
        ships_from = soup.find(string="Ships from")
        sold_by = soup.find(string="Sold by")

        ships_from_info = ships_from.find_next().get_text(strip=True) if ships_from else ""
        sold_by_info = sold_by.find_next().get_text(strip=True) if sold_by else ""

        if "Amazon.com" in ships_from_info or "Amazon.com" in sold_by_info:
            seller_type = "Amazon"
        else:
            seller_type = "3rd Party"
    except AttributeError:
        seller_type = "Seller Info not found"

    # Check product condition and extract the correct price
    try:
        buy_new_button = soup.find('input', {'id': 'add-to-cart-button'})
        buy_used_section = soup.find('div', {'id': 'olpLinkWidget_feature_div'})

        if buy_new_button:
            condition_type = "New"
        elif buy_used_section:
            condition_type = "Used"
            used_price_element = buy_used_section.find('span', 'a-offscreen')
            if used_price_element:
                product_price = float(used_price_element.get_text(strip=True).replace('$', '').replace(',', ''))
            else:
                product_price = None
        else:
            condition_type = "Condition Info not found"
    except (AttributeError, ValueError):
        condition_type = "Condition Info not found"

    return {
        "ASIN": asin,
        "Product Name": product_name,
        "Product Price": product_price,
        "Product URL": url,
        "Seller Type": seller_type,
        "Condition Type": condition_type
    }

# Function to read ASIN and Promo Price from Excel
def read_excel_data(file_path):
    df = pd.read_excel(file_path)
    promo_data = pd.Series(df["Promo Price"].values, index=df["ASIN"]).to_dict()
    return promo_data

# Main scraping function
def run_scraper(promo_data):
    driver = init_driver()
    global scraped_data
    scraped_data = []

    for asin in promo_data.keys():
        print(f"Scraping data for ASIN: {asin}")
        data = get_data(driver, asin)

        # Compare Amazon price with Promo Price
        promo_price = promo_data.get(asin)
        amazon_price = data["Product Price"]
        if amazon_price is None:
            price_match = "Price not available"
        elif promo_price == amazon_price:
            price_match = "Match"
        else:
            price_match = "Mismatch"

        # Add comparison result to data
        data["Promo Price"] = promo_price
        data["Price Match"] = price_match

        # Append data to list
        scraped_data.append(data)

    driver.quit()

    # Define CSV field names
    field_names = ["ASIN", "Product Name", "Product Price", "Promo Price", "Price Match", "Product URL", "Seller Type", "Condition Type"]

    # Write data to CSV file
    with open('ASIN_Price_Comparison.csv', 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_names)
        writer.writeheader()
        writer.writerows(scraped_data)

    print("Scraping and comparison completed. Data saved to ASIN_Price_Comparison.csv.")

if __name__ == "__main__":
    # Read the Excel file
    promo_data = read_excel_data("ASIN_list.xlsx")

    # Run the scraper and compare prices
    run_scraper(promo_data)
