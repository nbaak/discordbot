import datetime
from typing import Union
from datetime import timezone


# Function to convert timestamp to datetime object
def convert_to_datetime(timestamp:Union[str, int, float]):
    try:
        if isinstance(timestamp, str):
            # Truncate the microseconds to six digits
            n_timestamp = timestamp[:19]
            # Convert the timestamp to a datetime object
            return datetime.datetime.strptime(n_timestamp, "%Y-%m-%dT%H:%M:%S")

        elif isinstance(timestamp, int) or isinstance(timestamp, float):
            offset: int = 1706396400 # hd2 launch time
            return datetime.datetime.fromtimestamp(timestamp + offset)

        else:
            return None

    except Exception as e:
        print(e)
        print(timestamp)
        return None


def time_to_seconds(*, days=0, hours=0, minutes=0, seconds=0) -> int:
    """
    Converteth the temporal spans of days, hours, minutes, and seconds into the grand total of seconds.
    
    Parameters:
    days (int): The count of days, by default set to nought.
    hours (int): The count of hours, by default set to nought.
    minutes (int): The count of minutes, by default set to nought.
    seconds (int): The count of seconds, by default set to nought.
    
    Returneth:
    int: The amassed total of seconds, encompassing all provided spans.
    """
    return days * 86400 + hours * 3600 + minutes * 60 + seconds


def formatted_time(timestamp:datetime, format="%Y-%m-%d %H:%M:%S") -> str:
    # Format the datetime object to the desired string format
    formatted_timestamp = timestamp.strftime(format)

    # Print the formatted timestamp
    return formatted_timestamp


def convert_to_discord_italic(text):
    return text.replace("<i=1>", "*").replace("<i=2>", "*").replace("<i=3>", "*").replace("</i>", "*")


def add_timestamp(message:str, ts:datetime) -> str:
    return f"{formatted_time(ts)}: {message}"


def get_recent_messages(entries, nr_entries):
    if not entries:
        return []

    entry = entries[0]
    reference_time = entry['published']

    nr_days = 0
    current_time = reference_time
    entry_message = convert_to_discord_italic(entry['message'])
    entry_message = add_timestamp(entry_message, reference_time)
    recent_messages = [entry_message]

    for entry in entries:
        entry_time = entry['published']
        entry_message = convert_to_discord_italic(entry['message'])
        entry_message = add_timestamp(entry_message, entry_time)

        if nr_days == nr_entries: return recent_messages

        if entry_message in recent_messages: continue

        if entry_time != current_time:
            current_time = entry_time
            nr_days += 1
        if nr_days < nr_entries:
            recent_messages.append(entry_message)

    return None


def delta_to_now(timestamp:datetime.datetime):
    tz = timezone.utc
    now_utc:str = str(datetime.datetime.now(tz))[:19]
    now = datetime.datetime.strptime(now_utc, "%Y-%m-%d %H:%M:%S")

    return timestamp - now


def days_hours_minutes(td: Union[datetime.timedelta, int]):
    if isinstance(td, datetime.timedelta):
        return td.days, (td.seconds // 3600) % 24, (td.seconds // 60) % 60
    else:
        return td // 86400, (td // 3600) % 24, (td // 60) % 60


def formatted_delta(td: Union[datetime.timedelta, int]) -> str:
    days, hours, minutes = map(int, days_hours_minutes(td))
    formatted_time = ""
    if days:
        formatted_time += f"{days}d "

    formatted_time += f"{hours}h {minutes}m"

    return formatted_time


def test():
    test_ts = "2024-07-06T12:18:26.27878Z"
    print(test_ts[:19])


if __name__ == "__main__":
    test()

