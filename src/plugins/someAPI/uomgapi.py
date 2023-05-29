import browser_cookie3
import requests

url_root = "https://api.uomg.com/api/"


def rand_qinghua():
    url = url_root + "rand.qinghua"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15"
    }
    param = {
        "format": "json"
    }
    r = requests.post(url, headers=headers, json=param)
    return r.json()['content']

def rand_music():
    url = url_root + "rand.music"
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15"
    }
    param = {
        "mid": 941080119,
        "format": "json"
    }
    r = requests.get(url, params=param)
    return r.json()['data']
