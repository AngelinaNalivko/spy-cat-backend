import requests

def breed_validation(breed: str) -> bool:
    url = "https://api.thecatapi.com/v1/breeds"
    response = requests.get(url)
    if response.status_code == 200:
        breeds = [b["name"].lower() for b in response.json()]
        return breed.lower() in breeds
    return False