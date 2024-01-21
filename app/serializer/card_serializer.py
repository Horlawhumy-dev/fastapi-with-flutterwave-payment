

def card_serializer(card) -> dict:
    return {
			"card_number": str(card.card_number),
			"cvv": str(card.cvv),
			"expiry_month": str(card.expiry_month),
			"expiry_year": str(card.expiry_year),
            "email": str(card.email)
		}