import kincone as k
from selenium import webdriver
from selenium.webdriver.firefox.options import Options


def test_xxx():
    print("log: test_xxx() called")

def test_load_userconf():
    print("log: test_load_userconf() called")
    k.load_userconf()
    print("log: email ->", k.email)
    print("log: password ->", k.password)

def test_load_attendances():
    print("log: test_load_attendances() called")
    k.load_attendances()
    for attendance in k.attendances:
        print("log: data ->", attendance)

def test_webdriver():
    print("log: test_webdriver() called")
    try:
        print("log: make object 'opt'")
        opt = Options()
        print("log: add argument to 'opt', -headless")
        opt.add_argument('-headless')
        print("log: make webdriver with firefox")
        driver = webdriver.Firefox(options=opt)
    except Exception as e:
        print("log: error occurred.", e)
    finally:
        print("log: webdriver close")
        driver.quit()

if __name__ == '__main__':
    test_xxx()
    test_load_userconf()
    test_load_attendances()
    test_webdriver()

