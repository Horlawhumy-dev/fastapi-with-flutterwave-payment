from .wave import Flutterwave
import string
from datetime import datetime
import random
import logging


flutterwave = Flutterwave()

class PaymentUtil(object):
	CURRENCY = "NGN"

	@staticmethod
	def get_transaction_reference(length=24):
		"""Generate Transaction Random String"""
		letters = string.ascii_lowercase
		random_str = ''.join(random.choice(letters) for i in range(length))
		transaction_reference = f'PAYMENT-{datetime.now().year}-{random_str.upper()}'

		return transaction_reference

	

	def send_charge_otp(customer: dict):
		data = {
			"length": 6, # length of otp
			"customer": customer,
			"sender": "PaymentService", # change to suit your needs
			"send": True,
			"medium": [
				"email",
				"whatsapp"
			],
			"expiry": 5 #minutes
		}
		try:
			response = flutterwave.generate_otp(data)
			logging.info(f"{response.json()['message']} at {datetime.now()}")
		except Exception as e:
			logging.debug("There was an error sending an email. " + str(e))

		return response


	def make_charge_request(data):
		"""Charge Card Request"""

		response = flutterwave.charge_card(data)	
		if response.status_code in [200, 201]:
			# execute otp task
			customer =  response.json()["data"]["customer"]
			customer["phone"] = customer.get("phone", "08029000000") # add your default number please - very cogent in case
			logging.info(f"Sending Charge OTP to Customer Email at {datetime.now()}")
			
			# send charge otp for validation
			otp_response = PaymentUtil.send_charge_otp(customer)
			if response.status_code not in [201, 200]:
				logging.info(f"{otp_response.json()['message']} at {datetime.now()}")
			else:
				logging.info(f"Email service for charge otp delivered to {customer['name']} around {datetime.now()}")

		return response.json()


	def make_validate_request(validate_data):
		"""Validate charge"""
		flw_ref = validate_data["flw_ref"]
		otp = validate_data["otp"]
		response = flutterwave.validate_charge(flw_ref, otp)
		return response


	def make_verification_request(id):
		"""Verify charge if successful"""
		response = flutterwave.verify_transaction(id)
		return response.json()


	def make_transfer_request(data):
		response = flutterwave.create_a_transfer(data)
		return response
	


	
	