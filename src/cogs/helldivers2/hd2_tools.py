import datetime
from typing import Union
from datetime import timedelta, timezone


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
    tz = timezone.utc
    now_utc:str = str(datetime.datetime.now(tz))[:19]
    now = datetime.datetime.strptime(now_utc, "%Y-%m-%d %H:%M:%S")
    
    return timestamp - now


def days_hours_minutes(td):
    return td.days, td.seconds // 3600, (td.seconds // 60) % 60
   
        
def formatted_delta(dt:datetime.timedelta) -> str:
    days, hours, minutes = days_hours_minutes(dt)
    formatted_time = ""
    if days:
        formatted_time += f"{days}d "
    
    formatted_time += f"{hours}h {minutes}m"    
    
    return formatted_time


def test():
    pass


if __name__ == "__main__":
    test()

