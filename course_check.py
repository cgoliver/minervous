import time
import sys
import os  
import logging

from selenium import webdriver  
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

try:
    from mcgill_login import uname, pwd
except:
    pass

search_url = "https://horizon.mcgill.ca/pban1/bwskfcls.P_GetCrse"
login_url = "https://horizon.mcgill.ca/pban1/twbkwbis.P_ValLogin"

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--window-size=1920x1080")


driver = webdriver.Chrome(chrome_options=chrome_options,\
    executable_path=os.path.abspath("chromedriver"))

def login(username, password):
    #get login page
    driver.get(login_url)
    time.sleep(2)
    #give email
    uname = driver.find_element_by_xpath("//*[@id=\"mcg_un\"]")

    #give password
    pw = driver.find_element_by_xpath("//*[@id=\"mcg_pw\"]")

    uname.send_keys(username)
    pw.send_keys(password)

    time.sleep(1)

    submit = driver.find_element_by_xpath("//*[@id=\"mcg_un_submit\"]")

    submit.click()

    return driver.page_source 

def check_availability(course, crn, term="Winter 2018", dept="COMP"):
    """
        Returns:
            dict: keys are info fields and values are status. eg.
            dict['status']: "Active"
            dict['remaining']: 3

    """
    driver.get("https://horizon.mcgill.ca/pban1/bwskfcls.p_sel_crse_search")
    select = Select(driver.find_element_by_id("term_input_id"))
    select.select_by_visible_text(term)

    driver.find_element_by_xpath("/html/body/div[3]/form/input[3]").click()

    sel = driver.find_elements_by_name("sel_subj")[1]
    select = Select(sel)
    select.select_by_value(dept)
        
    
    #submit department
    driver.find_element_by_name("SUB_BTN").click()
    logging.debug(driver.current_url)

    #select course
    rows = driver.find_elements_by_tag_name("tr")
    for row in rows:
        try:
            course_num = row.text.split()[0]
        except IndexError:
            continue
        else:
            if course_num == course:
                row.find_element_by_name("SUB_BTN").click()
                break

    rows = driver.find_elements_by_tag_name("tr")
    info_dict = {}
    for row in rows:
        if crn in row.text:
            #get info from data row
            rem = row.find_elements_by_tag_name("td")[12].text
            status = row.find_elements_by_tag_name("td")[19].text
            info_dict["spots"] = rem
            info_dict["status"] = status
            return info_dict 
    
    
if __name__ == "__main__":
    login(uname, pwd)
    rem = check_availability("767", "11806")
