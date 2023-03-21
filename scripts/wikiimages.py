import wikipedia
import requests
import json



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


import requests 
from PIL import Image
import imageloader


def loadWikiImage(search_term,destdir='images/',nospace=False,save=False,lang='en'):
    wiki_image_url,name = get_wiki_image_link(search_term,lang)
    if wiki_image_url==False:
        return False,None,None
    if nospace: #On enlève les underscore (cela peut être à l'origine d'erreurs)
        name = name.replace(" ","_")
    return imageloader.loadImage(wiki_image_url,destdir+name,save)
    
        
# sucss,_,img = loadWikiImage("Thomas Pesquet",destdir='web/images/',nospace=True)
# if sucss :img.show()
# else :print("Pas d'image")
