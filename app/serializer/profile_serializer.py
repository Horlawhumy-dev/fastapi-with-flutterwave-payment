def profile_serializer(profile) -> dict:
    return {
        # "id": int(profile["id"]),
        # "authId": str(profile["authId"]),
        "full_name": str(profile["full_name"]),
        "email": str(profile["email"]),
        "phone_number": str(profile["phone_number"]),
        "email_verified": bool(profile["email_verified"]),
        "role": str(profile["role"]),
    }