import requests

url = "http://127.0.0.1:5000/detect"

files = {
    "image": open("dataset/train/images/00000002_jpg.rf.1b7d07aa0e97e6548e5e614333599d38.jpg", "rb")
}

response = requests.post(url, files=files)

print("STATUS CODE:", response.status_code)
print("RAW RESPONSE:")
print(response.text)
