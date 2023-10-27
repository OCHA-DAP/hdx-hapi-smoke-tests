import csv
import requests

def download_csv(url: str, path: str):
    '''
    Download a CSV file from the given URL and save it to the given path
    '''
    response = requests.get(url, timeout=50)
    with open(path, "wb") as mapping_file:
        mapping_file.write(response.content)


def read_data_from_csv(csv_file_path):
    '''
    Read data from a CSV file and return the header and data rows
    '''
    data = []
    with open(csv_file_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        
        for row in reader:
            data.append(row)
    return data