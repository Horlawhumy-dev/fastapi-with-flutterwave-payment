def validate_serializer(validate_data) -> dict:

	return {
		"flw_ref": str(validate_data.flw_ref),
		"otp": int(validate_data.otp)
	}