### Calculate Debt ###

# for CLI
import os
import colorama as color

# for doing polynomial regression on debt guidelines,
# to approximate a given loan's suggested enrollment debt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures

class GuideLines(object):
    """
    Creates & calculates the appropriate enrollment balance guidelines,
    based on the guidelines, which are manually-stored in this class definition
    """
    def __init__(self):
        pass        
        
    def get_enrollment_bal(Loan):
        
        interest = Loan.interest
        principal = Loan.loan

        if interest == 'low':
            if principal >= 1000:
                enrollment_bal = principal*2
                return enrollment_bal
            else:
                principal_list = [300,400,500,600,700,800,900,1000,1300,1500,2000]
                balance_list = [900,1000,1300,1500,1600,1700,1900,2000,2600,3000,4000]

        elif interest == 'high':
            if principal > 2000:
                enrollment_bal = principal*3
                return enrollment_bal
            else:
                principal_list = [300,400,500,600,700,800,900,1000,1300,1500,2000]
                balance_list = [1200,1600,2000,2200,2400,2600,2800,3000,3500,4000,5000]

        data = dict(zip(principal_list, balance_list))
        
        if Loan.loan in data.keys():
            enrollment_bal = data[Loan.loan]
        else:
            df = pd.DataFrame(data.items())
            x = df[0].values.reshape(-1,1)
            y = df[1].values.reshape(-1,1)

            x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)
            poly_reg = PolynomialFeatures(degree=6)
            x_poly = poly_reg.fit_transform(x)
            pol_reg = LinearRegression()
            pol_reg.fit(x_poly, y)

            enrollment_bal = round(int(pol_reg.predict(poly_reg.fit_transform([[principal]]))), -2)

        return enrollment_bal


class Loan(object):
    """
    Creates an object that represents a payday/installment loan
    """
    def __init__(self):
        self.lender = str()
        self.loan = int()
        self.bal = int()
        self.interest = str()
        self.pay = int()
        self.freq = str()
        self.w = int()
        self.b = int()
        self.s = int()
        self.m = int()

    def set(self):
        self.lender = input(f"\n Enter {light_cyan}lender{reset_color} name:\n\n")
        self.loan = int(input(f"\n Enter {light_yellow}loan{reset_color} amount:\n\n"))
        self.interest = input(f"\n Enter {light_red}interest{reset_color} level (high/low):\n\n")
        self.pay = int(input(f"\n Enter {light_red}payment{reset_color} amount:\n\n"))
        self.freq = input(f"\n Enter payment {light_cyan}frequency{reset_color} (w/b/s/m):\n\n")

        if self.freq == 'w':
            self.w = self.pay
            self.b = self.pay*2
            self.s = round(((self.pay*365)/84)/2)
            self.m = round((self.pay*365)/84)

        elif self.freq == 'b':
            self.w = round(self.pay/2)
            self.b = self.pay
            self.s = round((365*self.pay)/336)
            self.m = round((365*self.pay)/168)

        elif self.freq == 's':
            self.w = round((168/365)*self.pay)
            self.b = round((336/365)*self.pay)
            self.s = self.pay
            self.m = self.pay*2

        elif self.freq == 'm':
            self.w = round((84/365)*self.pay)
            self.b = round((168*self.pay)/365)
            self.s = round(self.pay/2)
            self.m = self.pay

        self.pays = f'{self.lender} {self.w}w {self.b}b {self.s}s {self.m}m'
        
        self.bal = GuideLines.get_enrollment_bal(self)

        loans.append(self)

    def print(self):
        print(f" {self.lender}\n {self.loan}\n {self.pay}{self.freq}")

class Debt(object):
    '''
    Creates an object that represents a person's payday/installment loan debt
    '''
    def __init__(self):
        self.loans = list()
        self.w = int()
        self.b = int()
        self.s = int()
        self.m = int()

        self.lenders = list()
        self.pays = str()
        self.debt = int()

    def set(self):
        self.loans = loans
        self.w = sum([loan.w for loan in loans])
        self.b = sum([loan.b for loan in loans])
        self.s = sum([loan.s for loan in loans])
        self.m = sum([loan.m for loan in loans])

        self.debt = sum([loan.bal for loan in loans])

        self.lenders = [loan.lender for loan in loans]
        self.num = len(self.lenders)
        self.pays = f'Paying:\n {light_red + str(self.w)}{light_cyan}w{reset_color} {light_red + str(self.b)}{light_cyan}b{reset_color} {light_red + str(self.s)}{light_cyan}s{reset_color} {light_red + str(self.m)}{light_cyan}m{reset_color}'

    def print(self):
        clear()
        for Loan in self.loans:
            print(f'\n {d.lenders.index(Loan.lender) + 1})\n {light_cyan + Loan.lender} {light_red + str(Loan.pay)}{light_cyan + Loan.freq} {light_red + Loan.interest}\n {light_yellow + str(Loan.loan)}    {light_green + str(Loan.bal) + reset_color}')
            print(f' {Loan.w}{light_cyan}w{reset_color} {Loan.b}{light_cyan}b{reset_color} {Loan.s}{light_cyan}s{reset_color} {Loan.m}{light_cyan}m{reset_color}')
        print(f'\n\n {self.pays}')
        print(f'\n Enrollment Debt:\n {light_green + str(self.debt)}{reset_color}\n')
        
def new():
    Loan.set(Loan())
    d.set()
    d.print()

def rm():
    d.print()
    loan_num = int(input(f"\n Which loan would you like to delete?\n\n Enter the loan's number:\n {range(d.num)[0]+1} - {range(d.num)[-1]+1}\n\n ")) - 1
    del d.loans[loan_num]
    d.set()
    d.print()

def clear():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

if __name__ == '__main__':

    # CLI text colors
    reset_color = color.Style.RESET_ALL
    light_cyan = color.Fore.LIGHTCYAN_EX
    light_red = color.Fore.LIGHTRED_EX
    light_green = color.Fore.LIGHTGREEN_EX
    light_yellow = color.Fore.LIGHTYELLOW_EX

    loans = []
    d = Debt()

    run = True
    clear()

    while run == True:
        response = input(f'\n What would you like to do ({light_cyan}a{reset_color}/{light_cyan}d{reset_color}/{light_cyan}r{reset_color}/{light_cyan}del{reset_color}/{light_cyan}q{reset_color})?'+
            f'\n\n {light_cyan}a{reset_color}: add debt'+
            f'\n {light_cyan}d{reset_color}: display debt'+
            f'\n {light_cyan}r{reset_color}: reset'+
            f'\n {light_cyan}del{reset_color}: delete'+
            f'\n {light_cyan}q{reset_color}: quit'+
            '\n\n ')
        if response == 'a':
            new()
        elif response == 'd':
            d.print()
        elif response == 'r':
            loans = []
            d = Debt()
            clear()
        elif response == 'del':
            if len(d.loans) > 0:
                rm()
            else:
                print("\n\n ...there are no loans to delete!")
        elif response == 'q':
            clear()
            run = False