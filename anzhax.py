# Only used for boolean eval. Try and replace later.
import argparse, ast


# Parameters syntax |  --home=Browser, --headless=True/False, --CRN=1337, --Pass=1111

# Checks if input is string because argparse can't directly do this
def stringOnly(x):
    try:
        int(x)
    except ValueError:
        return x
    raise argparse.ArgumentTypeError('No numbers allowed!')

# Ensuring length is =4. Assuming non-int will be caught too.
def PINcheck(x):
    if len(x) > 4 or len(x) < 4:
        raise argparse.ArgumentTypeError('Four exact numbers only, sweetie.')
    return x

def browserCheck(x):
    browerList = ['Firefox', 'Chrome']
    # if x != 'Firefox' or 'Chrome':
    if x not in browerList:
        raise argparse.ArgumentTypeError('Only type Firefox/Chrome m8, first-caps no typos.')
        # return x
    else:
        stringOnly(x)
        return x

def boolCheck(x):
    try:
        return ast.literal_eval(x)
    except ValueError:
        return x
    raise argparse.ArgumentTypeError('Keep it True or False!')

def intCheck(x):
    print(x)
    print(type(x))
    try:
        int(x)
    except ValueError:
        return x
    raise argparse.ArgumentTypeError('CRN aka login/username! Must be a number.')

# Initialise input parsing
input = argparse.ArgumentParser(add_help=False)

# Required inputs
## Most currently using help parameter causing using custom functions to check inputs
input.add_argument('--browser', type=browserCheck, required=True)
input.add_argument('--headless', type=boolCheck, required=True)
input.add_argument('--CRN', type=int, required=True, help='CRN Number aka login/username! Must be a number.')
input.add_argument('--Password', type=stringOnly, required=True)

# All values get chucked in here
inputs = input.parse_args()


# SETTINGS
headless = inputs.headless
CRN = str(inputs.CRN)
Password = inputs.Password
# Yes, I need to sort out the switching between int and str

# Importing the correct stuff based on browser
if inputs.browser == 'Firefox':   # M A S T E R R A C E
    from selenium.webdriver import Firefox
    from selenium.webdriver.firefox.options import Options
    opts = Options()
    if headless == True:
        opts.add_argument("--headless")
    #opts.add_argument("--headless")
    browser = Firefox(options=opts)
else:  # Yeah I can probs fix how I'm asking for input since one name is redundant. Already checking input earlier up
    from selenium.webdriver import Chrome
    from selenium.webdriver.chrome.options import Options
    opts = Options()
    if headless == True:
        opts.add_argument("--headless")
    #opts.add_argument("--headless")
    browser = Chrome(options=opts)
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

browser.get("https://www.anz.com/INETBANK/login.asp")
# Awaiting load of URL
try:
    waiting = WebDriverWait(browser, 10)
    waiting.until(EC.presence_of_element_located((By.XPATH, """//*[@id="SignonButton"]""")))
    print("We're in.")
except TimeoutException:
    print('Page no loading :( ')


# Inputting CRN into field
browser.find_element_by_xpath("""//*[@id="crn"]""").clear()
browser.find_element_by_xpath("""//*[@id="crn"]""").send_keys(CRN)

# Inputting Password into field
browser.find_element_by_xpath("""//*[@id="Password"]""").clear()
browser.find_element_by_xpath("""//*[@id="Password"]""").send_keys(Password)

# Submit fields a la Login
browser.find_element_by_xpath("""//*[@id="SignonButton"]""").click()
print('Done!')