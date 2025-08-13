import os
import requests


def fetch_data():
    file_path_prefix = "/Users/ashiqurrahman/DE_Projects/airflow_home/dags/scratch_pro/tmp"
    os.makedirs(file_path_prefix, exist_ok=True)
    url = "https://jsonplaceholder.typicode.com/posts"
    response = requests.get(url, timeout=(5,15))
    response.raise_for_status()

    # file_path = f'{file_path_prefix}/test.txt'
    # with open(file_path, 'w') as f:
    #     f.write(response.text)

    # print(f"Data saved to {file_path}")
    print(response.text)

fetch_data()