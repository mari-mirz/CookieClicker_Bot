from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

chrome_driver_path = "/Users/marianamirzoyan/Desktop/Development/chromedriver"

service = Service(chrome_driver_path)
driver = webdriver.Chrome(service=service)
driver.get(url="http://orteil.dashnet.org/experiments/cookie/")


def get_store():
    # putting store items into lists
    store = driver.find_elements(By.CSS_SELECTOR, "#store b")
    item_list = []
    for element in store:
        full_item = element.text
        item = full_item.replace(",", "").replace(" ", "").split("-")
        item_list.append(item)

    del item_list[8]

    # splitting lists
    items = []
    costs = []

    for n in range(len(item_list)):
        row = item_list[n]
        items.append(row[0])
        costs.append(row[1])

    # combining lists into dictionary
    item_dict = {}

    for key in items:
        for value in costs:
            item_dict[key] = int(value)
            costs.remove(value)
            break

    return item_dict


# buy item of highest value
def purchase(wallet, dictionary):
    affordable_items = {}
    for element in dictionary:
        if wallet > dictionary[element]:
            affordable_items[element] = dictionary[element]

    purchasable_item = max(affordable_items)
    print(purchasable_item)
    item = driver.find_element(By.ID, f"buy{purchasable_item}")
    item.click() 


# start timer (5 seconds)
cookie = driver.find_element(By.CSS_SELECTOR, "#cookie")

timeout = time.time() + 5

while True:
    money = ((driver.find_element(By.ID, "money")).text)
    if "," in money:
        money = money.replace(",", "")
    cookie.click()

    if time.time() > timeout:
        store_dict = get_store()
        purchase(int(money), store_dict)
        timeout = time.time() + 5
