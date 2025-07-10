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


def date_to_str(date_: date) -> str:
    return date_.strftime(formats[2]) if date_ else ''
