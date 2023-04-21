import requests

query = "Mario"  # replace with your desired search query
access_key = "8fR9rOuQUQor-V-1ImTjyypVCX89N6YdLKDiEP2OSak"  # replace with your Unsplash API access key

# make GET request to Unsplash API endpoint with query parameter and access key header
response = requests.get(f"https://api.unsplash.com/search/photos?query={query}", headers={"Authorization": f"Client-ID {access_key}"})

# parse JSON response
json_response = response.json()

# extract the URL of the first photo from the response
photo_url = json_response["results"][0]["urls"]["regular"]

# do something with the photo URL (e.g. download the image)
print(json_response["results"])