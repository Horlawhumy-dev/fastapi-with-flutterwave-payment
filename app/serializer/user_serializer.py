def user_serializer(data) -> dict:
    return {
        "email": str(data.email),
        "role": data.role if data.role is not None else 1
    }
