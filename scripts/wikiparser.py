# EXTERNAL LIBRAIRIES
import wikipedia
import requests
import json
# LOCAL LIBRARIES
from scripts.imagelib import ImageParser

class WikiParser(ImageParser):
    def getImageLink(keyword:str)->str: 
        return _get_wiki_image_link(keyword)
    

def _get_wiki_image_link(search,lang='fr'):
    """
    Recherche un lien viable pour charger une image wikipedia représentative du mot clé recherché
    """
    wikipedia.set_lang(lang)
    results = wikipedia.search(search, results = 3)
    if(len(results)==0): return ''
    return _get_wiki_suggestion_link(results[0],lang)


def _get_wiki_suggestion_link(page_name,lang='fr'):
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
            return image_url
    return ''
    