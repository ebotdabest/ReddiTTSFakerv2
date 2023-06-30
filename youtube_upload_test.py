from selenium import webdriver
from selenium.webdriver.common.by import By
from config import WEBDRIVER_PATH, YT_ACCOUNT


gmailId, passWord = YT_ACCOUNT["email"], YT_ACCOUNT["password"]

def upload(title, description, tags, visibility, video):
    driver = webdriver.Chrome(WEBDRIVER_PATH)
    driver.maximize_window()
    try:
        driver.get(r'https://accounts.google.com/signin/v2/identifier?continue=' + \
                   'https%3A%2F%2Fmail.google.com%2Fmail%2F&service=mail&sacu=1&rip=1' + \
                   '&flowName=GlifWebSignIn&flowEntry = ServiceLogin')
        driver.implicitly_wait(15)

        loginBox = driver.find_element(By.XPATH, '//*[@id ="identifierId"]')
        loginBox.send_keys(gmailId)

        nextButton = driver.find_elements(By.XPATH,'//*[@id ="identifierNext"]')
        nextButton[0].click()

        passWordBox = driver.find_element(By.XPATH,
            '//*[@id ="password"]/div[1]/div / div[1]/input')
        passWordBox.send_keys(passWord)

        nextButton = driver.find_elements(By.XPATH, '//*[@id ="passwordNext"]')
        nextButton[0].click()

        print('Login Successful...!!')

        driver.get("https://youtube.com")
    except:
        print('Login Failed')

    driver.get("https://www.youtube.com/upload")
    upload_vid_btn = driver.find_element(By.XPATH, "//input[@type='file']")
    upload_vid_btn.send_keys(video)

    title_input = driver.find_element(By.XPATH, '//*[@id="child-input"]')
    title_input.click()
    text_input_input = title_input.find_element(By.XPATH, '//*[@id="textbox"]')
    text_input_input.clear()
    text_input_input.send_keys(title)
    descripton_input = driver.find_element(By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[2]/ytcp-social-suggestions-textbox/ytcp-form-input-container/div[1]/div[2]/div/ytcp-social-suggestion-input/div')
    descripton_input.click()
    descripton_input.send_keys(description)


    nokid = driver.find_element(By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-ve/ytcp-video-metadata-editor/div/ytcp-video-metadata-editor-basics/div[5]/ytkc-made-for-kids-select/div[4]/tp-yt-paper-radio-group/tp-yt-paper-radio-button[2]')
    nokid.click()

    next = driver.find_element(By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[2]/div/div[2]/ytcp-button[2]/div')
    next.click()

    stuf = driver.find_element(By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/div[1]/ytcp-animatable/ytcp-stepper/div/div[4]/button')
    stuf.click()

    visible = driver.find_element(By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-uploads-review/div[2]/div[1]/ytcp-video-visibility-select/div[2]/tp-yt-paper-radio-group/tp-yt-paper-radio-button[3]/div[1]')
    mid = driver.find_element(By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-uploads-review/div[2]/div[1]/ytcp-video-visibility-select/div[2]/tp-yt-paper-radio-group/tp-yt-paper-radio-button[2]/div[1]')
    xdd = driver.find_element(By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[1]/ytcp-uploads-review/div[2]/div[1]/ytcp-video-visibility-select/div[2]/tp-yt-paper-radio-group/tp-yt-paper-radio-button[1]/div[1]')
    if visibility == "visible":
        visible.click()
    elif visibility == "mid":
        mid.click()
    elif visibility == "priv":
        xdd.click()

    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.support.ui import WebDriverWait

    data = WebDriverWait(driver, 120).until(
        EC.text_to_be_present_in_element((By.XPATH, "/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[2]/div/div[1]/ytcp-video-upload-progress/span"), 'Ellenőrzések futtatása kész. Nem találtunk problémát.'))

    if data:
        save = driver.find_element(By.XPATH, '/html/body/ytcp-uploads-dialog/tp-yt-paper-dialog/div/ytcp-animatable[2]/div/div[2]/ytcp-button[3]/div')
        save.click()

    nice = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/ytcp-video-share-dialog/ytcp-dialog/tp-yt-paper-dialog/div[2]/div/div/ytcp-icon-button/tp-yt-iron-icon'))
    )

    if nice:
        nice.click()
        driver.quit()



# login()
# upload("Askreddit", "First video", ["reddit", "askreddit"], "mid", r"D:\ReddiTTSFakerv1\ReddiTTSFaker-v2-private\videos\10oc0di\video.mp4")
# driver.quit()

'app, "redditwanderernice@gmail.com", "ThereddiTreg2023"'