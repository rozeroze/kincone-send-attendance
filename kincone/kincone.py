import sys
import csv
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

LOGIN_URL = "https://kincone.com/auth/login"
LOGOUT_URL = "https://kincone.com/auth/logout"
CONFIGFILE = "/kincone/.kincone.user"
ATTENDANCEFILE = "/kincone/attendance.csv"
SCREENSHOT = "/kincone/snap/"
TITLES = ["編集済みです"]

class Browser:
    driver = None
    def __init__(self):
        pass
    def open():
        pass

class Attendance:
    def data_load(self, data):
        self.overwrite = data[0]
        self.date = data[1]
        self.start_hours = data[2]
        self.end_hours = data[3]
        self.outing_out_hours = data[4]
        self.outing_in_hours = data[5]
        self.note = data[6]
    def set_id(self, data_id):
        self.id = data_id

# test
#with open(ATTENDANCEFILE, mode="r") as f:
#    reader = csv.reader(f)
#    lines = [row for row in reader]
#    for row in lines[1:]: # out of header
#        atn = Attendance()
#        atn.data_load(row)
#        print(atn.overwrite, atn.date, atn.start_hours, atn.end_hours, atn.outing_out_hours, atn.outing_in_hours, atn.note)
#sys.exit()

OPT = Options()
OPT.add_argument('-headless')

with open(CONFIGFILE, mode = "r") as f:
    lines = f.read().splitlines()
    for line in lines:
        [lhs, rhs] = line.split("=")
        if lhs == "email":
            email = rhs
        elif lhs == "password":
            password = rhs

# test
#print("email: " + email)
#print("password: " + password)
#sys.exit()

def get_current_window_size(driver):
    print("log: call get_current_window_size(driver)")
    w = driver.execute_script('return document.body.scrollWidth')
    h = driver.execute_script('return document.body.scrollHeight')
    driver.set_window_size(w, h)

def make_snap(driver, name):
    print("log: call make_snap(driver, name)")
    driver.save_screenshot(SCREENSHOT + name)
    print("log: -> " + SCREENSHOT + name)

def kincone_open(driver):
    print("log: call kicone_open(driver)")
    driver.get(LOGIN_URL)

def kincone_login(driver):
    print("log: call kincone_login(driver)")
    form = driver.find_element_by_css_selector("#content > div.container > div > div > div.col-sm-4.col-sm-offset-4 > div > form")
    form.find_element_by_id("email").send_keys(email)
    form.find_element_by_id("password").send_keys(password)
    form.find_element_by_css_selector("div.clearfix.form-group > div.pull-right > input").click()

def kincone_logout(driver):
    print("log: call kincone_logout(driver)")
    driver.get(LOGOUT_URL)

def kincone_get_data_id(driver, attendance):
    print("log: call kincone_get_data_id(driver, attendance)")
    row_id = "attendance-row-{0}".format(attendance.date)
    data_id = driver.find_element_by_css_selector("#{0} .delete-button".format(row_id)).get_attribute("data-id")
    return data_id

def kincone_is_data_exists(driver, attendance):
    print("log: call kincone_is_data_exists(driver, attendance)")
    row_id = "attendance-row-{0}".format(attendance.date)
    title = driver.find_element_by_id(row_id).get_attribute("title")
    for t in TITLES:
        if t == title:
            return True
    return False

def kincone_remove_attendance(driver, attendance):
    print("log: call kincone_remove_attendance(driver, attendance)")
    # display remove-dialog
    row_id = "attendance-row-{0}".format(attendance.date)
    #driver.execute_script("document.querySelector('#{0}').scrollIntoView()".format(row_id))
    #driver.find_element_by_css_selector("#{0} .delete-button".format(row_id)).click()
    driver.execute_script("document.querySelector('#{0} .delete-button').click()".format(row_id))
    time.sleep(5)
    make_snap(driver, "open-remove-dialog.png")
    # send delete
    form = driver.find_element_by_css_selector("#content > div.container > div > div.modal.fade.bs-delete-modal-sm > div > div > div.modal-footer > form")
    #form.find_element_by_id("id").send_keys(attendance.id)
    form.submit()
    time.sleep(5)

def kincone_open_attendance(driver, attendance):
    print("log: call kincone_open_attendance(driver, attendance)")
    url = "https://kincone.com/attendance/edit/{0}".format(attendance.id)
    print("log: in-edit: open url -> {0}".format(url))
    driver.get(url)

# hour
def kincone_edit_attendance_hour(driver, attendance):
    print("log: call kincone_edit_attendance_hour(driver, attendance)")
    driver.find_element_by_id("start_hours").send_keys(attendance.start_hours)
    driver.find_element_by_css_selector("#outings > button").click()
    driver.find_element_by_id("out_hours_0").send_keys(attendance.outing_out_hours)
    driver.find_element_by_id("in_hours_0").send_keys(attendance.outing_in_hours)
    driver.find_element_by_id("end_hours").send_keys(attendance.end_hours)

# flag
def kincone_edit_attendance_flags(driver, attendance):
    print("log: call kincone_edit_attendance_flags(driver, attendance)")
    # note: be all checkboxes out
    section = driver.find_element_by_css_selector("#form-attendance-edit > div:nth-child(7)")
    checkboxes = section.find_elements_by_css_selector("input[type=checkbox]:checked")
    for checkbox in checkboxes:
        checkbox.click()

# note
def kincone_edit_attendance_note(driver, attendance):
    print("log: call kincone_edit_attendance_note(driver, attendance)")
    driver.find_element_by_id("note").send_keys(attendance.note)

# submit
def kincone_submit_attendance(driver, attendance):
    print("log: call kincone_submit_attendance(driver, attendance)")
    # edit-page submit ( to confirm-page )
    driver.find_element_by_css_selector("#form-attendance-edit > div:nth-child(11) > div:nth-child(2) > button").click()
    # confirm-page submit
    driver.find_element_by_css_selector("#form-attendance-confirm > div:nth-child(13) > div:nth-child(2) > button").click()

def kincone_edit_attendance(driver, attendance):
    print("log: call kincone_edit_attendance(driver, attendance)")
    try:
        #driver = webdriver.Firefox(options=OPT)
        atndriver = driver
        print("log: in-edit: webdriver start")
        kincone_open_attendance(atndriver, attendance)
        make_snap(atndriver, "attendance-{0}-opened.png".format(attendance.date))
        kincone_edit_attendance_hour(atndriver, attendance)
        kincone_edit_attendance_flags(atndriver, attendance)
        kincone_edit_attendance_note(atndriver, attendance)
        make_snap(atndriver, "attendance-{0}-pre-submit.png".format(attendance.date))
        kincone_submit_attendance(atndriver, attendance)
        make_snap(atndriver, "attendance-{0}-post-submit.png".format(attendance.date))
    except Exception as e:
        print(e)
    finally:
        atndriver.quit()
        print("log: in-edit: webdriver quit")

def main():
    print("log: call main()")
    try:
        driver = webdriver.Firefox(options=OPT)
        print("log: webdriver start")
        driver.implicitly_wait(10)
        print("log: webdriver set implicitly_wait -> 10")
        kincone_open(driver)
        get_current_window_size(driver)
        kincone_login(driver)
        make_snap(driver, "login.png")
        with open(ATTENDANCEFILE, mode="r") as f:
            print("log: attendance file open")
            reader = csv.reader(f)
            lines = [row for row in reader]
            for row in lines[1:]: # no-header
                print("log: data ->", row)
                atn = Attendance()
                atn.data_load(row)
                data_id = kincone_get_data_id(driver, atn)
                print("log: id ->", data_id)
                atn.set_id(data_id)
                if (atn.overwrite == "1" and kincone_is_data_exists(driver, atn)):
                    print("log: overwrite is true and data exists, try remove")
                    kincone_remove_attendance(driver, atn)
                kincone_edit_attendance(driver, atn)
                break # test: one-pattern
        print("log: attendance file close")
        kincone_logout(driver)
        make_snap(driver, "logout.png")
    except Exception as e:
        print(e)
    finally:
        driver.quit()
        print("log: webdriver quit")

if __name__ == '__main__':
    main()
