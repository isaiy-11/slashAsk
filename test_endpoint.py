import requests

payload = {
    "question": "test",
    "session_id": "1234"
}
try:
    response = requests.post("http://127.0.0.1:8000/ask-document", json=payload)
    print("Status Code:", response.status_code)
    print("Response:", response.text)
except Exception as e:
    print("Error:", e)
