# Scrape Check24 to extract pricing of electricity from any provider available for Berlin Mitte
# Modules required:
# selenium (with geckodriver)
# time
# scrapy
# pandas

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

driver = webdriver.Firefox('/usr/local/bin/')

### Function PageStatus
def PageStatus(driver, id, timeout=5): # timeout expressed in seconds

    try:
        element_present = EC.presence_of_element_located((By.ID, id))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print("Timed out waiting for page to load")
    finally:
        print("Page loaded") # ensure that the page loads regularly

root = 'https://www.check24.de/strom-gas/'
postcode = '10969'
consumption = '7000'

driver.get(root)
driver.maximize_window()

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
import time
time.sleep(5)
driver.find_element_by_class_name('c24-cookie-button').click()

from selenium.webdriver.common.action_chains import ActionChains

ActionChains(driver).move_to_element(driver.find_element_by_class_name('filter-setting__image--list'))
driver.find_element_by_class_name('filter-setting__image--list').click()
PageStatus(driver, id='paginator__button')

# click repeatedly on the pagination button to load the rest of the contents
try:
    while EC.presence_of_element_located((By.CLASS_NAME, 'paginator__button')):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        driver.find_element_by_class_name('paginator__button').click()
        #time.sleep(3) # wait before checking page # BAD MOVE...but it serves the function for now!
        PageStatus(driver, id='paginator__button')
except:
    print('All providers loaded!')

elements = driver.find_elements_by_class_name("tariff-tabbar__tab--first")
type(elements)
len(elements)

print(f'Clicking all {len(elements)} links is gonna take a while, go grab a nice coffee!')
driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") # scroll to end of page
target = 'https://vergleich.check24.de/common/ajax/tariff_detail?'
net_names = list()
for e in reversed(elements): # then click elements in reverse order - trick to prevent pop-ups which could block the clicking
    ActionChains(driver).move_to_element(e)
    e.click()

tarif_tabs = driver.find_elements_by_class_name("ajax-tabs")
type(tarif_tabs)
len(tarif_tabs)

from scrapy import Selector
import pandas as pd

#t = tarif_tabs[3]

df_list = list()
values = []
for t in tarif_tabs:
    html = t.get_attribute('innerHTML')
    sel = Selector(text=html)
    col = sel.xpath('.//div[contains(@class, "fact__label")]')
    if col != []:
        df = pd.DataFrame(columns = ['Anbieter']+[str.strip().rstrip().replace('\\n', '') for str in col.xpath('./text()').extract()])
        prov = sel.xpath('.//div[contains(@class, "ajax-provider")]')
        provider = prov.xpath('.//text()').extract()[1].strip().rstrip().replace('\\n', '')
        val = sel.xpath('.//div[contains(@class, "fact__value")]')
        values = [str.strip().rstrip().replace('\\n', '') for str in val.xpath('./text()').extract()]
        new_row = [provider] + values
        df.loc[len(df) + 1, :] = new_row
        df_list.append(df)
    else:
        continue
len(df_list)

for i in range(len(df_list)):
    print(i) ; print(df_list[i].columns.duplicated())

df_list[107] = df_list[107].loc[:, ~df_list[107].columns.duplicated()]
df_list[107].columns.duplicated()

final = pd.concat(df_list, sort=False)
final.shape
final = final.fillna('NA')
final.to_csv('electricity_prices_check24.csv', index=False)
