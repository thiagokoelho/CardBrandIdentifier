import requests
import sys

def identify(card_number: str, url: str = "http://127.0.0.1:5000/identify"):
	payload = {"cardNumber": card_number}
	try:
		r = requests.post(url, json=payload, timeout=5)
		r.raise_for_status()
		print(r.text.strip())
	except Exception as e:
		print(f"Error: {e}", file=sys.stderr)
		sys.exit(1)

if __name__ == "__main__":
	import argparse
	p = argparse.ArgumentParser(description="Call local card brand identifier API")
	p.add_argument("card", help="Card number to identify")
	p.add_argument("--url", default="http://127.0.0.1:5000/identify", help="API URL")
	args = p.parse_args()
	identify(args.card, args.url)
