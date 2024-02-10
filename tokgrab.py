from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time 
import re
import os
import pandas as pd
import json

tiktok_urls =  ["https://www.tiktok.com/@justmaiko/video/6841591262680730886",
"https://www.tiktok.com/@justmaiko/video/7319932559876525342",
"https://www.tiktok.com/@bbykevv_/video/7298031771952729387",
"https://www.tiktok.com/@richieejuice/video/7299625993742896415",
"https://www.tiktok.com/@soobinismyboyfriend/video/7326419745123749162",
"https://www.tiktok.com/@nevaaadaa/video/7316681825387171077",
"https://www.tiktok.com/@taina/video/7297339538685381894",
"https://www.tiktok.com/@theanimemen/video/7323433434108464430",
"https://www.tiktok.com/@theanimemen/video/7237339371135880494",
"https://www.tiktok.com/@theanimemen/video/7232372653946850603"]
script_path = "./browser_scripts/tiktok_analyze.js"
chromeTest = True
data_path = "./stats_data"
report_time = 0.25
experiment = 0
bandwidth = 0
length = 15

def read_script(file_path):
    with open(file_path, 'r') as file:
        return file.read()
    
def wait_for_element(driver, css_selector, timeout=45):
    end_time = time.time() + timeout
    print(f"Waiting for element with selector {css_selector}...")
    while True:
        try:
            element = driver.find_elements(By.CSS_SELECTOR, css_selector)
            if element:
                return element[0]
            elif time.time() > end_time:
                raise TimeoutError(f"Element with selector {css_selector} not found in {timeout} seconds")
        except NoSuchElementException:
            pass
        time.sleep(0.05)  # Wait 50ms before trying again

def record_xhr_requests(driver, proto, pcap_filename):
    logs_raw = driver.get_log("performance")
    logs = [json.loads(lr["message"])["message"] for lr in logs_raw]
    with open(f'pcaplogs/{pcap_filename}_{proto}.json', 'w') as outfile:
        json.dump(logs, outfile)

js_analyze = read_script(script_path)

def append_to_csv(data, num):
    video_id = re.search(r'(\d+)$', data['url']).group()
    csv_file = f"{data_path}/vid_{num}_{video_id}.csv"
    df = pd.DataFrame(columns=data.keys())
    df = df._append([df, pd.DataFrame([data])], ignore_index=True)
    if os.path.exists(csv_file):
        df.to_csv(csv_file, index=False,mode="a",header=False)
    else:
        df.to_csv(csv_file, index=False,mode="w",header=True)
    return video_id

if __name__ == "__main__":

    if chromeTest:

        s = Service(r"/usr/local/bin/chromedriver")

        chromium_executable_path = '/usr/bin/google-chrome'
        chrome_options = Options()
        chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        chrome_options.add_experimental_option('perfLoggingPrefs', {'enableNetwork': True})
        # chrome_options.add_argument("--headless")  # Runs Chrome without UI
        chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
        chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems


        driver = webdriver.Chrome(service=s, options=chrome_options)
        print("Loading page...")
        counter = 0
        print("Currently Processing Video:", counter)
        for url in tiktok_urls:
            driver.get(url)
            while(True):
                ended=False
                send_data = driver.execute_script(js_analyze)
                video_id = append_to_csv(send_data, counter)
                time.sleep(report_time)
                ended = driver.execute_script("return document.getElementsByTagName('video')[0].ended")                    
                if(ended):
                    record_xhr_requests(driver, video_id, counter)
                    break
                
            time.sleep(1)
            counter+=1
