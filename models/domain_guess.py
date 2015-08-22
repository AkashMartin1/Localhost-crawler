import string
from time import sleep


class DomainGuess:
    def __init__(self):
        pass

    def do(self):
        domain_extension = ["com", "us", "in", "net", "co", "cc", "ru"]
        str = string.lowercase
        domain = ""
        while True:
            for ii in range(0, 26):
                if len(str) >= 2:
                    domain += (str[ii])
                    print(domain)
                    sleep(1)
                    print("Sleeping.......")
                else:
                    for iii in range(0, 26):
                        domain += (str[ii] + str[iii])
                        print(domain)
                        sleep(1)
                        print("Sleeping.......")

DomainGuess().do()
