import requests
import os
from dotenv import load_dotenv


sms_username = os.environ.get('sms_username')
sms_password = os.environ.get('sms_password')




class Sms():

    def __init__(self):
        self.url = f'https://portal.nigeriabulksms.com/api/?username={sms_username}&password={sms_password}&action=balance'

    def balance_getter(self):
        balance = int(requests.get(url=self.url).json()['balance'])
        return balance

    def sms_sender(self, sender , phone_numbers, message):
        url = f'https://portal.nigeriabulksms.com/api/?username={sms_username}&password={sms_password}&message={message}&' \
              f'sender={sender}&mobiles={phone_numbers}'
        send_sms = requests.post(url)
        return send_sms

    def numbers_counter(self, phone_numbers):
        splitter = phone_numbers.split(',')
        return len(splitter)


    def delivery_report(self,phone_numbers):
        report = requests.get(f'https://portal.nigeriabulksms.com/api/?username={sms_username}&password={sms_password}'
                            f'&action=reports').json()[:self.numbers_counter(phone_numbers)]
        report_dict = {'status': [], }
        for i in report:
            report_dict['status'].append(i.get('status'))

        return report_dict

