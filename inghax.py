import time
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options
import cv2
import numpy as np
import easyocr
import base64
from pprint import pprint

# SETTINGS
headless = False
clientNumber = "1337"
PIN = "1111"
opts = Options()

if headless == True:
    opts.add_argument("--headless")
    browser = Firefox(options=opts)
else:
    opts = Options()
    browser = Firefox()

browser.get("https://ing.com.au/securebanking/")

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

# Nathan is a cuck.

def template_match(data):
    #print(data)
    clean_base64 = base64.b64decode((str(data)))
    narray = np.frombuffer(clean_base64, np.uint8)
    img = cv2.imdecode(narray, cv2.IMREAD_ANYCOLOR)
    cv2.imwrite("Zero_image.png", img)
    zero = cv2.imread("Zero_image.png")
    template = cv2.imread("template.png")
    res = cv2.matchTemplate(zero, template, cv2.TM_CCOEFF_NORMED)
    print(res)
    print(type(res))
    if res >= 0.60:
        print("Probs 0")
        return "0"
    else:
        print("WTF")
        return 1

# Nathan is a cuck.
def save(encoded_data, file):
    clean_base64 = base64.b64decode((str(encoded_data)))
    narray = np.frombuffer(clean_base64, np.uint8)
    img = cv2.imdecode(narray, cv2.IMREAD_ANYCOLOR)
    cv2.imwrite(file, img)
    result = reader.readtext(file)
    try:
        value = result[-0][1]
        # print("Digit: {0}".format(value))
        # print("Base64: {0}".format(encoded_data))
        lukeisafucboi[value] = encoded_data
    except IndexError:
        #print("Testing")
        value2 = template_match(encoded_data)
        if value2 == "0":
            lukeisafucboi[value2] = encoded_data


time.sleep(3)
table = browser.find_element_by_xpath("""//*[@id="cifField"]""")
browser.find_element_by_id("cifField").clear()
browser.find_element_by_id("cifField").send_keys(clientNumber)

digitpanel = browser.find_element_by_xpath("""//*[@id="keypad"]""")
keypad = digitpanel.find_element_by_class_name("module-keypad")
login_button = browser.find_element_by_xpath("""//*[@id="login-btn"]""")
ing_values = {}
keypad_digits = {}

lukeisafucboi = {}
lukehasmallpp = {}


reader = easyocr.Reader(['en'])


'''c = browser.find_element_by_css_selector('.module-keypad')
innerHTML = c.get_attribute('innerHTML')
src = c.get_attribute("src")
print(src)'''

banner()
# 1, 4  div elements = 0 isnt in the elements. - I am god.
for i in range(0, 5):
    for j in range(0, 5):
        for key_num in keypad.find_elements_by_xpath("""//*[@id="keypad"]/div/div[{}]/div[{}]/div/img""".format(j, i)):
            digits = key_num.get_attribute("src")
            ing_values = digits
            #print(ing_values[22:])
            test_vales = ing_values[22:]
            lukehasmallpp[test_vales] = (j, i)
            save(test_vales, "testfile{0}.png".format(i))

#print(lukeisafucboi)
#print('\n')
#print(lukehasmallpp)
#print('\n \n')

listy = []
'''for senpaiLukas in PIN:
    rr = lukeisafucboi[senpaiLukas]
    listy[rr] = lukehasmallpp[rr]
pprint(listy)'''

for senpaiLukas in list(PIN):
    imgString = lukeisafucboi[senpaiLukas]
    listy.append([imgString, lukehasmallpp[imgString]])
#pprint(listy)

for i in listy:
    nums = i[1]
    position = keypad.find_elements_by_xpath("""//*[@id="keypad"]/div/div[{}]/div[{}]/div/img""".format(nums[0], nums[1]))[0]
    position.click()

'''for i in keypad.find_elements_by_xpath("""//*[@id="keypad"]/div/div[{}]/div[{}]/div/img""".format(3, 3)):
    print(i)
    print(i.get_attribute("value"))'''

pprint(listy)
pprint(lukeisafucboi)


time.sleep(1)
login_button.click()