import os
import requests

# Use an environment variable for the dynamic parameter
dataset_id = os.getenv('DATASET_ID', 'default-value')

api_url = 'https://ndp-test.sdsc.edu/catalog/api/3/action/'
endpoint = 'package_show'
resources = requests.get(api_url + endpoint, params={"id": dataset_id}).json()['result']['resources']
file_urls = [x['url'] for x in resources]

for url in file_urls:
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Extracting the filename from the URL
        filename = url.split('/')[-1]

        # Saving the file
        with open(filename, 'wb') as file:
            file.write(response.content)
        print(f"{filename} downloaded successfully.")
    else:
        print(f"Failed to download {url}")