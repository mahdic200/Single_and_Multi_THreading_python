import requests, os, timeit


class SingleThreading:
    ABS_PATH = os.path.dirname(os.path.abspath(__file__))
    
    def __init__(self) -> None:
        self.__urls = []
        self.__startTime = 0
        self.__endTime = 0
        self.__logs = []
        self.__downloadedImagesFolder = "SingleThreadingImages"
        if not os.path.exists(SingleThreading.standardPath(self.__downloadedImagesFolder)):
            os.mkdir(SingleThreading.standardPath(self.__downloadedImagesFolder))
        
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
        try:
            response = requests.get(url)
            response.raise_for_status()
            if response.status_code != 204:
                path = SingleThreading.standardPath(self.__downloadedImagesFolder, self.__getImageName(url))
                with open(path, "wb+") as f:
                    f.write(response.content)
        except Exception as e:
            # self.__logs.append({"message":e, "url":url})
            raise Exception(e)

    def __getImageName(self, url):
        return url.split("/")[-1]

    def __initUrls(self):
        path = SingleThreading.standardPath("urls.txt")
        with open(path, 'r') as f:
            allUrls = f.readlines()
        for url in allUrls:
            self.__urls.append(url.replace("\n", ""))

    def __main(self):
        self.__initUrls()
        for url in self.__urls:
            try:
                self.__downloadImage(url)
            except Exception as e:
                print(e)
                continue

    def fire(self):
        self.__startTime = timeit.default_timer()
        self.__main()
        self.__endTime = timeit.default_timer()

    def standardPath(*args):
        return os.path.join(SingleThreading.ABS_PATH, *args)

sth = SingleThreading()
sth.fire()

print(f"total process time : {sth.totalTime} seconds .")

# print(SingleThreading.ABS_PATH)


























































