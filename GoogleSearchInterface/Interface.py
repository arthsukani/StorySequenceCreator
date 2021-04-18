from google_images_search import GoogleImagesSearch
import random
import os
from os import path
class GoogleInterface:
    def __init__(self,keyword,total_images=25):
        self.inputFormat = {"Records":[]}
        self.gis = GoogleImagesSearch('AIzaSyB07WusV1J5ncbUBCCyRWnmWTPSWLb6K5U','de1bc6f11f40840c2')

        # define search params:
        self._search_params = {
            'q': keyword,
            'num': total_images,
        }

        self.totalimages = total_images

    def setKeywords(self,keyword,total_images=10):
        self._search_params = {
            'q': keyword,
            'num':total_images,
        }

    def gettingUrls(self):
        self.gis.search(search_params=self._search_params)
        result = self.gis.results()
        index = random.randrange(0,len(result))
        return result[index].url

if __name__ == "__main__":
    print("Testing Images Interface")
    G = GoogleInterface("Man on the Sky")
    G.gettingUrls()