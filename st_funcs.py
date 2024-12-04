import re
import time
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.remote.webdriver import WebDriver


def check_element_exists(driver, by, xpath):
    try:
        driver.find_element(by, xpath)
    except NoSuchElementException:
        return False
    return True


# Opens the SchoolTracs timetable to the specified date and branch
def open_timetable(driver: WebDriver, timetable: dict) -> None:
    """
    Opens the SchoolTracs timetable to the specified branch and date

    Parameters
    ----------
    driver : WebDriver
        webdriver used to access the SchoolTracs website
    timetable : dict
        dict containing the branch and date

    Returns
    -------
    None
    """

    if driver == None:
        return "No WebDriver found."

    # Open timetable
    driver.find_element(By.XPATH, "//*[contains(text(), 'Timetable')]").click()
    print("Opening timetable...")

    # Select branch
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[contains(@id, 'ext-comp-1002')]"))).click()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, f"//div[contains(text(), '{ timetable['branch'] }')]"))).click()
    timetable["branch"] = driver.find_element(By.XPATH, "//input[contains(@id, 'ext-comp-1002')]").get_attribute("value")
    print(f"Branch: { timetable['branch'] }")

    # Wait for page to load
    body = driver.find_element(By.TAG_NAME, "body")
    while "x-body-masked" in body.get_attribute("class"):
        pass

    # Select date
    date_input = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@name='dateInput']")))
    date_input.clear()
    date_input.send_keys(timetable["date"])
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@class=' x-btn-text st-tb-left']"))).click()
    WebDriverWait(driver, 10).until(EC.invisibility_of_element((By.XPATH, "//div[@class='ext-el-mask']")))
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[@class=' x-btn-text st-tb-right']"))).click()
    date = driver.find_element(By.XPATH, "//input[@name='dateInput']").get_attribute("value")
    timetable["date"] = datetime.strptime(date, '%d/%m/%Y').strftime('%Y-%m-%d')
    print(f"Date: { timetable['date'] }")

    # Wait table to load
    WebDriverWait(driver, 10).until(EC.invisibility_of_element((By.XPATH, "//div[@class='ext-el-mask']")))


# Returns a list of student dicts containing their act-box, name, act-name, timeslot, and teacher.
def get_students(driver: WebDriver, timetable: dict) -> list[dict]:
    """
    Returns a list of students found on the SchoolTracs timetable

    Parameters
    ----------
    driver : WebDriver
        webdriver used to access the SchoolTracs website
    timetable : dict
        dict containing the branch and date

    Returns
    -------
    students : list[dict]
        a list of students (dict)
    """

    if driver == None:
        return "No WebDriver found."
    print("Scanning timetable...")

    # Get all non-0/0 courses
    activities = []
    result = WebDriverWait(driver, 5).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='act-box']")))
    for activity in result:
        if "0/0" not in activity.get_attribute("textContent"):
            activities.append(activity)

    # Create student dict using timetable information (course, timeslot, instructor, name)
    students = []
    for activity in activities:
        for customer in activity.find_element(By.XPATH, ".//div[@class='customers']").find_elements(By.XPATH, ".//div"):
            if "line-through" not in customer.find_element(By.XPATH, ".//span[@class='name']").get_attribute("style"):
                student = {
                    "act-name": activity.find_element(By.XPATH, ".//div[@class='act-name']").text,
                    "name": (re.sub("\\(.*?\\)", "", customer.find_element(By.XPATH, ".//span[@class='name']").text)).strip(),
                    "time": activity.find_element(By.XPATH, ".//div[@class='time']").text,
                    "teacher": activity.find_element(By.XPATH, ".//div[@class='resource'][@style='']").text if check_element_exists(activity, By.CLASS_NAME, "resource") else "",
                    "prev_remarks": []
                }
                students.append(student)
    print("List of students created.")

    # Get each student's activity information
    for student in students:
        print(f"Obtaining student details ({ students.index(student) + 1 }/{ len(students) })")

        # Skip non-regular students
        if student['act-name'] not in "ENGBCROBMC STEMGMRobloxScratchSSL":
            continue

        # Open student details
        act_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//span[contains(text(), '{ student['name'] }')]/ancestor::div[@class='act-box']")))
        driver.execute_script("arguments[0].click();", act_box)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//a[contains(text(), '{ student['name'] }')]"))).click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, f"//label[contains(text(), '{ student['name'] }')]")))
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//button[contains(text(), 'Detail')]"))).click()

        # Open student activities (the popup window)
        enrollmentrecords = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, f"//span[contains(text(), 'Enrollment Records')]")))
        driver.execute_script("arguments[0].click();", enrollmentrecords)
        time.sleep(5)

        # Extract last known activity
        date_list = driver.find_elements(By.XPATH, f"""//div[contains(@class, 'x-grid3-col-date') and contains(text(), '{ timetable['date'] }')]
                                                                                                    //ancestor::div[contains(@class, 'x-grid3-row')]
                                                                                                    //following-sibling::div""")
        for date_row in date_list:
            name = date_row.find_element(By.XPATH, ".//div[contains(@class, 'x-grid3-col-name')]").text
            date = date_row.find_element(By.XPATH, ".//div[contains(@class, 'x-grid3-col-date')]").text
            remark = date_row.find_element(By.XPATH, ".//div[contains(@class, 'x-grid3-col-remark')]").text
            attendance = date_row.find_element(By.XPATH, ".//div[contains(@class, 'x-grid3-col-attendance')]").text
            
            if name != student['act-name']:
                continue

            if date == timetable["date"]:
                continue
            
            if attendance == "Present":
                student['prev_remarks'].append((date, remark))
                break
            student['prev_remarks'].append((date, remark))
     
        # Close popup        
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//div[@class=' x-window x-resizable-pinned']//descendant::div[@class='x-tool x-tool-close']"))).click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Timetable')]"))).click()
        
    return students