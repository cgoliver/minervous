import time
import os  
import urllib
import requests

from selenium import webdriver  
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options


chrome_options = Options()  
chrome_options.add_argument("--headless")  
chrome_options.binary_location = '/Applications/Google Chrome \
    Canary.app/Contents/MacOS/Google Chrome Canary' 


driver = webdriver.Chrome(executable_path=os.path.abspath("chromedriver"),\
    chrome_options=chrome_options)

search_url = "https://horizon.mcgill.ca/pban1/bwskfcls.P_GetCrse"
login_url = "https://horizon.mcgill.ca/pban1/twbkwbis.P_ValLogin"

username = "carlos.gonzalezoliver@mail.mcgill.ca"
pwd = "sasjajuli_milojuli"

params=(("sid",username),
        ("PIN",pwd))

data=urllib.parse.urlencode(params)

cookies={"TESTID":"set"}

r_login = requests.post(login_url,data=data,cookies=cookies)
sessionid = r_login.cookies.get("SESSID")

print(sessionid)

r=requests.post(search_url,cookies={"SESSID": sessionid})
print(r.status_code)
print(r.url)

driver.get(r.url)

time.sleep(5)

htmlSource = driver.page_source
printt(htmlSource)
