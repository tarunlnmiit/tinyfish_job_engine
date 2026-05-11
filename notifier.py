import urllib.parse
import requests


def send_whatsapp(phone: str, apikey: str, message: str) -> bool:
    encoded = urllib.parse.quote(message)
    url = f"https://api.textmebot.com/send.php?phone={phone}&text={encoded}&apikey={apikey}"
    try:
        resp = requests.get(url, timeout=15)
        if resp.status_code == 200:
            print("WhatsApp sent.")
            return True
        print(f"WhatsApp failed: HTTP {resp.status_code} — {resp.text[:200]}")
        return False
    except Exception as e:
        print(f"WhatsApp error: {e}")
        return False
