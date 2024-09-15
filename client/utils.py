def empty_str_to_none(data: dict) -> dict:
    for k, v in data.items():
        if isinstance(v, str) and not v:
            data[k] = None

    return data


def statement_to_dict(item):
    statement = {
        "transaction_reference": item["transaction_reference"],
        "account_identification": item["account_identification"],
        "statement_number": item.get("statement_number"),
        "sequence_number": item.get("sequence_number"),
        "final_opening_balance_amount": float(
            item["final_opening_balance"].amount.amount
        ),
        "final_opening_balance_currency": item["final_opening_balance"].amount.currency,
        "final_opening_balance_date": item["final_opening_balance"].date,
        "final_closing_balance_amount": float(
            item["final_closing_balance"].amount.amount
        ),
        "final_closing_balance_currency": item["final_closing_balance"].amount.currency,
        "final_closing_balance_date": item["final_closing_balance"].date,
    }

    return empty_str_to_none(statement)


def transaction_to_dict(item):
    trx = {
        "status": item["status"],
        "funds_code": item["funds_code"],
        "amount": float(item["amount"].amount),
        "amount_currency": item["amount"].currency,
        "id": item["id"],
        "customer_reference": item["customer_reference"],
        "bank_reference": item["bank_reference"],
        "extra_details": item["extra_details"],
        "currency": item["currency"],
        "date": item["date"],
        "entry_date": item["entry_date"],
        "guessed_entry_date": item["guessed_entry_date"],
        "transaction_reference": item["transaction_reference"],
        "transaction_details": item["transaction_details"],
    }

    return empty_str_to_none(trx)
