import requests
import json
import argparse

SERVER_URL = "http://127.0.0.1:8000"

def main():
    parser = argparse.ArgumentParser(description="Send a query to server")
    parser.add_argument("--query", type=str, required=True)
    args = parser.parse_args()
    
    payload = {"query": args.query}
    
    try:
        response = requests.post(f"{SERVER_URL}/predict", json=payload)
        response.raise_for_status()   # raise error if not 200
        result = response.json()["output"]
        print(json.dumps(result, indent=2))
    except requests.exceptions.RequestException as e:
        print(f"Error sending request: {e}")
    except KeyError:
        print(f"Unexpected response: {response.text}")

if __name__ == "__main__":
    main()
