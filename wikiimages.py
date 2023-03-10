import wikipedia
import requests
import json


def get_wiki_image(search_term):
    WIKI_REQUEST = 'http://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles='
    try:
        result = wikipedia.search(search_term, results = 1)
        wikipedia.set_lang('en')
        wkpage = wikipedia.WikipediaPage(title = result[0])
        title = wkpage.title
        response  = requests.get(WIKI_REQUEST+title)
        json_data = json.loads(response.text)
        img_link = list(json_data['query']['pages'].values())[0]['original']['source']
        return img_link        
    except:
        return 0


import requests # request img from web
import urllib.request
import mimetypes

def getExtension(filename):
    contentType, _ = mimetypes.guess_type(filename)
    if(contentType=="image/svg+xml"):return ".svg"
    elif(contentType=="image/png"):return ".png"
    elif(contentType=="image/jpg"):return ".jpg"
    elif(contentType=="image/jpeg"):return ".jpeg"
    elif(contentType=="image/gif"):return ".gif"
    else : return ""

def downloadImage(url,file_name):
    extension = getExtension(url)
    file_name+=extension
    # url = input('Please enter an image URL (string):') #prompt user for img url
    # file_name = input('Save image as (string):') #prompt user for file_name
    res = requests.get(url, stream = True)
    if res.status_code == 200 or res.status_code == 403:
        opener=urllib.request.build_opener()
        opener.addheaders=[('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
        urllib.request.install_opener(opener)
        img = urllib.request.urlretrieve(url,file_name)

    return res.status_code


def downloadWikiImage(search_term):
    wiki_image_url = str(get_wiki_image(search_term))
    downloadImage(wiki_image_url,'images/'+search_term)
        

downloadWikiImage("Rennes")