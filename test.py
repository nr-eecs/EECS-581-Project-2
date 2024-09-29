

def a():
    try:
        b()
    except:
        print("lmao")

def b():
    for i in range(10):
        print("hi")
        raise Exception

a()