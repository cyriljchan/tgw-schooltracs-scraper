# Scrape SchoolTracs for student enrollment records
# 'https://my.schooltracs.com/app/login'

from datetime import datetime
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
    
    def change_branch(self):
        os.system("cls")
        branches = {"1":"Happy Valley", "2":"Taikoo", "3":"Whampoa"}
        print("Change Branch")
        print("Branches:")
        for key, branch in branches.items():
            print(f"[{ key }] { branch }")
        choice = input("Choose an option [1,2,3] then press [ENTER] ")
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@class='x-form-text x-form-field x-trigger-noedit']"))).click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, f"//div[contains(text(), '{ branches[choice] }')]"))).click()
        self.headers["branch"] = driver.find_element(By.XPATH, "//input[@class='x-form-text x-form-field x-trigger-noedit']").get_attribute("value")
        
        body = driver.find_element(By.TAG_NAME, "body")
        while "x-body-masked" in body.get_attribute("class"):
            pass

    def change_date(self):
        os.system("cls")
        print("Change Date")
        date = input("Input date (YYYY-MM-DD) then press [ENTER] ")
        date_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='dateInput']")))
        date_input.clear()
        date_input.send_keys(date)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@class=' x-btn-text st-tb-left']"))).click()
        WebDriverWait(driver, 10).until(EC.invisibility_of_element((By.XPATH, "//div[@class='ext-el-mask']")))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@class=' x-btn-text st-tb-right']"))).click()
        date = driver.find_element(By.XPATH, "//input[@name='dateInput']").get_attribute("value")
        self.headers["date"] = datetime.strptime(date, '%d/%m/%Y').strftime('%Y-%m-%d')


class SchoolTracsMain(SchoolTracsFuncs):
    def __init__(self) -> None:
        self.headers = {"branch":"", "date":""}

    def timetable_menu(self):
        os.system("cls")
        timetable_btn = driver.find_element(By.XPATH, "//*[contains(text(), 'Timetable')]")
        driver.execute_script("arguments[0].click()", timetable_btn)
        self.headers["branch"] = driver.find_elements(By.XPATH, "//input[@class='x-form-text x-form-field x-trigger-noedit']")[0].get_attribute("value")
        date = driver.find_element(By.XPATH, "//input[@name='dateInput']").get_attribute("value")
        self.headers["date"] = datetime.strptime(date, '%d/%m/%Y').strftime('%Y-%m-%d')
        instructor = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, "//span[@title='Instructor']"))).text

        print(f"""Hello, { instructor } \n""")
        print(f"Branch: { self.headers['branch'] }")
        print(f"Date: { self.headers['date'] }")
        print(f"[1] View Schedule ({ self.headers['date'] })")
        print(f"[2] View Schedule with Remarks/Activities ({ self.headers['date'] })")
        print(f"[3] Change Branch")
        print(f"[4] Change Date")
        print(f"[0] Logout")
        choice = input("Choose an option [1,2,3,4,0] then press [ENTER] ")

        if choice == "0":
            driver.find_element(By.XPATH, "//button[@class=' x-btn-text st-icon-logout']").click()
            self.main_menu("Logged out.")

        elif choice == "1":
            # TODO: extract timetable information
            pass
        elif choice == "2":
            # TODO: extract timetable information and student remarks
            pass
        elif choice == "3":
            self.change_branch()
            self.timetable_menu()
        elif choice == "4":
            self.change_date()
            self.timetable_menu()
        else:
            self.timetable_menu()

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