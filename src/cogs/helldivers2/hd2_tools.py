import datetime
from typing import Union
from datetime import timedelta


# Function to convert timestamp to datetime object
def convert_to_datetime(timestamp:Union[str, int, float]):
    if isinstance(timestamp, str):
        # Truncate the microseconds to six digits
        timestamp = timestamp[:26] + "Z"
        # Convert the timestamp to a datetime object
        return datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")
    elif isinstance(timestamp, int) or isinstance(timestamp, float):
        return datetime.datetime.fromtimestamp(timestamp)
    else:
        return None
        

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
    now = datetime.datetime.now()
    return timestamp - now


def no_microseconds(delta:Union[datetime.timedelta, str]) -> str:
    if isinstance(delta, datetime.timedelta) or isinstance(delta, str):
        return str(delta).split('.')[0]
    else:
        return None


def test():
    t_str = "2024-07-04 10:06:44: <i=3>CYBERSECURITY ALERT</i>"
    print(convert_to_discord_italic(t_str))
    
    text = "normal text without any html italic shit"
    print(convert_to_discord_italic(text))
    
    ts = 1720314451.016
    ts = int(ts)
    dt = convert_to_datetime(ts)
    print(dt)
    
    now = datetime.datetime.now()
    delta = dt - now
    print(str(delta)[:-7])
    print(now)
    print('XXX', no_microseconds(delta))


if __name__ == "__main__":
    test()

