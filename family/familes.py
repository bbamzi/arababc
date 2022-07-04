import pandas as pd
from datetime import datetime


class Families:

    def age(self, new):
        # date_to_datetime = pd.to_datetime(new, infer_datetime_format=True)
        this_year = datetime.today().year
        age = this_year - pd.to_datetime(new, infer_datetime_format=True).year
        return age

    def title_adder(self, gender, date_of_birth, marital_status):

        # new["gender"] = new["gender"]
        # new["marital_status"] = new["marital_status"]
        if gender.lower() == 'male' and self.age(date_of_birth) >= 70:
            return 'Pa'
        elif gender.lower() == 'female' and self.age(date_of_birth) >= 70:
            return 'Ma'
        elif gender.lower() == 'female' and self.age(date_of_birth) >= 40 and marital_status == 'single':
            return 'Ms'
        elif gender.lower() == 'male' and self.age(date_of_birth) >= 40 and marital_status == 'single':
            return 'Mr'
        elif gender.lower() == 'female' and marital_status == 'married':
            return 'Mrs'
        elif gender.lower() == 'female' and marital_status == 'single':
            return 'Miss'
        elif gender.lower() == 'male' and marital_status == 'married':
            return 'Mr'
        elif gender.lower() == 'male' and marital_status == 'single':
            return 'Bro'

        else:
            pass

    def family_checker(self, marital_status, date_of_birth, gender):
        age = self.age(date_of_birth)
        if (age >= 40) & (marital_status == 'single') | (gender == 'male') & (marital_status == 'married') | \
                (marital_status == 'widowed') & (gender == 'female'):
            return True
        else:
            return False

    def extract(self, first_name, surname, marital_status,
                gender, date_of_birth, phone_number, email,
                residential_address, Neigborhood, lga, state, coordinates, google_suggested_address):
        output = {}
        title = self.title_adder(gender, date_of_birth, marital_status)
        output['family_name'] = title + " " + first_name + " " + surname
        output['phone_number'] = phone_number
        output['email'] = email
        output['residential_address'] = residential_address
        output['google_suggested_address'] = residential_address
        output['Neigborhood'] = Neigborhood
        output['lga'] = lga
        output['state'] = state
        output['coordinates'] = coordinates
        return output
