from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import os

# Path to the chromedriver (in the current directory)
chromedriver_path = os.path.join(os.getcwd(), 'chromedriver')

# Set up the service for Chrome
service = Service(chromedriver_path)

# Set up Chrome options
options = webdriver.ChromeOptions()

# Initialize the Chrome driver
driver = webdriver.Chrome(service=service, options=options)

# Navigate to a website of your choice
driver.get("http://www.serebii.net")

# Add your automation script here

# Close the browser
# driver.quit()
