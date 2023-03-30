import wikipedia
import requests
import json

from PIL import Image
import imageloader


def get_wiki_image_link(search_term,lang='fr'):
    WIKI_REQUEST = 'http://'+lang+'.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&piprop=original&titles='
    try:
        wikipedia.set_lang(lang)
        results = wikipedia.search(search_term)
        for result in results:
            try:
                page = wikipedia.page(title=result,auto_suggest=False)
                title = page.title
                response  = requests.get(WIKI_REQUEST+title)
                json_data = json.loads(response.text)
                img_link = list(json_data['query']['pages'].values())[0]['original']['source']
                return str(img_link),title
            except:
                pass
        return False,None
    except:
        return False,None


def loadWikiImage(search_term,destdir='images/',nospace=False,save=False,lang='en'):
    wiki_image_url,name = get_wiki_image_link(search_term,lang)
    if wiki_image_url==False:
        return False,None,None
    return imageloader.loadImage(wiki_image_url,destdir+name,save,nospace)
    
        
sucss,_,img = loadWikiImage("Arothron meleagris",save=False,lang='fr')
if sucss :img.show()
else :print("Pas d'image")