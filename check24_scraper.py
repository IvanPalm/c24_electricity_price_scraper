
root = 'https://www.check24.de/strom-gas/'
postcode = '10969'
consumption = '7000 KWh'

from selenium import webdriver

driver = webdriver.Firefox('/usr/local/bin/')

### Function PageStatus
def PageStatus(driver, id, timeout=2): # timeout expressed in seconds
    from selenium.common.exceptions import TimeoutException
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By

    try:
        element_present = EC.presence_of_element_located((By.ID, id))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")
    finally:
        print("Page loaded") # ensure that the page loads regularly

driver.get(root)

# fill in field for postcode
in_postcode = driver.find_element_by_id('c24api_zipcode')
in_postcode.clear()
in_postcode.send_keys(postcode)
# fill in field for total consumption
in_totcons =  driver.find_element_by_id('c24api_totalconsumption')
in_totcons.clear()
in_totcons.send_keys(consumption)

# hit the button Vergleich and check page loading
driver.find_element_by_id('c24_calculate').click()
PageStatus(driver, id='c24-cookie-button')

# click on 'OK-Cookies' and then 'Alle tariffen' to remove filters
try:
    driver.find_element_by_class_name('c24-cookie-button').click()
except:
    driver.find_element_by_class_name('filter-setting__image--list').click()
finally:
    driver.find_element_by_class_name('filter-setting__image--list').click()
PageStatus(driver, id='paginator__button')

# click repeatedly on the button to load the rest of the contents
import time
# for i in range(0, 21):
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     driver.find_element_by_class_name('paginator__button').click()
#     time.sleep(5) # wait before checking page # BAD MOVE...but it serves the function for now!
#     PageStatus(driver, id='paginator__button')
try:
    while EC.presence_of_element_located((By.CLASS_NAME, 'paginator__button')):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.find_element_by_class_name('paginator__button').click()
        time.sleep(5) # wait before checking page # BAD MOVE...but it serves the function for now!
        PageStatus(driver, id='paginator__button')
except:
    print('All providers loaded!')

elements = driver.find_elements_by_class_name("tariff-tabbar__tab--first")

# Gets network information, including network calls
def GetNetworkResources(driver):
    Resources = driver.execute_script("return window.performance.getEntries();")
    for resource in Resources:
        print(resource['name'])
    return Resources

print(f'Clicking all {len(elements)} links is gonna take a while, go grab a nice coffee!')
for e in elements:
    e.click()

GetNetworkResources(driver)
type(net_data)










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
