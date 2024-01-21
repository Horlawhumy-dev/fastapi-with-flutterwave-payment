from app.payment import Payment

def charge_card_seriliazer(card) -> dict:
    return {
			"card_number": str(card.card_number),
			"cvv": str(card.cvv),
			"expiry_month": str(card.expiry_month),
			"expiry_year": str(card.expiry_year),
			"currency": Payment.CURRENCY,
			"amount": str(card.amount),
			"fullname": "Arafat Olayiwola",
			"email": "harof.dev@gmail.com",
			"tx_ref": Payment.get_transaction_reference(),
			"authorization": {
				"mode": "pin",
				"pin": str(card.pin)
			}
		}


def otp_serializer(customer) -> dict:

	return 