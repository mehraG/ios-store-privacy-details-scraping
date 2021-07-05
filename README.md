# ios-store-privacy-details-scraping
Scraping privacy details of ios apps and storing it in a csv file.

It uses an ```https://amp-api.apps.apple.com``` api to fetch privacy details. And a bearer token is hardcoded. That bearer token will expire around Nov, 2021. So, please update the bearer token in the code if you are planning to use this after Nov, 2021. 

## Usage
Add app name and app id of the ios app you wish to fetch privacy details for, to 👇 **this list** inside the code.

```python
app_details = [
 # Each tuple contains app name & app id
 ("PUBG MOBILE - Traverse", 1330123889),
 ("Signal - Private Messenger", 874139669),
 ("Steps – Step Counter, Activity", 719208154),
 ("Facebook", 284882215),
 ("WhatsApp Messenger", 310633997),
]
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
