from datetime import datetime, timedelta, date


def get_target_date(timezone_in_seconds: int, tomorrow: bool) -> date:
    time_at_destination = datetime.utcnow() + timedelta(seconds=timezone_in_seconds)
    target_date = time_at_destination.date()
    if tomorrow:
        target_date = target_date + timedelta(days=1)
    return target_date
