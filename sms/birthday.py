import datetime
from datetime import datetime
import random
from sms.messges import messages

from family.familes import Families
from sms import Sms




def month_day(new):
    current_month = new.month
    day = new.day
    month_and_day = (current_month, day)
    return month_and_day

def month(new):
    current_month = new.month

    return current_month

class Birthday(Families):
    def __init__(self):
        super().__init__()
        # self.df['wed_month_and_day'] = self.df['wedding_date'].apply(wed_month_day)
        self.df['month_and_day'] = self.df['date_of_birth'].apply(month_day)
        self.df['month'] = self.df['date_of_birth'].apply(month)

    def month_birthday(self):
        today = datetime.datetime.today().date()
        month = today.month
        day = today.day
        celebrant_number = self.df[self.df.month == month].phone_number
        return celebrant_number

    def today_birthday(self):
        lst = []
        celebrants_info = {}
        today = datetime.datetime.today().date()
        # today = datetime.datetime(2020, 1, 23)
        month = today.month
        day = today.day
        celebrant_number = self.df[self.df.month_and_day == (month, day)].phone_number
        celebrant_name = self.df[self.df.month_and_day == (month, day)].first_name
        celebrant_title = self.df[self.df.month_and_day == (month, day)].title
        name = celebrant_title + " "+ celebrant_name.str.title()
        new = zip(name,celebrant_number)
        return list(new)




    def b_day_checker(self):
        if len(self.today_birthday()) > 0:
            return True
        else:
            return False

    def message_picker(self,member):
        message_picked = random.choice(list(messages['msg']))
        hash_replace = message_picked.replace('###',member)
        return hash_replace

    def messaging(self):
        lst = []
        sms = Sms()
        sender_name = 'Araba B.C'
        for i in self.today_birthday():
            phone_numbers = i[1]
            name = i[0]

            message = self.message_picker(name)
            sms.sms_sender(sender=sender_name, phone_numbers=phone_numbers, message=message)





