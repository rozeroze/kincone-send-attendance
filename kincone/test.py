import kincone as k


def test_xxx():
    pass

def test_load_userconf():
    k.load_userconf()
    print("email:", k.email)
    print("password:", k.password)

def test_load_attendances():
    k.load_attendances()
    for attendance in k.attendances:
        print(attendance)

if __name__ == '__main__':
    test_xxx()
    print("log: test_load_userconf()")
    test_load_userconf()
    print("log: test_load_attendances()")
    test_load_attendances()

