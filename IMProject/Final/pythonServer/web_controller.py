from asyncio import sleep
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
 
# Define a custom user agent
my_user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"

# Set up Chrome options
chrome_options = Options()
#chrome_options.add_argument("--headless")

# Set the custom User-Agent
chrome_options.add_argument(f"--user-agent={my_user_agent}")


driver = webdriver.Chrome(options=chrome_options)

driver.get("https://mail.google.com/")
 

# Keep the script running until the window is manually closed
import asyncio

async def keep_running():
    try:
        while True:  
            await sleep(100)
            element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div:nth-child(23)/div.nH/div/div.nH.aqk.aql.bkL/div.aeN.WR.baA.nH.oy8Mbf.bhZ/div.aic/div/div"))
            )
           
            print(element.text)

    except KeyboardInterrupt:
        pass

asyncio.run(keep_running())

# Remove the line that closes the browser window
# driver.close()