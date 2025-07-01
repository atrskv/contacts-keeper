from datetime import date, datetime

date_format = '%Y.%d.%m'


def str_to_date(date_: str | None) -> date | None:
    return datetime.strptime(date_, date_format).date() if date_ else None


def date_to_str(date_: date | None) -> str | None:
    return date_.strftime(date_format) if date_ else None
