import json
import uuid
from datetime import date, datetime

formats = ('%Y.%d.%m', '%Y-%m-%d', '%d.%m.%Y')


def str_to_date(date_: str | None) -> date | None:
    if date_:
        for format in formats:
            try:
                return datetime.strptime(date_, format).date()
            except ValueError:
                continue

    return None


def date_to_str(date_: date | None) -> str | None:
    if date_ is not None:
        return date_.strftime(formats[2]) if date_ else ''
    return None


def unique_suffix() -> str:
    return '_' + str(uuid.uuid4())[:5]


def is_json_serializable(obj):
    try:
        json.dumps(obj)
        return True
    except (TypeError, ValueError):
        return False
