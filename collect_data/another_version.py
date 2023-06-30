import selenium.webdriver.remote.webelement
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


chrome_options = Options()
chrome_options.add_argument("--no-sandbox")

webdriver_service = Service("chromedriver/chromedriver") ## path to where you saved chromedriver binary
browser = webdriver.Chrome(service=webdriver_service, options=chrome_options)


driver = webdriver.Chrome("chromedriver.exe")

driver.get("https://www.reddit.com/r/AskReddit/comments/105mamm/what_are_some_incorrect_grammatical_habits_that/")


elems = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@data-testid='post-comment-header']/parent::div")))

counter = 0
for e in elems[:5]:
    print(e.screenshot(f"{counter}.png"))
    print('______________')
    counter += 1
