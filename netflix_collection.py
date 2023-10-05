# display = Display(visible=0, size=(2000, 3555))
# display.start()
import click
from matplotlib.pyplot import pause
from selenium import webdriver
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import creds
from selenium.webdriver.common.action_chains import ActionChains

email = creds.username
pwd = creds.password
movie_id = "70196252"
home_page_url = "https://www.netflix.com/browse"


def clear_cookies(driver):
    driver.get("https://www.netflix.com/clearcookies")
    wait_until_url_changes_to(driver, "https://www.netflix.com/")
    print("COOKIES CLEARED!")


def wait_until_present(driver, xpath, timeout=20):
    WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((By.XPATH, xpath)))


def wait_until_clickable(driver, xpath, timeout=20):
    WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((By.XPATH, xpath)))


def wait_until_interactable(driver, xpath, timeout=20):
    WebDriverWait(driver, timeout).until(
        EC.visibility_of_element_located((By.XPATH, xpath)))


def wait_until_url_changes_to(driver, desired_url, timeout=20):
    wait = WebDriverWait(driver, timeout)
    wait.until(
        lambda driver: driver.current_url == desired_url)


def ctrl_shift_alt_q(driver):
    actions = ActionChains(driver)
    actions.key_down(Keys.CONTROL).key_down(Keys.SHIFT).key_down(Keys.ALT).send_keys(
        "Q").key_up(Keys.CONTROL).key_up(Keys.SHIFT).key_up(Keys.ALT).perform()


def try_to_turn_on_stats(driver):
    wait_until_present(
        driver, "/html/body/div[1]/div/div/div[1]/div/div/div/div/div/video")
    ctrl_shift_alt_q(driver)


def try_to_click_play(driver):
    wait_until_present(
        driver, "/html/body/div[1]/div/div/div[1]/div/div/div/div/div/video")
    paused = driver.execute_script(
        r"""return document.getElementsByTagName("video")[0].paused""")
    if (paused):
        driver.find_element(
            "xpath", '/html/body/div[1]/div/div/div[1]').click()


def log_in(driver):
    driver.get("https://www.netflix.com/Login")
    username_xpath = "/html/body/div[1]/div/div[3]/div/div/div[1]/form/div[1]/div/div/label/input"
    wait_until_present(driver, username_xpath)
    username_filed = driver.find_element("xpath", username_xpath)
    username_filed.send_keys(email)
    time.sleep(2)

    password_xpath = "/html/body/div[1]/div/div[3]/div/div/div[1]/form/div[2]/div/div/label/input"
    wait_until_present(driver, password_xpath)
    password_field = driver.find_element("xpath", password_xpath)
    password_field.send_keys(pwd)
    time.sleep(2)

    singin_button_xpath = "/html/body/div[1]/div/div[3]/div/div/div[1]/form/button"
    wait_until_clickable(driver, singin_button_xpath)
    # time.sleep(2)
    driver.find_element("xpath", singin_button_xpath).click()
    wait_until_url_changes_to(driver, home_page_url)
    print("LOGIN SUCCESSFUL!")
    # time.sleep(10)


def watch_movie(driver, movie_id):
    driver.get(f"https://www.netflix.com/watch/{movie_id}")


def main():
    options = webdriver.ChromeOptions()
    proto = "TCP"
    # options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    # print(os.path.exists())
    options.add_argument("--disable-logging")
    options.add_extension(f'{os.getcwd()}/Chrome extension.crx')
    # Needs to be big enough to get all the resolutions
    options.add_argument("--window-size=2000,3555")
    if (proto == "TCP"):
        options.add_argument("--disable-quic")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")

    # stopthreads =False
    # th = threading.Thread(target=capture_live_packets, args=(url,intface,lambda: stopthreads,))

    driver = webdriver.Chrome(
        chrome_options=options, executable_path="/usr/bin/chromedriver_linux64/chromedriver")
    clear_cookies(driver)
    log_in(driver)
    # time.sleep(100000000)
    watch_movie(driver, movie_id)
    try_to_turn_on_stats(driver)
    time.sleep(5)
    try_to_click_play(driver)
    time.sleep(1000000)


if __name__ == "__main__":
    main()
