def user_serializer(data) -> dict:
    return {
        "email": str(data.email),
        "role": (data.role) or 1
    }