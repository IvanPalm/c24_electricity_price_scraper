url_api = ['https://vergleich.check24.de/common/ajax/tariff_detail?&calculationparameterId=2fc32fbf4ea74b9693cd1d7da2a0246a&tariffversionId=937662&tariffversionVariationKey=b-325169-b-875682-b-875683-b-875684&productId=1&c24_reference_tariff=no',
'https://vergleich.check24.de/common/ajax/tariff_detail?&calculationparameterId=2fc32fbf4ea74b9693cd1d7da2a0246a&tariffversionId=936037&tariffversionVariationKey=b-874223-b-874224-b-874225&productId=1&c24_reference_tariff=no']

import requests
from requests.exceptions import HTTPError
from scrapy import Selector
import pandas as pd

df = pd.DataFrame(columns = range(0, 13))
colnames = []
values = []

for url in url_api:
    try:
        # resp = requests.get(url + url_par)
        resp = requests.get(url)

        # If the response was successful, no Exception will be raised
        resp.raise_for_status()
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        print('Success!')

    resp.encoding = 'utf-8'
    html = resp.content
    sel = Selector(text=html)
    col = sel.xpath('.//div[contains(@class, "fact__label")]')
    df.columns = ['Anbieter']+[str.strip().rstrip().replace('\\n', '') for str in col.xpath('./text()').extract()]
    prov = sel.xpath('.//div[contains(@class, "ajax-provider")]')
    provider = prov.xpath('.//text()').extract()[1].strip().rstrip().replace('\\n', '')
    val = sel.xpath('.//div[contains(@class, "fact__value")]')
    values = [str.strip().rstrip().replace('\\n', '') for str in val.xpath('./text()').extract()]
    new_row = [provider] + values
    df.loc[len(df) + 1, :] = new_row

df
