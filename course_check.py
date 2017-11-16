import time
import sys
import os  
import urllib
import requests

from selenium import webdriver  
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

search_url = "https://horizon.mcgill.ca/pban1/bwskfcls.P_GetCrse"
login_url = "https://horizon.mcgill.ca/pban1/twbkwbis.P_ValLogin"

uname = "carlos.gonzalezoliver@mail.mcgill.ca"
pwd = "sasjajuli_milojuli"

chrome_options = Options()
# chrome_options.add_argument("--headless")
# chrome_options.add_argument("--window-size=1920x1080")


driver = webdriver.Chrome(chrome_options=chrome_options,\
    executable_path=os.path.abspath("chromedriver"))

def login(username, password):
    #get login page
    driver.get(login_url)
    time.sleep(5)
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

def course_search(deptartment, course, term="Winter 2018", dept="COMP"):
    driver.get("https://horizon.mcgill.ca/pban1/bwskfcls.p_sel_crse_search")
    select = Select(driver.find_element_by_id("term_input_id"))
    select.select_by_visible_text(term)
    time.sleep(2)
    # print(driver.page_source)
    print(driver.current_url)

    driver.find_element_by_xpath("/html/body/div[3]/form/input[3]").click()

    time.sleep(2)
    sel = driver.find_elements_by_name("sel_subj")[1]
    select = Select(sel)
    select.select_by_value(dept)
        
    
    #submit department
    driver.find_element_by_name("SUB_BTN").click()
    time.sleep(2)
    print(driver.current_url)

    #select course
    rows = driver.find_elements_by_tag_name("tr")
    for row in rows:
        try:
            course_num = row.text.split()[0]
            print(course_num)
        except IndexError:
            continue
        else:
            if course_num == "767":
                print(course)
                row.find_element_by_name("SUB_BTN").click()
                break

    # course = driver.find_element_by_xpath("//input[@name='SEL_CRSE' and\
        # @value='767']").click()
    
    # driver.find_element_by_link_text("Student Menu").click()
    # driver.find_element_by_link_text("Registration Menu").click()
    
login(uname, pwd)
course_search("hi", "ho")
# htmlSource = driver.page_source
# printt(htmlSource)
