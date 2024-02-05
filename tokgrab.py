from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time 

tiktok_urls = ["https://www.tiktok.com/@hey_im_moodie/video/7294260320426839342",
        "https://www.tiktok.com/@hey_im_moodie/video/7259463538891066667",
        "https://www.tiktok.com/@cg5beats/video/7288033141762133291",
        "https://www.tiktok.com/@gamexplain/video/7070879107264875818",
        "https://www.tiktok.com/@ucsbvsa/video/7301555633088777518",
        "https://www.tiktok.com/@ucsbvsa/video/7297420252030225706",
        "https://www.tiktok.com/@avantgardey_/video/7288298668883594497",
        "https://www.tiktok.com/@laoceats/video/7301496364578508078",
        "https://www.tiktok.com/@oliviaroseolson/video/6998945191709117701",
        "https://www.tiktok.com/@avantgardey_/video/7260404785260563720",
        ]


if __name__ == "__main__":
    chrome = False
    script_path = "./browser_scripts/tiktok_analyze"

    if chrome:
        s = Service(r"/usr/local/bin/chromedriver")
        chromium_executable_path = '/usr/bin/google-chrome'
        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # Runs Chrome without UI
        chrome_options.add_argument("--no-sandbox")  # Bypass OS security model
        chrome_options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems
        chrome_options.add_extension("TokSlow.crx")

        driver = webdriver.Chrome(service=s, options=chrome_options)