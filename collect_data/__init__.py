import selenium.common
from selenium import webdriver
from selenium.webdriver.common.by import By

import console_api
from config import SHOTS_DIR, WEBDRIVER_PATH, WEBDRIVER_TYPE, TESSERACT_DIR
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from selenium.webdriver.remote.webelement import WebElement
from tts import say_save


def contains_element(list1, list2):
    return any(elem in list2 for elem in list1)

removed = []

def parse_text(text: str):
    import re
    if "edited" in text:
        txt = "\n".join(text.split("\n")[3:-6])
    else:
        txt = "\n".join(text.split("\n")[4:-6])

    if "ago" in txt:
        sp = txt.split("ago")
        sp.pop(0)
        txt = "\n".join(sp)

    return txt

    # return find_all_between_tags(text.strip().split("\n"), body_start, body_end)


def get_threadshot_by_url(url: str, id: str):
    global removed

    if WEBDRIVER_TYPE == "chrome":
        driver = webdriver.Chrome(WEBDRIVER_PATH)
    elif WEBDRIVER_TYPE == "firefox":
        driver = webdriver.Firefox(WEBDRIVER_PATH)
    elif WEBDRIVER_PATH == "edge":
        driver = webdriver.Edge(WEBDRIVER_PATH)

    driver.get(url)

    driver.find_element(By.XPATH,
                        '//*[@id="SHORTCUT_FOCUSABLE_DIV"]/div[3]/div/section/div/section[2]/section[2]/form/button'
                        ).click()

    try:
        driver.find_element(By.XPATH, f'//*[@id="t3_{id}"]').screenshot(f"{SHOTS_DIR}/{id}/thread.png")
    except Exception as e:
        pass

    console_api.print_msg("Done!", "red")


# https://www.reddit.com/r/AskReddit/comments/104ydw2/what_is_causing_the_recent_trend_of_using_quotes/
def get_mugshot_by_url(url: str, amount: int, id: str):
    global removed
    amount += 1

    if WEBDRIVER_TYPE == "chrome":
        driver = webdriver.Chrome(WEBDRIVER_PATH)
    elif WEBDRIVER_TYPE == "firefox":
        driver = webdriver.Firefox(WEBDRIVER_PATH)
    elif WEBDRIVER_PATH == "edge":
        driver = webdriver.Edge(WEBDRIVER_PATH)

    driver.get(url)

    driver.find_element(By.XPATH,
                        '//*[@id="SHORTCUT_FOCUSABLE_DIV"]/div[3]/div/section/div/section[2]/section[2]/form/button'
                        ).click()

    try:
        driver.find_element(By.XPATH, f'//*[@id="t3_{id}"]').screenshot(f"{SHOTS_DIR}/{id}/thread_mini.png")
    except Exception as e:
        pass

    driver.save_screenshot(f"{SHOTS_DIR}/{id}/thread.png")

    try:
        driver.find_element(By.XPATH, f'//*[@id="t3_{id}"]').screenshot(f"{SHOTS_DIR}/{id}/thread_mini.png")
    except Exception as e:
        pass

    try:
        driver.find_elements(By.XPATH, '//*[@id="SHORTCUT_FOCUSABLE_DIV"]/div[2]/div[2]/div/button')[0].click()
    except Exception as e:
        pass

    elems = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located(
            (By.XPATH, "//div[@data-testid='post-comment-header']/parent::div/parent::div")))

    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    import time
    time.sleep(5)
    driver.execute_script("window.scrollTo(0,0)")
    time.sleep(2)
    counter = 0
    for e in elems[:amount]:
        try:
            e: WebElement = e
            e.screenshot(f"{SHOTS_DIR}/{id}/{counter + 1}.png")
            time.sleep(1)
            import pytesseract
            from PIL import Image
            pytesseract.pytesseract.tesseract_cmd = TESSERACT_DIR

            image = Image.open(f"{SHOTS_DIR}/{id}/{counter + 1}.png")

            text: str = pytesseract.image_to_string(image)
            # print(text.lower().strip().split() in ("reply", "share", "report", "save", "follow"))
            fails = 0
            if contains_element(["reply", "share", "report", "save", "follow"], text.lower().strip().split()):
                # print("Created!")
                console_api.print_msg("[green]Image created![/green]")
                console_api.print_msg("[yellow]_______________[/yellow]")
                # print(e.text)
                # print(e.text.strip())
                txt = parse_text(e.text.strip())
                nicexd = txt.strip().replace("\n", "").replace("Vote", ""). \
                    replace("Reply", ""). \
                    replace("Share", ""). \
                    replace("Report", ""). \
                    replace("Save", ""). \
                    replace("Follow", "")
                console_api.print_msg(f"[red]Saying[/red] : [green]{nicexd}[/green]")
                say_save(nicexd,
                         f"{counter}",
                         id)

                # //*[@id="t1_j3o776f"]/div[2]/div[3]/div[2]/div
                counter += 1
            else:
                try:
                    os.remove(f"{SHOTS_DIR}/{id}/{counter + 1}.png")
                except FileNotFoundError:
                    console_api.print_msg("The file does note exits so it cannot be deleted.", style="red")

                console_api.print_msg("Screenshot cannot be created because of not being a proper a mugshot.",
                                      style="red")
                console_api.print_msg("[yellow]_______________[/yellow]")
                removed.append(f"{SHOTS_DIR}/{id}/{counter + 1}.png")
                fails += 1
            if fails > amount - 1:
                console_api.print_msg("Cannot proceed.", style="red")
                exit()
        except selenium.common.WebDriverException as e:
            try:
                os.remove(f"{SHOTS_DIR}/{id}/{counter + 1}.png")
            except FileNotFoundError:
                console_api.print_msg("The file does note exits so it cannot be deleted.", style="red")
            console_api.print_msg(f"Screenshot cannot be created because of \n{e}.", style="red")
            console_api.print_msg("[yellow]_______________[/yellow]")

    # os.remove(f"{SHOTS_DIR}/{id}/0.png
    driver.quit()
