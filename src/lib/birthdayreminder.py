
from datetime import datetime
from lib.admin_tools import load as fload
from lib.admin_tools import save as fsave


class BirthdayReminder():

    def __init__(self, bday_reminder_file):
        self.bday_reminder_file = bday_reminder_file
        self.birthdays = fload(self.bday_reminder_file) or {}
        print('Birthdays:', self.birthdays)

    def add_birthday(self, guild, user, year, month, day, show=False):

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

    def check_day(self, cdate=None):
        current_date = datetime.now().strftime("%m-%d")

        cdate = cdate or current_date

        birthdays_today = []

        for gid, guild in self.birthdays.items():

            for user, date in guild.items():

                if date['day'] == cdate:
                    birthdays_today.append((gid, user))

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
    br.add_birthday('000', 'Test1' , '2023', '02', '01', False)
    br.add_birthday('000', 'Test2' , '2023', '02', '01', False)
    br.add_birthday('000', 'Test3' , '2023', '02', '01', False)
    br.add_birthday('000', 'Test4' , '2023', '12', '31', False)
    br.add_birthday('001', 'Test5' , '2023', '12', '31', False)

    br.add_birthday('000', 'Test23', '2024', '01', '01', False)
    br.add_birthday('000', 'Test24', '2024', '01', '01', False)
    br.add_birthday('001', 'Test25', '2024', '01', '01', False)

    print(br.birthdays)
    print()
    print()

    print('check:', br.check_day('02-01'))

    print(br.check_day('01-01'))
    print(br)
    br.remove_birthday('000', 'Test1')
    br.remove_birthday('000', 'Test1')
    print(br)
    print(br.check_day('01-01'))


if __name__ == "__main__":
    test()
