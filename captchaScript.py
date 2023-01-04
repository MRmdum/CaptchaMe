import requests
import base64
from bs4 import BeautifulSoup
from PIL import Image

import pytesseract
import argparse
import cv2

mySession = requests.Session()

##connection to web page

url = "http://challenge01.root-me.org/programmation/ch8/"
page = mySession.get(url)

#parsing
soup = BeautifulSoup(page.content,"html.parser")
results = soup.find_all('img')[0].attrs['src'].split(",")[1]

#decoding base 64 + download
with open("imageToSave.png", "wb") as fh:
    fh.write(base64.decodebytes(results.encode('utf-8')))


#captcha solving part#

im = Image.open('imageToSave.png')
pixelMap = im.load()

img = Image.new( im.mode, im.size)
pixelsNew = img.load()
for i in range(img.size[0]):
    for j in range(img.size[1]):
        if pixelMap[i,j] == (0,0,0) or pixelMap[i,j] == (255,255,255): #rgba color not sure about the last one
            pixelsNew[i,j] = (255,255,255)
        else:
            pixelsNew[i,j] = (0,0,0)

filename = "filteredCaptcha.png"
img.save(filename)

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
	help="path to input image to be OCR'd")
ap.add_argument("-p", "--preprocess", type=str, default="thresh",
	help="type of preprocessing to be done")
args = vars(ap.parse_args())

###

image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

###

text = pytesseract.image_to_string(Image.open(filename))
text = text.replace('\n', '').replace(' ', '').replace(',', '').replace('\'', '')

print(text)
###

post_params = {'cametu' : text}
headers = {'Content-Type' : 'application/x-www-form-urlencoded'}
cookies ={'PHPSESSID': mySession.cookies.get('PHPSESSID')}

rcontent = mySession.post(url,data=post_params,cookies =cookies)

soup = BeautifulSoup(rcontent.content,"html.parser")
results = str(soup.find_all('p')[0]).removeprefix("<p>").removesuffix(".<br/></p>")

print(results)

#flag: dtePZJgVAfaU