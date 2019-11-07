import time, csv, requests, os, threading
from selenium import webdriver

class PostDownloader:
        
    __usernames = []

    def __init__(self, config):
        self.__config = config
        self.__initEnv()
    
    def __initEnv(self):
        self.__driverOptions = webdriver.ChromeOptions()
        for chromeOp in self.__config.GetChromeArgs():
            self.__driverOptions.add_argument(chromeOp)
        if not os.path.isdir("userdata"):
            os.mkdir("userdata")
            os.mkdir("userdata/linksFiles")
            os.mkdir("userdata/images")

    def __DownloadImage(self, url, destination, fileName):
        file = requests.get(url)
        open(destination+'/'+fileName,'wb').write(file.content)
    
    def __DownloadFoundedImages(self, username, images):
        destDir = 'userdata/images/' + username + '_photos'
        if not os.path.isdir(destDir):
            os.mkdir(destDir)
        print(f"Downloading {username}'s photos...")
        index = 0
        for img in images:
            fileName = username + '_img_' + str(index) + '.jpg'
            self.__DownloadImage(img,destDir,fileName)
            index += 1
        print(username + ' photos downloaded.')
    
    def __SearchForImgsLinks(self, username):
        webAddres = "https://www.instagram.com/" + username + "/?hl=pl"
        xPath = "//div[contains(@class, 'eLAPa')]//div[contains(@class, 'KL4Bh')]//img" 
        browser = webdriver.Chrome(options=self.__driverOptions)
        browser.get(webAddres)

        postAmmount = int((browser.find_element_by_xpath("//a[contains(@class, '-nal3')]//span[contains(@class, 'g47SY')]")).text.replace(" ", ""))
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
        return list(images)
    
    def __SaveImgsLinks(self, username, links):
        linksFileName = "userdata/linksFiles/" + username + "links.csv"
        with open(linksFileName, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow([f'Images: {len(links)}'])
            for img in links:
                writer.writerow([img])
        print(f"{username}'s {len(links)} links saved.")

    def DownloadUserImages(self, username):
        links = self.__SearchForImgsLinks(username)
        self.__SaveImgsLinks(username, links)
        self.__DownloadFoundedImages(username, links)

    def DownloadImages(self, usernames):
        threads = []
        for user in usernames:
            threads.append(threading.Thread(target=self.DownloadUserImages, args=(user,)))
        print('Processing...')
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        print('All images downloaded.')
    
    def AddUserName(self, username):
        self.__usernames.append(username)

    def AddUserNames(self, newUsernames):
        self.__usernames + newUsernames