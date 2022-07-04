import requests
import json
import urllib
# from family.familes import Families
#



# class google_address():
#     def __init__(self):
#         self.df = fams
#         self.df["Address"] = fams['residential_address'].apply(self.google_address_getter)
#         self.df["Neighbourhood"] = fams['residential_address'].apply(self.google_neigbourhood_getter)
#         self.df["LGA"] = fams['residential_address'].apply(self.google_lga_getter)
#         self.df["State"] = fams['residential_address'].apply(self.google_state_getter)
#         self.df["Coordinates"] = fams['residential_address'].apply(self.google_lat_lng_getter)
#
#
#
#
#
#     def address_formatter(self,address):
#         try:
#             req = requests.get(f'{base_url}{urllib.parse.urlencode({"address": address, "key": AUTH_KEY})}')
#             data = json.loads(req.content)
#             google_formatted_address = data['results'][0]['formatted_address']
#             state = data['results'][0]['address_components'][3]['long_name']
#             lat_and_long = data["results"][0]["geometry"]["location"]
#             LGA = data['results'][0]['address_components'][4]['long_name']
#             return data
#
#
#         except (NameError, TypeError, IndexError) as error:
#
#             return 'invalid'
#
#
#
#     def google_address_getter(self,address):
#         try:
#             return self.address_formatter(address)['results'][0]['formatted_address']
#         except (NameError, TypeError, IndexError) as error:
#             return 'invalid'
#
#
#
#     def google_lga_getter(self,address):
#         try:
#             return self.address_formatter(address)['results'][0]['address_components'][4]['long_name']
#         except (NameError, TypeError, IndexError) as error:
#             return 'invalid'
#
#     def google_neigbourhood_getter(self,address):
#         try:
#             return self.address_formatter(address)['results'][0]['address_components'][2]['long_name']
#         except (NameError, TypeError, IndexError) as error:
#             return 'invalid'
#
#     def google_state_getter(self,address):
#         try:
#             return self.address_formatter(address)['results'][0]['address_components'][3]['long_name']
#         except (NameError, TypeError, IndexError) as error:
#             return 'invalid'
#
#     def google_lat_lng_getter(self,address):
#         try:
#             new = self.address_formatter(address)['results'][0]['geometry']['location']
#             return [float(i) for i in new.values()]
#         except (NameError, TypeError, IndexError) as error:
#             return 'invalid'



# print(google_address().address_formatter())
# google_address().df.to_csv('familydata2.csv')
# print(google_address().address_formatter("37 abati george St, Lagos"))
# google_address().df.to_csv('news.csv')

