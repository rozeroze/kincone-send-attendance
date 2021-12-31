import kincone as k


def test_xxx():
    pass

def test_open_userconf():
    k.load_userconf()
    print("email:", k.email)
    print("password:", k.password)


if __name__ == '__main__':
    test_xxx()
    test_open_userconf()

