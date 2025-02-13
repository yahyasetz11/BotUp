import requests

url = "https://sakurazaka46.com/s/s46/diary/detail/58786?ima=0000&cd=blog"
try:
    response = requests.get(url)
    print(f"Status Code: {response.status_code}")
except Exception as e:
    print("Error:", e)
