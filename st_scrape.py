# Scrape SchoolTracs for student enrollment records
# 'https://my.schooltracs.com/app/login'

import getpass
import os, sys
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


options = Options()
options.add_argument("--headless")
url = "https://my.schooltracs.com/app/login"
driver = webdriver.Firefox(options=options)
driver.get(url)


class SchoolTracsFuncs:
    def login(self) -> None:
        # TODO: login funcationality
        pass


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