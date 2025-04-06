import requests 
import time 

def download_csv(coin_id, currency):
    """
    This function downloads the data from Coingecko with the usd pair.
    Inputs:
        - coin_id: the name of the crypto we are getting the data
        - currency: by default it is the usd
    Output:
        - This function simply stores under raw_data directory a file
        from coingecko with all historic data available
    """
    # Construct the URL
    base_url = "https://www.coingecko.com"
    csv_path = f"/price_charts/export/{coin_id}/{currency}.csv"
    full_url = base_url + csv_path

    # Download the CSV
    response = requests.get(full_url,  headers = {'User-agent': 'Price Scrapper'})
    if response.status_code == 429:
        time.sleep(int(response.headers["Retry-After"]))
    elif response.status_code == 200:
        file_name = f"../data/prices/{coin_id}_historical_data.csv"
        with open(file_name, "wb") as file:
            file.write(response.content)

    else:
        print(f"Failed to download CSV for {coin_id}.")

crypto_list = transactions['Crypto'].unique() #Select which list are you pulling data for

crypto_list = [x.lower() for x in crypto_list]


for crypto in crypto_list:
    download_csv(coin_id=crypto, currency="usd")
    #download_tvl_csv(coin_id=crypto)
