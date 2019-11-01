import time, csv, requests, os
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument("--incognito")

if not os.path.isdir("userdata"):
    os.mkdir("userdata")
    os.mkdir("userdata/linksFiles")
    os.mkdir("userdata/images")

profile = input("Enter instagram username: ")

browser = webdriver.Chrome(options=options)

webAddres = "https://www.instagram.com/" + profile + "/?hl=pl"
linksFileName = "userdata/linksFiles/" + profile + "links.csv"
xPath = "//div[contains(@class, 'eLAPa')]//div[contains(@class, 'KL4Bh')]//img" 

browser.get(webAddres)

postAmmount = int(browser.find_element_by_xpath("//a[contains(@class, '-nal3')]//span[contains(@class, 'g47SY')]").text)

images_len = 0
images = set()
print('Collecting images url\'s...')
while(images_len < postAmmount):
    time.sleep(1)
    tmpImgs = browser.find_elements_by_xpath(xPath)
    for webEl in tmpImgs:
        images.add(webEl.get_attribute("src"))
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    images_len = len(images)
browser.close()

with open( linksFileName, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([f'Images: {len(images)}'])
    for img in images:
        writer.writerow([img])
    
print(f"{len(images)} links saved.")

# Downloader 
def downloadImage(url, destination, fileName):
    file = requests.get(url)
    open(destination+'/'+fileName,'wb').write(file.content)

destDir = 'userdata/images/' + profile + '_photos'
if not os.path.isdir(destDir):
    os.mkdir(destDir)
print('Downloading...')
index = 0
for img in images:
    fileName = profile + '_img_' + str(index) + '.jpg'
    downloadImage(img,destDir,fileName)
    index += 1
print('Photos downloaded.')