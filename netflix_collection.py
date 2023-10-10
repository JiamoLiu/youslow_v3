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
import json
import random
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import threading
from subprocess import Popen, PIPE
import signal
import argparse
import pandas as pd
import sys
from datetime import datetime

email = creds.username
pwd = creds.password
home_page_url = "https://www.netflix.com/browse"
intface = "enp11s0"


def get_filename(link):
    return "./production/traces/"+link.split("/")[-1] + "."+str(time.time())


def capture_live_packets(network_interface, filename, stop):
    output = filename+".pcap"

    process = Popen(['tshark', '-i', network_interface,
                    '-w', output, "-s", "400"])
    # stdout, stderr = process.communicate()

    while (stop() == False):
        pass
    process.send_signal(signal.SIGINT)


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
        driver, "/html/body/div[1]/div/div/div[1]/div/div/div/div/div/video", timeout=60)
    paused = driver.execute_script(
        r"""return document.getElementsByTagName("video")[0].paused""")
    if (paused):
        print("paused!!!")
        try:
            wait_until_clickable(
                driver, r"""/html/body/div[1]/div/div/div[1]/div/div[2]/div[2]/div/div[2]/button""", timeout=60)
            driver.find_element(
                "xpath", r"""/html/body/div[1]/div/div/div[1]/div/div[2]/div[2]/div/div[2]/button""").click()
        except:
            pass


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
    movie_request_time = datetime.now()
    driver.get(f"https://www.netflix.com/watch/{movie_id}")
    return movie_request_time


def get_working_url(url_df, num_iteration_of_videos=5):
    session_min = url_df["session_count"].min()

    should_stop = False
    if (session_min >= num_iteration_of_videos):
        should_stop = True
        return None, should_stop
    else:
        urls = list(url_df.query(
            "session_count == {}".format(session_min))["video_id"])
        chosen = random.choice(urls)
        return chosen, should_stop


def record_xhr_requests(driver, proto, pcap_filename):
    logs_raw = driver.get_log("performance")
    logs = [json.loads(lr["message"])["message"] for lr in logs_raw]
    with open(f'{pcap_filename}_{proto}.json', 'w') as outfile:
        json.dump(logs, outfile)


def collect(movie_id, proto="TCP"):
    success = False
    try:
        options = webdriver.ChromeOptions()
        # options = webdriver.ChromeOptions()
        # options.add_argument("--headless")
        # print(os.path.exists())
        desired_capabilities = DesiredCapabilities.CHROME
        desired_capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
        desired_capabilities["pageLoadStrategy"] = "none"

        options.add_extension(f'{os.getcwd()}/Chrome extension.crx')
        # Needs to be big enough to get all the resolutions
        options.add_argument("--window-size=2000,3555")
        if (proto == "TCP"):
            options.add_argument("--disable-quic")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-component-update")

        driver = webdriver.Chrome(
            chrome_options=options, executable_path="/usr/bin/chromedriver_linux64/chromedriver", desired_capabilities=desired_capabilities)
        clear_cookies(driver)
        log_in(driver)
        stopthreads = False
        url = f"https://www.netflix.com/watch/{movie_id}"
        pcap_filename = get_filename(url)
        th = threading.Thread(target=capture_live_packets,
                              args=(intface, pcap_filename, lambda: stopthreads,))

        th.start()
        time.sleep(3)

        movie_request_time = watch_movie(driver, movie_id)
        try_to_click_play(driver)
        try_to_turn_on_stats(driver)

        time.sleep(180)
        record_xhr_requests(driver, proto, pcap_filename)
        driver.close()
        stopthreads = True
        th.join()
        success = True
        return movie_request_time, success

    except KeyboardInterrupt:
        driver.close()
        stopthreads = True
        th.join()
        success = True
        return movie_request_time, success
    except:
        success = False
        return None, success


def increment_session_count(working_urls, video_id):
    working_urls.loc[working_urls["video_id"]
                     == video_id, "session_count"] += 1
    working_urls.to_csv(working_url_file)


def record_session_time(start_time, end_time, proto, session_pair_id, movie_request_time):
    data = pd.DataFrame(
        [[start_time, end_time, proto, session_pair_id, movie_request_time]])
    data.columns = ["start_time", "end_time", "protocol",
                    "session_pair_id", "movie_request_time"]
    data["start_time"] = data["start_time"].astype(str)
    data["end_time"] = data["end_time"].astype(str)
    data["movie_request_time"] = data["movie_request_time"].astype(str)
    filename = "sesssion_start_end_time.csv"
    if (os.path.isfile(filename)):
        data.to_csv(filename, mode="a", header=False, index=False)
    else:
        data.to_csv(filename, index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', action='store')
    args = parser.parse_args()
    working_url_file = args.filename
    working_urls = pd.read_csv(working_url_file)[
        ["category", "video_id", "session_count"]]
    session_pair_id = 1

    while True:
        movie_id, should_stop = get_working_url(working_urls, 5)
        print(movie_id)

        if (should_stop):
            sys.exit()

        start_time = datetime.now()
        success = False
        while (not success):
            movie_request_time, success = collect(movie_id)

        increment_session_count(working_urls, movie_id)
        end_time = datetime.now()
        record_session_time(start_time, end_time, "TCP",
                            session_pair_id, movie_request_time)
        time.sleep(30)
        session_pair_id += 1
