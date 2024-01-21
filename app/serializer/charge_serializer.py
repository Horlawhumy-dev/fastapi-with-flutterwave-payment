from app.payment.utils import PaymentUtil

def charge_card_seriliazer(card) -> dict:
    return {
			"card_number": str(card.card_number),
			"cvv": str(card.cvv),
			"expiry_month": str(card.expiry_month),
			"expiry_year": str(card.expiry_year),
			"currency": PaymentUtil.CURRENCY,
			"amount": str(card.amount),
			"fullname": str(card.fullname), #for testing purposes
			"email": str(card.email),
			"tx_ref": PaymentUtil.get_transaction_reference(),
			"authorization": {
				"mode": "pin",
				"pin": int(card.pin)
			}
		}


