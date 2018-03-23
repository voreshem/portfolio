import os
import platform
from mpmath import mp

digits = input("How many digits shall I compute?\n")

def pyCalc(digits):
    mp.dps = digits
    return str(mp.pi)
if __name__ == '__main__':
    pi_digits = pyCalc(digits)
    f = open("pi_digits.txt", 'a')
    f.write(pi_digits + '\n'*2)
    f.close()
    if platform.system() == 'Windows':
        os.startfile(os.path.realpath(f.name))
    elif platform.system() == 'Darwin':
        os.popen("open " + os.path.realpath(f.name))
    elif platform.system() == 'Linux':
        os.popen("xdg-open " + os.path.realpath(f.name))
