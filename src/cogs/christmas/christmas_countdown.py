from datetime import datetime


class ChristmasCountdown:

    @staticmethod
    def calculate_days_remaining(day=24):
        current_date = datetime(datetime.today().year, datetime.today().month, datetime.today().day)
        christmas_date = datetime(current_date.year, 12, day)

        # Check if Christmas already passed this year, if yes, calculate for the next year
        if current_date > christmas_date:
            christmas_date = datetime(current_date.year + 1, 12, day)

        # Calculate the remaining days until Christmas
        remaining_time = christmas_date - current_date
        return remaining_time.days
    
    @staticmethod
    def next_christmas_year(day=24):
        current_date = datetime(datetime.today().year, datetime.today().month, datetime.today().day)
        christmas_date = datetime(current_date.year, 12, day)

        # If Christmas has already passed this year, return the next year
        if current_date > christmas_date:
            return current_date.year + 1
        else:
            return current_date.year


def test():
    days_remaining = ChristmasCountdown.calculate_days_remaining()

    print(days_remaining)


if __name__ == "__main__":
    test()
