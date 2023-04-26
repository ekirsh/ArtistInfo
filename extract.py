from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium_stealth import stealth
import undetected_chromedriver as uc
import time
from urllib.parse import urlparse
import openai
import sys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent


openai.api_key = "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"

def bypass_cloudflare(driver):
    stage = WebDriverWait(driver, 20).until(presence_of_element_located((By.CSS_SELECTOR, '#challenge-stage')))
    print(stage)
    time.sleep(2.8)
    try:
        frame = WebDriverWait(driver, 20).until(presence_of_element_located((By.XPATH,'//*[contains(@id, "cf-chl-widget")]')))
    except:
        driver.refresh()
    driver.switch_to.frame(frame)
    print(frame)
    time.sleep(1.7)
    challenge_stage = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, '#challenge-stage > div > label > span.mark')))
    print("Found")
    element = driver.find_element(By.CSS_SELECTOR, '#challenge-stage > div > label > input')
    time.sleep(2.6)
    element.click()
    driver.switch_to.default_content()

def createDriver() -> uc.Chrome:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    prefs = {"profile.managed_default_content_settings.images":2}
    chrome_options.headless = True


    chrome_options.add_experimental_option("prefs", prefs)
    myDriver = uc.Chrome(options=chrome_options)

    return myDriver

def getPerplex(driver: uc.Chrome, artist: str):
    driver.get(f'https://www.perplexity.ai/search?q=songwriter/producer+{artist}')
    time.sleep(1.7)
    # Find and input the question in the textarea field
    #search_field = WebDriverWait(driver, 10).until(presence_of_element_located((By.TAG_NAME, "textarea")))
    #search_field.send_keys(f'Tell me everything there is to know about artist/songwriter/producer {artist}. Go into the amount of detail that a CEO of a record label would want to know')
    # Submit the question by pressing Enter and wait for the results page to load
    #search_field.send_keys(Keys.RETURN)
    WebDriverWait(driver, 10).until(presence_of_element_located((By.CSS_SELECTOR, "#__next > main > div > div > div.grow > div > div > div.min-h-\[100vh\].flex.flex-col.pt-\[56px\].pb-\[124px\].md\:pb-0 > div > div > div:nth-child(2) > div > div > div > div.border-borderMain.dark\:border-borderMainDark.divide-borderMain.dark\:divide-borderMainDark.ring-borderMain.dark\:ring-borderMainDark.transition.duration-300.bg-transparent > div > div.border-borderMain.dark\:border-borderMainDark.divide-borderMain.dark\:divide-borderMainDark.ring-borderMain.dark\:ring-borderMainDark.transition.duration-300.bg-background.dark\:bg-backgroundDark > div.default.font-sans.text-base.text-textMain.dark\:text-textMainDark.selection\:bg-super.selection\:text-white.dark\:selection\:bg-opacity-50.selection\:bg-opacity-70 > div > div:nth-child(1) > div > span")))

    time.sleep(3)

    # Print out the results
    results = driver.find_elements(By.CSS_SELECTOR, "#__next > main > div > div > div.grow > div > div > div.min-h-\[100vh\].flex.flex-col.pt-\[56px\].pb-\[124px\].md\:pb-0 > div > div > div:nth-child(2) > div > div > div > div.border-borderMain.dark\:border-borderMainDark.divide-borderMain.dark\:divide-borderMainDark.ring-borderMain.dark\:ring-borderMainDark.transition.duration-300.bg-transparent > div > div.border-borderMain.dark\:border-borderMainDark.divide-borderMain.dark\:divide-borderMainDark.ring-borderMain.dark\:ring-borderMainDark.transition.duration-300.bg-background.dark\:bg-backgroundDark > div.default.font-sans.text-base.text-textMain.dark\:text-textMainDark.selection\:bg-super.selection\:text-white.dark\:selection\:bg-opacity-50.selection\:bg-opacity-70 > div > div:nth-child(1) > div > span")
    refs = results[0].find_elements(By.TAG_NAME, "a")
    references = []
    for ref in refs:
        y = {"title": urlparse(ref.get_attribute("href")).netloc, "url": ref.get_attribute("href")}
        if y not in references:
            references.append(y)

    #print(results[0].text.strip())
    print(references)
    msg = f'{references} /n {results[0].text.strip()}'
    print(format_response(msg))
    #for result in results:
        #print(result.text.strip())




def doBackgroundTask(inp):
    print("Doing background task")
    print(inp.msg)
    print("Done")