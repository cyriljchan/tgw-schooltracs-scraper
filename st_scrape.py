# Scrape SchoolTracs for student enrollment records
# 'https://my.schooltracs.com/app/login'

import getpass
import os, sys
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


options = Options()
options.add_argument("--headless")
url = "https://my.schooltracs.com/app/login"
driver = webdriver.Firefox(options=options)
driver.get(url)


class SchoolTracsFuncs:
    def login(self) -> None:
        print("Please enter login credentials.")

        login_msg = WebDriverWait(driver,10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "st-login-msg")))
        username = WebDriverWait(driver,10).until(EC.visibility_of_any_elements_located((By.ID, "username")))
        password = WebDriverWait(driver,10).until(EC.visibility_of_any_elements_located((By.ID, "password")))
        login_button = WebDriverWait(driver,10).until(EC.visibility_of_any_elements_located((By.ID, "login-btn")))
        
        driver.execute_script("arguments[0].innerHTML = '';", login_msg[0])
        driver.execute_script("arguments[0].innerHTML = '';", login_msg[-1])
        username[-1].clear()
        password[-1].clear()
        username[-1].send_keys(input("Login ID: "))
        password[-1].send_keys(getpass.getpass())
        driver.execute_script("arguments[0].click();", login_button[-1])

        try:
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), 'Invalid')]")))
            return False
        except:
            print("Logging in...")
            return True



class SchoolTracsMain(SchoolTracsFuncs):
    def timetable_menu(self):
        # TODO: open timetable and print selectible functions
        pass

    def main_menu(self, msg=None):
        os.system("cls")
        if msg:
            print(msg)
        print("TGW SchoolTracs Scraper")
        print("[1] Login")
        print("[0] Exit")
        choice = input("Choose an option [1,0] then press [ENTER] ")

        if choice == "0":
            os.system("cls")
            driver.close()
            sys.exit()
        
        elif choice == "1":
            os.system("cls")
            login = self.login()
            if login:
                self.timetable_menu()
            else:
                self.main_menu("Invalid login or password.")
        
        else:
            os.system("cls")
            self.main_menu()

st_scrape = SchoolTracsMain()
st_scrape.main_menu()