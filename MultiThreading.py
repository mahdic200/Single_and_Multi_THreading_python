import requests, os, timeit
from threading import Thread


class MultiThreading:
    ABS_PATH = os.path.dirname(os.path.abspath(__file__))
    
    def __init__(self) -> None:
        self.__threads = []
        self.__urls = []
        self.__startTime = 0
        self.__endTime = 0
        self.__logs = []
        self.__downloadedImagesFolder = "MultiThreadingImages"
        if not os.path.exists(MultiThreading.standardPath(self.__downloadedImagesFolder)):
            os.mkdir(MultiThreading.standardPath(self.__downloadedImagesFolder))
        
    @property
    def totalTime(self):
        return self.__endTime - self.__startTime

    @property
    def urls(self):
        return self.__urls
    
    @property
    def logs(self):
        return self.__logs

    def __downloadImage(self, url):
        # try:
            response = requests.get(url)
            response.raise_for_status()
            if response.status_code != 204:
                path = MultiThreading.standardPath(self.__downloadedImagesFolder, self.__getImageName(url))
                with open(path, "wb+") as f:
                    f.write(response.content)
        # except Exception as e:
        #     # self.__logs.append({"message":e, "url":url})
        #     raise Exception(e)

    def __getImageName(self, url):
        return url.split("/")[-1]

    def __initUrls(self):
        path = MultiThreading.standardPath("urls.txt")
        with open(path, 'r') as f:
            allUrls = f.readlines()
        for url in allUrls:
            self.__urls.append(url.replace("\n", ""))

    def __main(self):
        self.__initUrls()
        i = 0
        for url in self.__urls:
            try:
                temp = Thread(target=self.__downloadImage, args=[url])
                self.__threads.append(temp)
                self.__threads[i].start()
                i += 1
            except Exception as e:
                print('there is a problem with url !')
                continue
            
        
        for thread in self.__threads:
            thread.join()

    def fire(self):
        self.__startTime = timeit.default_timer()
        self.__main()
        self.__endTime = timeit.default_timer()
        for i in self.__logs:
            path = MultiThreading.standardPath("error_logs.txt")
            with open(path, 'a+') as f:
                f.write(i["url"] + "\n")
                f.write(str(i["message"]) + "\n\n")

    def standardPath(*args):
        return os.path.join(MultiThreading.ABS_PATH, *args)

sth = MultiThreading()
sth.fire()

print(f"total process time : {sth.totalTime} seconds .")




























































