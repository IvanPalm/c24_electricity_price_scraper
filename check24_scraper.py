url = 'https://vergleich.check24.de/common/ajax/tariff_detail?&calculationparameterId=1845c5f5f696a77e002894ca988b51ef&tariffversionId=936998&tariffversionVariationKey=b-325169-b-875205-b-875206-b-875207&productId=1&c24_reference_tariff=no'
#url2 = 'https://vergleich.check24.de/common/ajax/tariff_detail?&calculationparameterId=1845c5f5f696a77e002894ca988b51ef&tariffversionId=936037&tariffversionVariationKey=b-874223-b-874224-b-874225&productId=1&c24_reference_tariff=no'

import requests
from requests.exceptions import HTTPError

for url in [url]:
    try:
        resp = requests.get(url)

        # If the response was successful, no Exception will be raised
        resp.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        print('Success!')

# resp.encoding
# resp.text
# resp.headers

from bs4 import BeautifulSoup

soup = BeautifulSoup(resp.text, 'html.parser')
soup.find_all(class_ = "flex__item--8")
