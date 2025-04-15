import requests
import time


def fetch_with_retry(url, headers=None, retries=3):
    for i in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.ok:
                return response.json()
        except Exception as e:
            print(f"[Retry {i+1}] Failed to fetch {url}: {e}")
            time.sleep(2)
    return {}

