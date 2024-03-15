from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  
from browsermobproxy import Server
import time 
import sys
import re
import os
import pandas as pd
import json

if len(sys.argv) !=5:
    print("Usage: python3 tokgrab.py <arg1> <arg2> <arg3> <arg4>")



script_path = "./browser_scripts/tiktok_analyze.js"
chromeTest = True
data_path = sys.argv[1] #path right before QoE/QoS
vidlength = sys.argv[2] #15 or 60
run_label = sys.argv[3] #Numbered Run
rate = sys.argv[4] #MBPS
log_path = f"tiktok_data/{run_label}/{vidlength}/{rate}Mbps/log.txt"
report_time = 0.25
experiment = 0
bandwidth = 0

server = Server('./browsermob-proxy-2.1.4/bin/browsermob-proxy')
server.start()
proxy = server.create_proxy()

def initalize_webdriver(proxy):
    s = Service(r"/home/khalid/Code/Research/youslow_v3/chromefiles/chromedriver")
    chrome_options = Options()
    chrome_options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
    chrome_options.add_experimental_option('perfLoggingPrefs', {'enableNetwork': True})
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    proxy_option = f'--proxy-server={proxy.proxy}'
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument(proxy_option)
    driver = webdriver.Chrome(service=s, options=chrome_options)
    proxy.new_har("tiktok", options={'captureHeaders': True, 'captureContent': True})
    return driver

def read_urls_from_file(file_path):
    urls = []
    file_path="tiktoklinks/"+file_path+".txt"
    with open(file_path, 'r') as file:
        for line in file:
            # Strip any leading/trailing whitespaces and append to the list
            urls.append(line.strip())
    return urls

def read_script(file_path):
    with open(file_path, 'r') as file:
        return file.read()
    
def wait_for_element(driver, css_selector, timeout=45):
    end_time = time.time() + timeout
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

def record_xhr_requests(driver, pcap_filename, proto):
    logs_raw = driver.get_log("performance")
    logs = [json.loads(lr["message"])["message"] for lr in logs_raw]
    with open(f'{data_path}/QoS/run_{run_label}_vid_{proto}_{pcap_filename}.json', 'w') as outfile:
        json.dump(logs, outfile)

js_analyze = read_script(script_path)

def append_to_csv(data, num):
    video_id = re.search(r'(\d+)$', data['url']).group()
    csv_file = f"{data_path}/QoE/run_{run_label}_vid_{num}_{video_id}.csv"
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
    return video_id

def delete_csv_file(video_id, num):
    try:
        csv_file = f"{data_path}/QoE/run_{run_label}_vid_{num}_{video_id}.csv"
        if os.path.exists(csv_file):
            os.remove(csv_file)
            print(f"File '{csv_file}' successfully deleted.")
        else:
            print(f"No file found at '{csv_file}', nothing to delete.")
    except Exception as e:
        print(f"Error deleting file: {e}")



if __name__ == "__main__":
    driver = initalize_webdriver(proxy)
    counter = 0
    success = 0
    tiktok_urls = read_urls_from_file(vidlength)
    for url in tiktok_urls:
        try:    
            driver.get(url)
            while(True):
                ended=False
                send_data = driver.execute_script(js_analyze)
                video_id = append_to_csv(send_data, counter)
                time.sleep(report_time)
                ended = driver.execute_script("return document.getElementsByTagName('video')[0].ended")                    
                if(ended):
                    record_xhr_requests(driver, video_id, counter)
                    har_data = proxy.har
                    HAR_FILE_PATH = f'{data_path}/HAR/run_{run_label}_vid_{counter}_{video_id}.har'
                    with open(HAR_FILE_PATH, 'w') as har_file:
                        json.dump(har_data, har_file, indent=4)
                    response = f"SUCCESS DURING Run #{run_label}, Video #{counter}, Mbps {rate}, Time {vidlength} sec"
                    print(response)
                    with open(log_path, 'a') as file:
                        file.write(response+"\n")                 
                    success+=1
                    break
        except WebDriverException as e:
            print(f"WebDriverException occurred: {e}")
            with open(log_path, 'a') as file:
                file.write(f"WebDriverException occurred during Run #{run_label}, Video #{counter}, MBPS #{rate}: {e.msg}\n")
            delete_csv_file(video_id, counter)  
        except Exception as e:
            print(f"NonLabeledException occurred: {e}")
            with open(log_path, 'a') as file:
                file.write(f"NonLabeledException occurred during Run #{run_label}, Video #{counter}, MBPS #{rate}: {e.msg}\n")      
            delete_csv_file(video_id, counter)           
        finally:
            time.sleep(1)
            counter+=1
            driver.quit()
            driver = initalize_webdriver(proxy)
    print(f"Total Successful Attempts: {success} out of {counter} attemps")
