from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

urls = [

    'https://www.serebii.net/' 
        
        ]
s = Service(r"./chromedriver.exe")
chromium_executable_path = 'C:/Users/khali/Chromium/chrome.exe'
chrome_options = Options()
chrome_options.binary_location = chromium_executable_path

for url in urls:
    driver = webdriver.Chrome(service=s, options=chrome_options)
    driver.get(url)