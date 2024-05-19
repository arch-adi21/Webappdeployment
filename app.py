from flask import Flask, jsonify
from flask_cors import CORS,cross_origin
import pytest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup as bs
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.select import Select
import re
from selenium.webdriver.support import expected_conditions as EC
import os
from datetime import date
from chromedriver_py import binary_path # this will get you the path variable

# svc = webdriver.ChromeService(executable_path=binary_path)
# driver = webdriver.Chrome(service=svc)

application = Flask(__name__) # initializing a flask app
app=application
CORS(app)
@app.route('/',methods=['GET'])
@cross_origin()
def announcements():
    DRIVER_PATH = r"chromedriver.exe"
    service= webdriver.ChromeService(executable_path=binary_path)
    driver = webdriver.Chrome(service=service)
    vars={}
    driver.get("https://ums.lpu.in/lpuums/LoginNew.aspx")
    driver.set_window_size(768, 864)
    driver.find_element(By.ID, "txtU").send_keys("12101718")
    try:
        search2 = driver.find_element(by=By.ID, value="TxtpwdAutoId_8767")
        search2.send_keys("Hatyarr5@")
    except Exception as e:
        #print(f"Error finding or clicking submit button: {e}")
        search2 = driver.find_element(by=By.ID, value="TxtpwdAutoId_8767")
        search2.send_keys("Hatyarr5@")
    driver.find_element(By.ID, "iBtnLogins150203125").click()

    try:
      element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "chkReadMessage")))
      if element:
        try:
          actions = ActionChains(driver)
          actions.move_to_element(element).perform()
          element.click()  # Click on the element directly (without find_element again)
        except Exception as e:
          print("Element with ID 'chkReadMessage' not found or not interactable within 10 seconds.")

        try:
          element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "enableClosedialog")))
          actions = ActionChains(driver)
          actions.move_to_element(element).perform()
          element.click()  # Click on the element directly (without find_element again)

        except Exception as e:
          element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CLASS_NAME, "enableClosedialog")))
          actions = ActionChains(driver)
          actions.move_to_element(element).perform()
          element.click()
          print("Element with ID 'chkReadMessage' not found or not interactable within 10 seconds.",e)
      else:
        print("Element with ID 'chkReadMessage' not found. Skipping actions.")
    except Exception as e:
      print("Element with ID 'chkReadMessage' not found or not interactable within 10 seconds.")

    driver.execute_script("window.scrollTo(0,90.4000015258789)")
    driver.execute_script("window.scrollTo(0,1744.800048828125)")
    driver.execute_script("window.scrollTo(0,1972.800048828125)")
    vars["window_handles"] =driver.window_handles
    try:
        element=WebDriverWait(driver,5).until(EC.presence_of_element_located((By.LINK_TEXT, "View All Announcements")))
        element.click()
    except:
      driver.quit()
    timeout=2
    time.sleep(round(timeout/1000))
    wh_now = driver.window_handles
    wh_then = vars['window_handles']
    if len(wh_now)>len(wh_then):
        vars["win8781"]=set(wh_now).difference(set(wh_then)).pop()

    driver.switch_to.window(vars["win8781"])
    driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_ddlSearchBy_Arrow").click()
    driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_ddlSearchBy_Input").send_keys("Uploaded By")
    time.sleep(3)
    try:
        element=WebDriverWait(driver,5).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".rcbHovered")))
        element.click()
    except:
        driver.quit()
    try:
        element=WebDriverWait(driver,5).until(EC.presence_of_element_located((By.ID,"ctl00_ContentPlaceHolder1_RadDatePicker1_popupButton")))
        element.click()
    except:
        driver.quit()
    today = date.today()
    y=today.strftime("%Y-%m-%d")
    x_path="//a[normalize-space()='"+y[-2:]+"']"


    # x_path="//a[normalize-space()='"+"18"+"']"
    try:
        element=WebDriverWait(driver,5).until(EC.presence_of_element_located((By.XPATH,x_path)))
        element.click()
    except:
        driver.quit()
    driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_RadComboBox1_Input").send_keys("Between")
    time.sleep(10)
    driver.find_element(By.ID, "ctl00_ContentPlaceHolder1_btnShow").click()
    cont=driver.page_source
    cont_html = bs(cont, "html.parser")
    # print(cont_html)
    commentboxes1 = cont_html.find_all('tr', {'class': "rgRow"})
    list1=[]
    for comment in commentboxes1:
      k=comment.text
      cleaned_text = re.sub(r"\s+", " ", k)
      cleaned_text = cleaned_text.replace("\xa0", " ")
      list1.append(cleaned_text)
      
    commentboxes2 = cont_html.find_all('tr', {'class': "rgAltRow"})
    for comment in commentboxes2:
      k=comment.text
      cleaned_text = re.sub(r"\s+", " ", k)
      cleaned_text = cleaned_text.replace("\xa0", " ")
      list1.append(cleaned_text)
    return jsonify(list1), 200
    
