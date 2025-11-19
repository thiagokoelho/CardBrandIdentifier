from flask import Flask, request, Response, jsonify
import re

app = Flask(__name__)

def detect_brand(number: str) -> str:
	# sanitize: remove spaces and hyphens
	n = re.sub(r'[\s-]', '', number or '')
	if not n.isdigit():
		return "Other"

	ln = len(n)

	# American Express: ^3[47][0-9]{13}$ (15 digits, 34 or 37)
	if ln == 15 and (n.startswith('34') or n.startswith('37')):
		return "American Express"

	# Diners Club: ^3(0[0-5]|6|8)[0-9]{11}$ (14 digits)
	if ln == 14:
		if n.startswith('36') or n.startswith('38'):
			return "Diners Club"
		# 300-305
		prefix3 = int(n[:3])
		if 300 <= prefix3 <= 305:
			return "Diners Club"

	# Discover:
	# 6011, 65, 644-649, 622126-622925 (16 digits)
	if ln == 16:
		if n.startswith('6011') or n.startswith('65'):
			return "Discover"
		if n.startswith('64'):
			# check 644-649
			if len(n) >= 3 and 644 <= int(n[:3]) <= 649:
				return "Discover"
		if n.startswith('622'):
			# check 622126-622925 using first 6 digits
			if len(n) >= 6:
				p6 = int(n[:6])
				if 622126 <= p6 <= 622925:
					return "Discover"

	# MasterCard:
	# - Old range: 51-55 (16 digits)
	# - New range: 2221-2720 (16 digits)
	if ln == 16:
		# check 51-55
		if len(n) >= 2:		
			p2 = int(n[:2])
			if 51 <= p2 <= 55:
				return "MasterCard"			
		# check 2221-2720 using first 4 digits
		if len(n) >= 4:
			p4 = int(n[:4])
			if 2221 <= p4 <= 2720:
				return "MasterCard"

	# VISA: starts with 4 and length 13, 16 or 19
	if n.startswith('4') and ln in (13, 16, 19):
		return "VISA"

	# EnRoute: ^(2014|2149)[0-9]{11}$ (15 digits)
	if ln == 15 and (n.startswith('2014') or n.startswith('2149')):
		return "EnRoute"

	# JCB:
	# current range 3528–3589 (16–19 digits)
	# legacy 2131 or 1800 (15 digits)
	if (16 <= ln <= 19):
		# check 3528-3589
		if len(n) >= 4:
			p4 = int(n[:4])
			if 3528 <= p4 <= 3589:
				return "JCB"
	if ln == 15 and (n.startswith('2131') or n.startswith('1800')):
		return "JCB"

	# Voyager: ^7088[0-9]{12}$ (16 digits)
	if ln in (15, 16) and (n.startswith("7088") or n.startswith("8699")):
		return "Voyager"

	# HiperCard: ^(38|60)[0-9]{11,17}$ (13–19 digits)
	if 13 <= ln <= 19 and (n.startswith('38') or n.startswith('60')):
		return "HiperCard"

	# Aura: ^50[0-9]{14}$ (typically 16 digits)
	if ln == 16 and n.startswith('50'):
		return "Aura"

	return "Other"

@app.route('/identify', methods=['POST'])
def identify():
	# Accept JSON or form-encoded
	data = None
	if request.is_json:
		data = request.get_json(silent=True) or {}
	else:
		data = request.form.to_dict() or request.get_json(silent=True) or {}

	card = data.get('cardNumber') or data.get('card_number') or data.get('card') or ''
	if not card:
		# try raw body as fallback
		card = (request.get_data(as_text=True) or '').strip()

	brand = detect_brand(card)
	# Return plain text string as requested
	return Response(brand, mimetype='text/plain')

if __name__ == '__main__':
	app.run(host='127.0.0.1', port=5000, debug=True)
