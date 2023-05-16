from serpapi import GoogleSearch
import json
from imagelib import ImageParser


class GImageSerpApiParser(ImageParser):
    def getImageLink(keyword: str) -> str:
        return _get_google_image_link(keyword)


def _get_google_image_link(search, lang='fr'):
    """
    Recherche un lien viable pour charger une image de google représentative du mot clé recherché
    """
    results = _search_google_image(search,lang)
    return ''
    print(results)
#_remove_query_string_from_url(results[0]["original"])



def _search_google_image(keyword : str,lang='fr'):
    params = {
    "q": keyword,
    "tbm": "isch",
    "ijn": "0",
    "api_key": "400100a67a253da696341b00365545083de9ac31f1f3372c4782b7614bc48df5",
    "gl": lang,
    "hl": lang
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    images_results = results["images_results"]
    # save the result locally
    # with open(keyword.replace(' ','_')+'_imagesearch.json', 'w') as fp:
    #     json.dump(images_results, fp)
    return images_results

def _remove_query_string_from_url(url):
    '''
    some urls of google images ends with an interrogation and numbers after

    They are not usefull, and may cause trouble in the image handling (we want the url to end with image format)

    example : 

    https://www.site.com/path/to/image/theimage.png?202209050149' 
    -> 
    https://www.site.com/path/to/image/theimage.png'
    '''
    if '?' in url:
        url_without_query_string = url[:url.rfind('?')]
    else:
        url_without_query_string = url
    return url_without_query_string

# image_link = _get_google_image_link("voiture")
# print(image_link)