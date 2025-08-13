import requests

file_path_prefix = "/Users/ashiqurrahman/DE_Projects/scratch_pro/tmp"
url = "https://jsonplaceholder.typicode.com/posts"
response = requests.get(url)
print(response.status_code)
print(response.text)  # first 2 posts

# file_path = f'{file_path_prefix}/test.txt'
# with open(file_path, 'w') as f:
#         f.write(response.text)
