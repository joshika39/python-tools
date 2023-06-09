from somepackage import testclass

if __name__ == "__main__":
    
    while True:
        input("Press any key to continue")
        test = testclass.Test()
        test.reload()
        print(test.calc())