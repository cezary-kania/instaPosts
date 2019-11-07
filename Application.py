from PostDownloader import PostDownloader
from DownloaderConfig import DownloaderConfig

if __name__ == "__main__":
    dConfig = DownloaderConfig('./config.json')
    p = PostDownloader(dConfig)
    usersList = input("Enter list of usernames: ").split(',')
    p.DownloadImages(usersList)