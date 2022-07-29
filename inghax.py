import cv2
import numpy as np
import easyocr
import base64
from pprint import pprint
import argparse
import ast # Only used for boolean eval. Try and replace later.

# Parameters syntax |  --home=Browser, --headless=True/False, --client=1337, --PIN=1111

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
    raise argparse.ArgumentTypeError('Client Number aka login/username! Must be a number.')

# Initialise input parsing
input = argparse.ArgumentParser(add_help=False)

# Required inputs
## Most currently using help parameter causing using custom functions to check inputs
input.add_argument('--browser', type=browserCheck, required=True)
input.add_argument('--headless', type=boolCheck, required=True)
input.add_argument('--client', type=int, required=True, help='Client Number aka login/username! Must be a number.')
input.add_argument('--PIN', type=PINcheck, required=True)

# All values get chucked in here
inputs = input.parse_args()


# SETTINGS
headless = inputs.headless
clientNumber = inputs.client
PIN = inputs.PIN
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

browser.get("https://ing.com.au/securebanking/")
# Awaiting load of URL
try:
    waiting = WebDriverWait(browser, 10)
    waiting.until(EC.presence_of_element_located((By.XPATH, """//*[@id="login-btn"]""")))
    print("We're in.")
except TimeoutException:
    print('Page no loading :( ')

def banner():
    print("""                                                                                                                                 
IIIIIIIIIINNNNNNNN        NNNNNNNN        GGGGGGGGGGGGGHHHHHHHHH     HHHHHHHHH               AAA               XXXXXXX       XXXXXXX
I::::::::IN:::::::N       N::::::N     GGG::::::::::::GH:::::::H     H:::::::H              A:::A              X:::::X       X:::::X
I::::::::IN::::::::N      N::::::N   GG:::::::::::::::GH:::::::H     H:::::::H             A:::::A             X:::::X       X:::::X
II::::::IIN:::::::::N     N::::::N  G:::::GGGGGGGG::::GHH::::::H     H::::::HH            A:::::::A            X::::::X     X::::::X
  I::::I  N::::::::::N    N::::::N G:::::G       GGGGGG  H:::::H     H:::::H             A:::::::::A           XXX:::::X   X:::::XXX
  I::::I  N:::::::::::N   N::::::NG:::::G                H:::::H     H:::::H            A:::::A:::::A             X:::::X X:::::X   
  I::::I  N:::::::N::::N  N::::::NG:::::G                H::::::HHHHH::::::H           A:::::A A:::::A             X:::::X:::::X    
  I::::I  N::::::N N::::N N::::::NG:::::G    GGGGGGGGGG  H:::::::::::::::::H          A:::::A   A:::::A             X:::::::::X     
  I::::I  N::::::N  N::::N:::::::NG:::::G    G::::::::G  H:::::::::::::::::H         A:::::A     A:::::A            X:::::::::X     
  I::::I  N::::::N   N:::::::::::NG:::::G    GGGGG::::G  H::::::HHHHH::::::H        A:::::AAAAAAAAA:::::A          X:::::X:::::X    
  I::::I  N::::::N    N::::::::::NG:::::G        G::::G  H:::::H     H:::::H       A:::::::::::::::::::::A        X:::::X X:::::X   
  I::::I  N::::::N     N:::::::::N G:::::G       G::::G  H:::::H     H:::::H      A:::::AAAAAAAAAAAAA:::::A    XXX:::::X   X:::::XXX
II::::::IIN::::::N      N::::::::N  G:::::GGGGGGGG::::GHH::::::H     H::::::HH   A:::::A             A:::::A   X::::::X     X::::::X
I::::::::IN::::::N       N:::::::N   GG:::::::::::::::GH:::::::H     H:::::::H  A:::::A               A:::::A  X:::::X       X:::::X
I::::::::IN::::::N        N::::::N     GGG::::::GGG:::GH:::::::H     H:::::::H A:::::A                 A:::::A X:::::X       X:::::X
IIIIIIIIIINNNNNNNN         NNNNNNN        GGGGGG   GGGGHHHHHHHHH     HHHHHHHHHAAAAAAA                   AAAAAAAXXXXXXX       XXXXXXX
""")
banner()


# Compares 0 on keypad to template.png
# EasyOCR cannot automatically detect a 0
# Similar to save function
def template_match(data):
    clean_base64 = base64.b64decode((str(data)))
    narray = np.frombuffer(clean_base64, np.uint8)
    img = cv2.imdecode(narray, cv2.IMREAD_ANYCOLOR)
    # Zero_image is what was found on the ING keypad
    # Generated at every runtime
    cv2.imwrite("Zero_image.png", img)
    zero = cv2.imread("Zero_image.png")
    template = cv2.imread("template.png")
    # OCR comparison done here
    # Res returns with a probability in a np array
    res = cv2.matchTemplate(zero, template, cv2.TM_CCOEFF_NORMED)
    if res >= 0.60:
        print("Probs 0")
        return "0"
    else:
        print("WTF")
        return 1

# Bulk of determining what keys are what happens here
def save(encoded_data, file):
    clean_base64 = base64.b64decode((str(encoded_data)))
    narray = np.frombuffer(clean_base64, np.uint8)
    img = cv2.imdecode(narray, cv2.IMREAD_ANYCOLOR)
    # Writes img file from base64 encode
    cv2.imwrite(file, img)
    # Reader (OCR) analyses the img file just created
    result = reader.readtext(file)
    try:
        value = result[-0][1]
        # print("Digit: {0}".format(value))
        # print("Base64: {0}".format(encoded_data))
        lukeisafucboi[value] = encoded_data
    # Catching invalid slices because result was empty (ie. OCR couldn't determine keypad number)
    except IndexError:
        # The base64 encodes that couldn't be solved get sent for specialist template matching
        value2 = template_match(encoded_data)
        if value2 == "0":
            # Input the determined 0 keypad into existing dictionary
            lukeisafucboi[value2] = encoded_data



# Finds and inputs Client Number into field (just plain text input here)
#table = browser.find_element_by_xpath("""//*[@id="cifField"]""")
#print(table)
browser.find_element_by_id("cifField").clear()
browser.find_element_by_id("cifField").send_keys(str(clientNumber))

# Grabs all base64 imgs that makeup the ING keypad
digitpanel = browser.find_element_by_xpath("""//*[@id="keypad"]""")
keypad = digitpanel.find_element_by_class_name("module-keypad")
# Find and store location of login btn for later
login_button = browser.find_element_by_xpath("""//*[@id="login-btn"]""") # also used for 'waiting'
ing_values = {}
keypad_digits = {}

# Dictionary pairing OCR'd digits and its corresponding base64 from the webpage
lukeisafucboi = {}
# Dictionary pairing base64 with its div location that it was found in
## Div location is just the index representing its nesting, within Selenium (not webpage)
lukehasmallpp = {}

# The OCR system that does the heavy lifting
reader = easyocr.Reader(['en'])


# 1, 4  div elements = 0 isnt in the elements. - I am god.
for i in range(0, 5):
    for j in range(0, 5):
        # Iterate through keypad digits
        for key_num in keypad.find_elements_by_xpath("""//*[@id="keypad"]/div/div[{}]/div[{}]/div/img""".format(j, i)):
            # Src is where the base64 is stored on the page
            digits = key_num.get_attribute("src")
            ing_values = digits
            #print(ing_values[22:])
            test_vales = ing_values[22:]
            # Store each key's base64 and corresponding div location for later
            lukehasmallpp[test_vales] = (j, i)
            save(test_vales, "testfile{0}.png".format(i))

# Dictionary pairing base64 w/ its location
# Made by comparing lukeisafucboi & lukehasmallpp to determined keypaid location for desired PIN
listy = []

# Iterate through dictionary of determined digits and dictionary of known location
# to find locations of PIN's numbers
for senpaiLukas in list(PIN):
    imgString = lukeisafucboi[senpaiLukas]
    listy.append([imgString, lukehasmallpp[imgString]])

# Click each keypad button, drawing from determined list
for i in listy:
    nums = i[1]
    position = keypad.find_elements_by_xpath("""//*[@id="keypad"]/div/div[{}]/div[{}]/div/img""".format(nums[0], nums[1]))[0]
    position.click()

try:
    waiting = WebDriverWait(browser, 10)
    waiting.until(EC.presence_of_element_located((By.XPATH, """//*[@id="login-btn"]""")))
    print("Into the mainframe...")
except TimeoutException:
    print('Cannot login :( ')
login_button.click()