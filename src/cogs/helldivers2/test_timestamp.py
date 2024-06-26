import datetime

# Define the timestamp
timestamp = "2024-07-03T11:05:13.5708687Z"

# Truncate the microseconds to six digits
timestamp = timestamp[:26] + "Z"

# Convert the timestamp to a datetime object
timestamp_dt = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%fZ")

# Get the current date and time
now = datetime.datetime.now()

# Calculate the time difference in seconds
time_difference = (timestamp_dt - now).total_seconds()

# Print the time difference
print(f"The time difference between {timestamp} and now is {time_difference} seconds.")
