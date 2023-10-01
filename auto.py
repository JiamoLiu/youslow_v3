from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time 

urls = ['https://www.youtube.com/watch?v=GwaRztMaoY0', 
        'https://www.youtube.com/watch?v=Tt4_enX63K0',
        'https://www.youtube.com/watch?v=C-7TIDIKc98',
        'https://www.youtube.com/watch?v=AWEm4tA2hMc',
        'https://www.youtube.com/watch?v=5yb2N3pnztU',
        'https://www.youtube.com/watch?v=gcgKUcJKxIs',
        'https://www.youtube.com/watch?v=dM7x1PNZDo0',
        'https://www.youtube.com/watch?v=S7QsHpLU1Sw',
        'https://www.youtube.com/watch?v=hbZr47jwL_4',
        'https://www.youtube.com/watch?v=swq--rdN-2k',
        'https://www.youtube.com/watch?v=Q7w5IMyJ3pM',
        'https://www.youtube.com/watch?v=v1YojYU5nPQ',
        'https://www.youtube.com/watch?v=L1FdEBTJXus',
        'https://www.youtube.com/watch?v=-t5--PiJsWo'
        ]
s = Service(r"./chromedriver.exe")
chromium_executable_path = 'C:/Users/khali/Chromium/chrome.exe'
chrome_options = Options()
chrome_options.add_argument("--load-extension=C:/Users/khali/OneDrive/Desktop/Code/Research/YTExtension/youslow_v3/YouSlow");
chrome_options.binary_location = chromium_executable_path


driver = webdriver.Chrome(service=s, options=chrome_options)
for url in urls:
    driver.get(url)
    actions = ActionChains(driver)
    actions.send_keys('k')
    actions.perform()
    time.sleep(20)