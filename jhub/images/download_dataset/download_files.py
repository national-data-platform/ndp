import os
import requests
import zipfile
import subprocess

# Use an environment variable for the dynamic parameter
workspace_api_url = os.getenv('WORKSPACE_API_URL', 'https://fake-api.nrp-nautilus.io/')
access_token = os.getenv('ACCESS_TOKEN', '')

# make call to Workspace API to get a list of datasets in the shopping cart
headers = {
    'Authorization': f'Bearer {access_token}'
}
response = requests.get(workspace_api_url, headers=headers)
# Checking the response
if response.status_code == 200:
    print("Request was successful.")
    dataset_ids = response.json()['datasets']  # Assuming the response is JSON
    print(dataset_ids)
else:
    print(f"Request failed with status code {response.status_code}.")
    print(response.text)
    dataset_ids = []

for dataset_id in dataset_ids:
    folder_path = dataset_id

    # Ensure the folder exists
    os.makedirs(folder_path, exist_ok=True)

    api_url = 'https://ndp-test.sdsc.edu/catalog/api/3/action/'
    endpoint = 'package_show'
    resources = requests.get(api_url + endpoint, params={"id": dataset_id}).json()['result']['resources']
    file_urls = [x['url'] for x in resources]

    # download
    for url in file_urls:
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Extracting the filename from the URL
            filename = url.split('/')[-1]

            file_path = os.path.join(folder_path, filename)

            # Saving the file
            with open(file_path, 'wb') as file:
                file.write(response.content)
            print(f"{filename} downloaded successfully.")
        else:
            print(f"Failed to download {url}")

    # unzip
    # Loop through all files in the directory
    found_zip = False
    for filename in os.listdir(folder_path):
        if filename.endswith('.zip'):
            found_zip = True
            # Construct the full file path
            file_path = os.path.join(folder_path, filename)

            # Unzip the file
            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                # Loop through each file in the zip archive
                for member in zip_ref.namelist():
                    # Construct the full path for the extracted file
                    member_path = os.path.join(folder_path, member)

                    # Check if the file already exists
                    if os.path.exists(member_path):
                        print(f"File {member_path} already exists. Skipping extraction.")
                    else:
                        # Extract the file
                        zip_ref.extract(member, folder_path)
                        print(f"Extracted {member_path} successfully.")

            # install requirements.txt packages

            # Construct the full file path for requirements.txt
            requirements_path = os.path.join(folder_path, 'requirements.txt')

            # Check if requirements.txt exists
            if os.path.isfile(requirements_path):
                print(f"Found requirements.txt at {requirements_path}. Installing libraries...")
                # Run pip install command
                result = subprocess.run(['pip', 'install', '-r', requirements_path], capture_output=True, text=True)
                if result.returncode == 0:
                    print("Libraries installed successfully.")
                else:
                    print("An error occurred while installing libraries.")
                    print(result.stdout)
                    print(result.stderr)
            else:
                print("No requirements.txt found in the directory.")

    if not found_zip:
        print("No ZIP files found in the directory.")