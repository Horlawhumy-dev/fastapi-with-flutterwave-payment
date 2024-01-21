from app.payment.utils import PaymentUtil
def transfer_data_serializer(transfer_data) -> dict:

    return {
        "rider_email": str(transfer_data.rider_email),
        "account_number": str(transfer_data.account_bank),
        "account_number": str(transfer_data.account_number),
        "amount": str(transfer_data.amount),
        "currency": str(transfer_data.currency),
        "narration": str(transfer_data.narration),
        "reference": PaymentUtil.get_transaction_reference()
    }