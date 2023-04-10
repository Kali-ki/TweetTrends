from bs4 import BeautifulSoup
import wikipedia
import requests
import json

from PIL import Image
import imageloader
import requests


def get_wiki_image_link(search,lang='fr'):
    """
    A pour objectif de charger une image représentative du mot clé recherché
    Actuellement, récupère la miniature wikipédia présente dans les suggestions de frappe
    """
    wikipedia.set_lang(lang)
    results = wikipedia.search(search, results = 3)
    reqImg = 'https://'+lang+'.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&titles='+results[0]+'&pithumbsize=500'
    resp = requests.get(reqImg)
    pages = json.loads(resp.text)['query']['pages']
    for page_id in pages.keys():
        page = pages[page_id]
        if 'thumbnail' in page:
            image_url = page['thumbnail']['source']
            res,name,img = imageloader.loadImage(image_url,save=False)
            if res:
                return image_url,page['title']
    return False,None


def loadWikiImage(search_term,destdir='images/',nospace=False,save=False,lang='fr'):
    wiki_image_url,name = get_wiki_image_link(search_term,lang)
    if wiki_image_url==False:
        return False,None,None
    return imageloader.loadImage(wiki_image_url,destdir+name,save,nospace)

# sucss,_,img = loadWikiImage("Mars Planète",save=False,lang='fr')
# if sucss :img.show()
# else :print("Pas d'image")