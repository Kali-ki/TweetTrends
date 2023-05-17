from PIL import Image
import urllib.request
import requests 
from rembg import remove
from abc import ABC, abstractmethod
import os


def imageNameFromUrl(url):
    '''
    extracts the name from the given url (last part of it)
    returns an array [imagename extension]
    '''
    return  url.split('/')[-1].split('.')


def extract_extension(filename):
    base_name = os.path.basename(filename)
    name, extension = os.path.splitext(base_name)
    return [name, extension]

def loadimage(url : str):
    '''
    url : the url of an image (the filename is in this url)
    return  : the loaded image
    '''
    extension  = imageNameFromUrl(url)[1]
    res = requests.get(url, stream = True)
    if res.status_code == 200 or res.status_code==403:
        opener=urllib.request.build_opener()
        opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        urllib.request.install_opener(opener)
        name,http =  urllib.request.urlretrieve(url)
        img = Image.open(name)
        return img
    return None


def showImage(img : Image):
    '''
    img : a Pillow Image (opened with from Image.open)

    it opens the image with the system viewer
    '''
    img.show()

def saveImage(img : Image,filename):
    img.save(filename, quality=100)
    

def rembg(img : Image):
    '''
    removes background from an image
    '''
    rgb_im = img.convert('RGBA')
    return remove(rgb_im)


# img = loadimage('https://upload.wikimedia.org/wikipedia/commons/6/67/FRA-ARG_%2810%29_%28cropped_2%29.jpg')
# img = rembg(img)
# showImage(img)


class ImageParser(ABC):
    '''
    Structure for classes that have the role of finding an illustration image from a keyword
    '''

    @abstractmethod
    def getImageLink(keyword:str)->str: pass