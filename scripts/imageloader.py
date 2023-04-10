from PIL import Image
import urllib.request
import mimetypes
import requests 

def getExtension(filename):
    contentType, _ = mimetypes.guess_type(filename)
    if(contentType=="image/svg+xml"):return ".svg"
    elif(contentType=="image/png"):return ".png"
    elif(contentType=="image/jpg"):return ".jpg"
    elif(contentType=="image/jpeg"):return ".jpg"
    elif(contentType=="image/gif"):return ".gif"
    else : return ""

def loadImage(url,file_name='tmp',save=True,nospace=False):
    extension = getExtension(url)
    file_name+=extension
    if nospace: #On enlève les underscore (cela peut être à l'origine d'erreurs)
        file_name = file_name.replace(" ","_")
    try :
        res = requests.get(url, stream = True)
        if res.status_code == 200 or res.status_code == 403:
            opener=urllib.request.build_opener()
            opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
            urllib.request.install_opener(opener)
            try:
                if(save):name,http =  urllib.request.urlretrieve(url,file_name)
                else: name,http =  urllib.request.urlretrieve(url)
                img = Image.open(name)
                return True,file_name,img
            except:
                pass
    except : pass
    return False,None,None