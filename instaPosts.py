import time, csv, requests, os, threading
from selenium import webdriver

options = webdriver.ChromeOptions()
options.add_argument("--incognito")

if not os.path.isdir("userdata"):
    os.mkdir("userdata")
    os.mkdir("userdata/linksFiles")
    os.mkdir("userdata/images")

def downloadImage(url, destination, fileName):
    file = requests.get(url)
    open(destination+'/'+fileName,'wb').write(file.content)

def downloadImages(username):
    webAddres = "https://www.instagram.com/" + username + "/?hl=pl"
    linksFileName = "userdata/linksFiles/" + username + "links.csv"
    xPath = "//div[contains(@class, 'eLAPa')]//div[contains(@class, 'KL4Bh')]//img" 
    browser = webdriver.Chrome(options=options)
    browser.get(webAddres)

    postAmmount = int(browser.find_element_by_xpath("//a[contains(@class, '-nal3')]//span[contains(@class, 'g47SY')]").text)

    images_len = 0
    images = set()
    print(f'Collecting {username} images url\'s...')
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
    
    print(f"{username}'s {len(images)} links saved.")

# Downloader 
    destDir = 'userdata/images/' + username + '_photos'
    if not os.path.isdir(destDir):
        os.mkdir(destDir)
    print(f"Downloading {username}'s photos...")
    index = 0
    for img in images:
        fileName = username + '_img_' + str(index) + '.jpg'
        downloadImage(img,destDir,fileName)
        index += 1
    print(username + ' photos downloaded.')

if __name__ == "__main__":
    userslist = ['astronomer_amber', 'miss_mariposita_ann', 'programm.r'] 
    threads = []
    for user in userslist:
        threads.append(threading.Thread(target=downloadImages, args=(user,)))
    print('Processing...')
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    print('All images downloaded.')