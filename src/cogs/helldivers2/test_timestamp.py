import datetime
from cogs.helldivers2.hd2_tools import formatted_time, convert_to_datetime


def main():
    # Define the timestamp
    timestamp = convert_to_datetime("2024-03-10T16:32:39.6810471Z")
    
    print(formatted_time(timestamp))

    # Define two timestamps
    timestamp1 = "2024-07-03T11:05:13.5708687Z"
    timestamp2 = "2024-07-01T09:30:45.1234567Z"
    
    # Convert both timestamps to datetime objects
    timestamp_dt1 = convert_to_datetime(timestamp1)
    timestamp_dt2 = convert_to_datetime(timestamp2)
    
    # Compare the timestamps
    if timestamp_dt1 < timestamp_dt2:
        print(f"{timestamp1} is older than {timestamp2}")
    elif timestamp_dt1 > timestamp_dt2:
        print(f"{timestamp2} is older than {timestamp1}")
    else:
        print(f"{timestamp1} and {timestamp2} are the same")
        
    print(int(timestamp_dt1.timestamp()))
    
    
if __name__ == "__main__":
    main()
