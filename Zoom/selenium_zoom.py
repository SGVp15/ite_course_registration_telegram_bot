import asyncio

from selenium import webdriver
from selenium.common import NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException, \
    InvalidArgumentException
from selenium.webdriver.common.by import By
from selenium_stealth import stealth

from Config import FILE_XPATH_BTN_ZOOM_REGISTRATION
from Contact.Contact import User
from Utils.chromedriver_autoupdate import ChromedriverAutoupdate
from Utils.log import log


async def registration_user_zoom_link(user: User) -> bool:
    ChromedriverAutoupdate(operatingSystem="win").check()

    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")

    # options.add_argument("--headless")
    options.add_argument("--disable-notifications")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options)
    stealth(driver,
            languages=["ru-RU", "ru"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )
    web_error = (
        NoSuchElementException, ElementClickInterceptedException, StaleElementReferenceException,
        InvalidArgumentException)

    async def fill_form(contact: User):
        async def fill_element(find_element='question_last_name', text=''):
            element = driver.find_element(by=By.ID, value=find_element)
            element.clear()
            element.send_keys(text)
            await asyncio.sleep(0.5)

        await asyncio.sleep(1)
        await fill_element('question_first_name', contact.first_name)
        await fill_element('question_last_name', contact.last_name)
        await fill_element('question_email', contact.email)

    for i in range(3):
        driver.get(url=user.url_registration)
        await asyncio.sleep(1)
        try:
            await fill_form(user)
            await asyncio.sleep(5)
            log.info('fill_form_ok')

            try:
                with open(FILE_XPATH_BTN_ZOOM_REGISTRATION, mode='r', encoding='utf-8') as f:
                    xpath = f.read()
            except FileNotFoundError:
                xpath = '//div[@class="btn-register mgb-lg mgt-sm"]//button'

            driver.find_element(By.XPATH, xpath).click()
        except web_error:
            await asyncio.sleep(4)
            continue
        # check page is registration - ok
        await asyncio.sleep(1)
        try:
            driver.find_element(By.XPATH, xpath).click()
        except web_error:
            driver.close()
            driver.quit()
            await asyncio.sleep(1)
            return True

    driver.close()
    driver.quit()
    await asyncio.sleep(1)
    return False
