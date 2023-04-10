from bs4 import BeautifulSoup
import wikipedia
import requests
import json

from PIL import Image
import imageloader
import requests


def _get_wiki_suggestion_link(page_name,lang):
    """
    Récupère le lien de la miniature wikipédia présente dans les suggestions de frappe
    """
    reqImg = 'https://'+lang+'.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&titles='+page_name+'&pithumbsize=500'
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

def _get_wiki_main_image_link(page_name,lang):
    """
    FIXME: problème d'asynchronisme mais sur la bonne voie
    Récupère le lien de l'image principale de la page wikipédia en question
    """ 
    reqImg = 'https://'+lang+'.wikipedia.org/w/api.php?action=query&prop=images&format=json&titles='+page_name+'&imlimit=max'
    resp = requests.get(reqImg)
    data = json.loads(resp.text)
    page_id = list(data['query']['pages'].keys())[0]  # Get the first (and only) page ID
    for i,image in enumerate(data['query']['pages'][page_id]['images']):
        image_title = image['title'].split(':')[-1]
        urlimage = 'https://'+lang+'.wikipedia.org/w/api.php?action=query&titles=Image:'+image_title+'&prop=imageinfo&iiprop=url&format=json'   
        print(urlimage)
        for s in page_name.split():
            if s in image_title.split():
                #FIXME: le problème est ici : ne fonctionne que très partiellement
                urlimage = json.loads(requests.get(urlimage).text)['query']['pages']['-1']['imageinfo'][0]['url']
                return urlimage,page_name
    return False, None


def get_wiki_image_link(search,lang='fr'):
    """
    Recherche un lien viable pour charger une image représentative du mot clé recherché
    """
    wikipedia.set_lang(lang)
    results = wikipedia.search(search, results = 3)
    # return _get_wiki_main_image_link(results[0],lang)
    return _get_wiki_suggestion_link(results[0],lang)


def loadWikiImage(search_term,destdir='images/',nospace=False,save=False,lang='fr'):
    wiki_image_url,name = get_wiki_image_link(search_term,lang)
    if wiki_image_url==False:
        return False,None,None
    return imageloader.loadImage(wiki_image_url,destdir+name,save,nospace)

# sucss,_,img = loadWikiImage("Vincent Collet",save=False,lang='fr')
# if sucss :img.show()
# else :print("Pas d'image")