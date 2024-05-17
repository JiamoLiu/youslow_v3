from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC  
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from browsermobproxy import Server
from datetime import datetime
import time 
import sys
import re
import os
import pandas as pd
import json
import subprocess
import signal

if len(sys.argv) !=7:
    print("Usage: python3 tokgrab.py <data_path> <vidlength> <run_label> <rate> <base_dir> <location>")
    exit(0)

script_path = "./browser_scripts/tiktok_analyze.js"
chromeTest = True
data_path = sys.argv[1] #path right before QoE/QoS
vidlength = sys.argv[2] #15 or 60
run_label = sys.argv[3] #Numbered Run
rate = sys.argv[4] #MBPS
base_dir = sys.argv[5] #file storage
location = sys.argv[6]
limit_time = 0
if vidlength == "15" or vidlength == "test":
    limit_time = 90
elif vidlength == "60":
    limit_time = 180
log_path = f"{base_dir}/{vidlength}/{location}/{rate}Mbps/{run_label}/log.txt"
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

def start_pcap_capture(index):
    # Define the current directory
    current_dir = os.getcwd()

    # Get the timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # Define the PCAP file name
    pcap_file = f"{current_dir}/pcap_try{index}_{timestamp}.pcap"

    # Start tcpdump and write to the PCAP file
    tcpdump_process = subprocess.Popen(["tcpdump", "-w", pcap_file, "-i", "any"])

    # Get the process ID of tcpdump and save it to a file
    tcpdump_pid = tcpdump_process.pid
    with open("tcpdump_pid.txt", "w") as pid_file:
        pid_file.write(str(tcpdump_pid))

def stop_pcap_capture():
    # Read the process ID from the file
    try:
        with open("tcpdump_pid.txt", "r") as pid_file:
            tcpdump_pid = int(pid_file.read().strip())

        # Terminate the tcpdump process
        os.kill(tcpdump_pid, signal.SIGTERM)
        print(f"tcpdump process with PID {tcpdump_pid} terminated.")
        
        # Optionally, remove the PID file after stopping the process
        os.remove("tcpdump_pid.txt")
    except FileNotFoundError:
        print("Error: PID file not found. Is tcpdump running?")
    except ProcessLookupError:
        print("Error: Process not found. It might have already been stopped.")
    except Exception as e:
        print(f"An error occurred: {e}")

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
    print(vidlength)
    retry_attempt = 7
    with open(log_path, 'a') as file:
        file.write("Initalize"+"\n")
    for url in tiktok_urls:
        attempt = 1
        counter += 1
        while (attempt<retry_attempt):
            try:    
                driver.get(url)
                video_element = WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.TAG_NAME, "video"))
                )
                start_time = time.time()
                while(True):
                    elapsed_time = time.time() - start_time
                    if elapsed_time > limit_time:  
                        raise TimeoutError(f'Timeout occurred after {limit_time} seconds')
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
                        attempt=30
                        break
            except WebDriverException as e:
                print(f"WebDriverException occurred: {e}")
                with open(log_path, 'a') as file:
                    file.write(f"WebDriverException occurred during Run #{run_label}, Video #{counter}, MBPS #{rate}: {e.msg}\n")
                    file.write(f"Retry occur, attempt {attempt}\n")
                attempt+=1
                delete_csv_file(video_id, counter)  
            except TimeoutError as e:
                print(f"TimeoutError occurred: {e}")
                with open(log_path, 'a') as file:
                    file.write(f"Timeout occurred during Run #{run_label}, Video #{counter}, MBPS #{rate}\n")
                    file.write(f"Retry occur, attempt {attempt}\n")
                attempt+=1
                delete_csv_file(video_id, counter)  
            except Exception as e:
                print(f"NonLabeledException occurred: {e}")
                with open(log_path, 'a') as file:
                    file.write(f"NonLabeledException occurred during Run #{run_label}, Video #{counter}, MBPS #{rate}: {e.msg}\n")      
                    file.write(f"Retry occur, attempt {attempt}\n")
                attempt+=1
                delete_csv_file(video_id, counter)  
            finally:
                time.sleep(1)
                driver.quit()
                driver = initalize_webdriver(proxy)
                if attempt == 7:
                    print(f"Failure after 6 retrues Run #{run_label}, Video #{counter}, MBPS #{rate}")
                    with open(log_path, 'a') as file:
                        file.write(f"FAIL DURING Run #{run_label}, Video #{counter}, Mbps {rate}, Time {vidlength} sec\n")
    print(f"Total Successful Attempts: {success} out of {counter} attemps")
    driver.quit()
    proxy.close()
    server.stop()
    with open(log_path, 'a') as file:
        file.write(f"Total Successful Attempts: {success} out of {counter} attemps\n")
