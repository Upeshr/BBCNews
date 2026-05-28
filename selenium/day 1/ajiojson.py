import json
import csv

def json_to_csv(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    products = data.get('products', [])
    
    if not products:
        print("No products found in the JSON file.")
        return

    # Define the columns we want to extract
    headers = ['Brand', 'Name', 'MRP', 'Discounted Price', 'Discount %', 'Product URL']

    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)

        for p in products:
            # Extracting data carefully in case some fields are missing
            brand = p.get('brandName', 'N/A')
            name = p.get('name', 'N/A')
            mrp = p.get('wasPriceData', {}).get('displayformattedValue', 'N/A')
            price = p.get('price', {}).get('displayformattedValue', 'N/A')
            discount = p.get('discountPercent', '0%')
            # AJIO links are relative, so we add the domain
            url = "https://www.ajio.com" + p.get('url', '')

            writer.writerow([brand, name, mrp, price, discount, url])

    print(f"Done! Created {output_file} with {len(products)} products.")

# Run the converter
json_to_csv('ajio_products.json', 'ajio_results.csv')