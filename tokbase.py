import signal
import json
import os
import sys
import json
import pandas as pd
import re
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from browsermobproxy import Server

#constants
script_path = "./browser_scripts/tiktok_analyze.js"
chromeTest = True
base_dir = sys.argv[1] #DataBase initial folder
location = sys.argv[2] #Campus or Satellite
rate = sys.argv[3] #MBPS (3MBPS or 5MBPS)
run_label = sys.argv[4] #Numbered Run 1-5?
data_path = sys.argv[5] #Location of Specific Instance with QoE, QoS, PCAP and HAR
log_path = f"{base_dir}/{location}/{rate}/{run_label}/log.txt"
report_time = 15

def refresh_button_exists(driver, timeout=0.01):
    try:
        wait = WebDriverWait(driver, timeout)
        wait.until(EC.presence_of_element_located((By.XPATH, '//button[contains(text(), "Refresh")]')))
        return True
    except TimeoutException:
        return False

def guest_button_exists(driver, timeout=0.01):
    
    try:
        wait = WebDriverWait(driver, timeout)
        wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="css-1cp64nz-DivTextContainer e1cgu1qo3"]//div[contains(text(), "Continue as guest")]')))
        return True
    except TimeoutException:
        return False


def click_guest(driver):
    wait = WebDriverWait(driver, 0.01)
    continue_as_guest_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="css-1cp64nz-DivTextContainer e1cgu1qo3"]//div[contains(text(), "Continue as guest")]')))
    continue_as_guest_button.click()

def click_refresh_until_disappears(driver, timeout=1.5):
    try:
        while True:
            try:
                wait = WebDriverWait(driver, timeout)
                refresh_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Refresh")]')))
                refresh_button.click()
                # WebDriverWait(driver, 2).until_not(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Refresh")]')))
            except TimeoutException:
                # If the button is not found or is no longer clickable, break the loop
                break
    except NoSuchElementException:
        # If the button is not found at all, exit the loop
        pass
#returns server, proxy for adjustment later
def initialize_proxy(server_path='./browsermob-proxy-2.1.4/bin/browsermob-proxy'):
    server = Server(server_path)
    server.start()
    proxy = server.create_proxy()
    return server, proxy
# deinitializes proxy and stops server
def delete_proxy(server):
    server.stop()
#initializes webdriver with proxy
def initialize_webdriver(proxy):
    s = Service(r"/home/khalid/Code/Research/youslow_v3/chromefiles/chromedriver")
    chrome_options = Options()
    chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
    chrome_options.add_experimental_option('perfLoggingPrefs', {'enableNetwork': True})
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    proxy_option = f'--proxy-server={proxy.proxy}'
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument(proxy_option)
    chrome_options.page_load_strategy = 'eager'
    driver = webdriver.Chrome(service=s, options=chrome_options)
    proxy.new_har("tiktok", options={'captureHeaders': True, 'captureContent': True})
    return driver

# Function to cleanly stop webdriver
def stop_webdriver(driver):
    driver.quit()

#read js file
def read_script(file_path):
    with open(file_path, 'r') as file:
        return file.read()
#QoS data is stored in .json file
def record_qos(driver):
    logs_raw = driver.get_log("performance")
    logs = [json.loads(lr["message"])["message"] for lr in logs_raw]
    with open(f'{data_path}/{location}_{rate}Mbps_run_{run_label}.json', 'w') as outfile:
        json.dump(logs, outfile)
#QoE data is stored in .csv file
def record_qoe(data):
    # video_id = re.search(r'(\d+)$', data['url']).group()
    csv_file = f"{data_path}/{location}_{rate}Mbps_run_{run_label}.csv"
    df = pd.DataFrame(columns=data.keys())
    # Filter out empty or all-NA entries before concatenation
    df_filtered = df.dropna(how='all')  # Drop rows where all values are NaN
    df_filtered = df_filtered.dropna(axis=1, how='all')  # Drop columns where all values are NaN
    # Concatenate filtered DataFrame with new data
    df = pd.concat([df_filtered, pd.DataFrame([data])], ignore_index=True)
    if os.path.exists(csv_file):
        df.to_csv(csv_file, index=False,mode="a",header=False)
    else:
        df.to_csv(csv_file, index=False,mode="w",header=True)
#HAR data is stored in .har file
def record_har(proxy):
    har_data = proxy.har
    HAR_FILE_PATH = f'{data_path}/{location}_{rate}Mbps_run_{run_label}.har'
    with open(HAR_FILE_PATH, 'w') as har_file:
        json.dump(har_data, har_file, indent=4)

def handle_interrupt(signum, frame):
    global driver, server
    stop_webdriver(driver)
    delete_proxy(server)
    print("Process interrupted, cleanup done")
    sys.exit(0)

# Setup signal handlers
signal.signal(signal.SIGINT, handle_interrupt)
js_analyze = read_script(script_path)

if __name__ == "__main__":
    server, proxy = initialize_proxy()
    driver = initialize_webdriver(proxy)
    tiktok_url = "https://www.tiktok.com/foryou"
    with open(log_path, 'a') as file:
        file.write(f"Starting tiktok script for {data_path}\n")
    try:
        driver.get(tiktok_url)
        try:
            video_element = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.TAG_NAME, "video")))
        except:
            if guest_button_exists(driver):
                click_guest(driver)
            if refresh_button_exists(driver):
                click_refresh_until_disappears(driver)
        video_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "video")))
        start_time = time.time()
        while(True):
            elapsed_time = time.time() - start_time
            ended=False
            send_data = driver.execute_script(js_analyze)
            record_qoe(send_data)
            ended = driver.execute_script("return document.getElementsByTagName('video')[0].ended")
            if elapsed_time > report_time:  
                record_qos(driver)
                record_har(proxy)
                break
    except Exception as e:
        print(f"Error: {e}")
    finally:
        stop_webdriver(driver)
        delete_proxy(server)
        print("Cleanup done")