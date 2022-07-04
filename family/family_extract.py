import pandas as pd
from datetime import datetime

class Extract:

    def age(self, new):
        this_year = datetime.today().year
        age = this_year - new.year
        return age

    def title_adder(self, new):
        new['date_of_birth'] = pd.to_datetime(new['date_of_birth'], infer_datetime_format=True)
        # new["gender"] = new["gender"]
        # new["marital_status"] = new["marital_status"]
        if new.gender.lower() == 'male' and self.age(new.date_of_birth) >= 70:
            return 'Pa'
        elif new.gender.lower() == 'female' and self.age(new.date_of_birth) >= 70:
            return 'Ma'
        elif new.gender.lower() == 'female' and self.age(new.date_of_birth) >= 40 and new.marital_status == 'single':
            return 'Ms'
        elif new.gender.lower() == 'male' and self.age(new.date_of_birth) >= 40 and new.marital_status == 'single':
            return 'Mr'
        elif new.gender.lower() == 'female' and new.marital_status == 'married':
            return 'Mrs'
        elif new.gender.lower() == 'female' and new.marital_status == 'single':
            return 'Miss'
        elif new.gender.lower() == 'male' and new.marital_status == 'married':
            return 'Mr'
        elif new.gender.lower() == 'male' and new.marital_status == 'single':
            return 'Bro'

        else:
            pass
