
from datetime import datetime
from lib.admin_tools import load as fload
from lib.admin_tools import save as fsave
from lib.calendar import Calendar


class BirthdayReminder():

    def __init__(self, bday_reminder_file):
        self.bday_reminder_file = bday_reminder_file
        self.birthdays = fload(self.bday_reminder_file) or {}
        print('Birthdays:', self.birthdays)

    def add_birthday(self, guild, user, year, month, day, show=False):
        if Calendar.is_valid(int(day), int(month), int(year)):
            if guild not in self.birthdays:
                self.birthdays[guild] = {}

            # year = year if not show else None
            bday_obj = {'day': f'{month}-{day}',
                        'year': year if show else None,
                        'show': show}

            self.birthdays[guild][user] = bday_obj

    def remove_birthday(self, guild, user):
        try:
            del self.birthdays[guild][user]
        except Exception as e:
            print(e)

    def check_day(self, guild_id, year:int=None, month:int=None, day:int=None):
        cyear = year or datetime.today().year
        cmonth = month or datetime.today().month
        cday = day or datetime.today().month

        cdate = f'{cmonth}-{cday}'

        birthdays_today = []

        if cdate == '3-1' and not Calendar.is_leap_year(cyear):
            birthdays_today = self.check_day(guild_id, cyear, 2, 29)

        for user, date in self.birthdays[guild_id].items():

            if date['day'] == cdate:
                birthdays_today.append((user, date))

        return birthdays_today

    def birthdays_in_system(self):
        total = sum(1 for g in self.birthdays.values() for d in g.values() if d)
        return total

    def __repr__(self):
        return f"{self.birthdays_in_system()} in system"

    def save(self):
        fsave(self.bday_reminder_file, self.birthdays)

    def load(self):
        self.birthdays = fload(self.bday_reminder_file)


def test():
    br = BirthdayReminder('test')
    br.add_birthday('000', 'Test1' , 2004, 2, 29, False)
    br.add_birthday('000', 'Test2' , 2005, 2, 29, False)  # invalid date
    br.add_birthday('000', 'Test3' , 2023, 3, 1, False)
    br.add_birthday('000', 'Test4' , 2023, 12, 31, False)
    br.add_birthday('001', 'Test5' , 2023, 12, 31, False)

    br.add_birthday('000', 'Test23', 2024, 1, 1, False)
    br.add_birthday('000', 'Test24', 2024, 1, 1, False)
    br.add_birthday('001', 'Test25', 2024, 1, 1, False)

    print(br.birthdays)
    print(Calendar.is_leap_year(2000))
    print()

    print('G 000: check 3-1:', br.check_day('000', year=2023, month=3, day=1))
    print('G 000: check 2-29:', br.check_day('000', year=2024, month=2, day=29))
    print('G 000: check 3-1:', br.check_day('000', year=2024, month=3, day=1))

    # print(br.check_day('01-01'))
    print(br)
    br.remove_birthday('000', 'Test1')
    br.remove_birthday('000', 'Test1')
    print(br)
    # print(br.check_day('01-01'))


if __name__ == "__main__":
    test()
