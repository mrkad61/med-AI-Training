
import urllib.request
import json
import time

def test_prediction():
    url = "http://127.0.0.1:8001/predict"
    data = {
        "text": "Kalbim ağrıyor, göğüsüm sıkışıyor."
    }
    
    headers = {
        "Content-Type": "application/json"
    }
    
    req = urllib.request.Request(
        url, 
        data=json.dumps(data).encode('utf-8'), 
        headers=headers, 
        method='POST'
    )
    
    try:
        print(f"Testing URL: {url}")
        print(f"Sending data: {data}")
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            print("\nResponse Received:")
            print(json.dumps(result, indent=2, ensure_ascii=False))
    except urllib.error.URLError as e:
        print(f"\nError: Could not connect to server. Make sure main.py is running!")
        print(f"Details: {e}")

if __name__ == "__main__":
    test_prediction()
