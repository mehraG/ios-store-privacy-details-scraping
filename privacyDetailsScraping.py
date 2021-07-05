import requests
import pandas as pd


def get_individual_privacy_detail(privacy_details_list, privacy_detail_type="DATA_USED_TO_TRACK_YOU"):
  temp = set()
  global all_privacy_details_P1, all_privacy_details_P2, all_privacy_details_P3, \
      privacy_details_P1, privacy_details_P2, privacy_details_P3

  for privacy_details in privacy_details_list:
    if privacy_details["identifier"] == privacy_detail_type:
      if privacy_details["dataCategories"] != []:
        for privacy_category in privacy_details["dataCategories"]:
          temp.add(privacy_category["dataCategory"])
      elif privacy_details["purposes"] != []:
        for privacy_purposes in privacy_details["purposes"]:
          for privacy_category in privacy_purposes["dataCategories"]:
            temp.add(privacy_category["dataCategory"])
      break

  if privacy_detail_type == "DATA_USED_TO_TRACK_YOU":
    all_privacy_details_P1 = all_privacy_details_P1 | temp
    privacy_details_P1.append(temp)
  elif privacy_detail_type == "DATA_LINKED_TO_YOU":
    all_privacy_details_P2 = all_privacy_details_P2 | temp
    privacy_details_P2.append(temp)
  elif privacy_detail_type == "DATA_NOT_LINKED_TO_YOU":
    all_privacy_details_P3 = all_privacy_details_P3 | temp
    privacy_details_P3.append(temp)


def get_privacy_details(app_id="719208154"):
  url = f"https://amp-api.apps.apple.com/v1/catalog/US/apps/{app_id}"
  headers = {
      "Authorization": "Bearer eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlU4UlRZVjVaRFMifQ.eyJpc3MiOiI3TktaMlZQNDhaIiwiaWF0IjoxNjI0NTczNzkwLCJleHAiOjE2MzE4MzEzOTB9.sVEHmkKzBWt5qmz1rcRu5LSMOgoZs4G_G_ymlI9HRsI07--4HK9N2UfE0nxshwa2wNxAK_JtiSgs7HzYW7RgZw",
      "Content-type": "application/json"
  }
  params = {
      'platform': 'web',
      'fields': 'privacyDetails',
      'l': 'en-gb',
  }
  r = requests.get(url, headers=headers, params=params)

  if r.status_code == 200:
    return r.json()['data'][0]['attributes']['privacyDetails']['privacyTypes']


def create_csv():
  global app_details
  data = []

  for i in range(len(app_details)):
    row_data = dict()
    row_data['name'] = app_details[i][0]
    for privacy_name in all_privacy_details_P1:
      row_data[f'P1 {privacy_name}'] = 1 if privacy_name in privacy_details_P1[i] else 0
    for privacy_name in all_privacy_details_P2:
      row_data[f'P2 {privacy_name}'] = 1 if privacy_name in privacy_details_P2[i] else 0
    for privacy_name in all_privacy_details_P3:
      row_data[f'P3 {privacy_name}'] = 1 if privacy_name in privacy_details_P3[i] else 0
    data.append(row_data)

  df = pd.DataFrame(data)

  # Reordering columns such that "Name" column in 1st column
  cols = df.columns.tolist()
  cols = cols[-1:] + cols[:-1]
  df = df[cols]

  df.to_csv('privacy_details.csv', index=False)


if __name__ == '__main__':
  '''
  P1 is DATA_USED_TO_TRACK_YOU 
  P2 is DATA_LINKED_TO_YOU 
  P3 is DATA_NOT_LINKED_TO_YOU 
  '''
  all_privacy_details_P1 = set()
  all_privacy_details_P2 = set()
  all_privacy_details_P3 = set()
  privacy_details_P1 = []
  privacy_details_P2 = []
  privacy_details_P3 = []

  app_details = [
      # Each tuple contains app name & app id
      ("PUBG MOBILE - Traverse", 1330123889),
      ("Signal - Private Messenger", 874139669),
      ("Steps – Step Counter, Activity", 719208154),
      ("Facebook", 284882215),
      ("WhatsApp Messenger", 310633997),
  ]

  for app_detail in app_details:
    temp_details = get_privacy_details(app_detail[1])
    get_individual_privacy_detail(temp_details, "DATA_USED_TO_TRACK_YOU")
    get_individual_privacy_detail(temp_details, "DATA_LINKED_TO_YOU")
    get_individual_privacy_detail(temp_details, "DATA_NOT_LINKED_TO_YOU")
    print(f'{app_detail[0]} privacy details fetched...')
  print('All apps privacy details fetched!')

  create_csv()
  print('CSV file created!')
