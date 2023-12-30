
from datetime import datetime


class Calendar:

    @staticmethod
    def calculate_time_distance(start:datetime, stop:datetime) -> int:
        """
        Calculate the time difference in seconds between two datetime objects or string representations.

        Parameters:
        - start (datetime or str): The starting datetime or its string representation.
        - stop (datetime or str): The ending datetime or its string representation.

        Returns:
        - int: The time difference in seconds.
        """
        if isinstance(start, str):
            start = datetime.fromisoformat(start)
        elif not isinstance(start, datetime):
            raise ValueError("Invalid type for start. It should be either datetime or str.")

        if isinstance(stop, str):
            stop = datetime.fromisoformat(stop)
        elif not isinstance(stop, datetime):
            raise ValueError("Invalid type for stop. It should be either datetime or str.")

        time_delta = stop - start
        return time_delta.days  # + time_delta.seconds / (24 * 3600)

    @staticmethod
    def is_leap_year(year:int) -> bool:
        """Return True for leap years, False for non-leap years."""
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def test():
    start_time = datetime(2023, 12, 24)
    # end_time = "2023-01-01T14:30:00"
    end_time = "2024-12-24"
    time_difference = Calendar.calculate_time_distance(start_time, end_time)

    print(f"Time difference: {time_difference} days")

    leap_year_1900 = Calendar.is_leap_year(1900)
    leap_year_2000 = Calendar.is_leap_year(2000)
    leap_year_2023 = Calendar.is_leap_year(2023)
    leap_year_2024 = Calendar.is_leap_year(2024)

    print(f"Leap year: 1600 ({leap_year_1900})")
    print(f"Leap year: 2000 ({leap_year_2000})")
    print(f"Leap year: 2023 ({leap_year_2023})")
    print(f"Leap year: 2024 ({leap_year_2024})")


if __name__ == "__main__":
    test()
