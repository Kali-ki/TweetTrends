# EXTERNAL LIBRARIES
from serpapi import GoogleSearch
# LOCAL LIBRAIRIES
from scripts.imagelib import ImageParser

class GImageSerpApiParser(ImageParser):
    def __init__(self, apikey):
        self.APIKEY = apikey

    def getImageLink(self, keyword: str) -> str:
        return self._get_google_image_link(keyword)

    def _get_google_image_link(self, search, lang='fr'):
        results = self._search_google_image(search, lang)
        if len(results)>0:
            return self._remove_query_string_from_url(results[0]["original"])
        else : 
            return ''

    def _search_google_image(self, keyword: str, lang='fr'):
        params = {
            "q": keyword,
            "tbm": "isch",
            "ijn": "0",
            "api_key": self.APIKEY,
            "gl": lang,
            "hl": lang
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        if "images_results" in results:
            images_results = results["images_results"]
            return images_results
        else :return []

    def _remove_query_string_from_url(self, url):
        if '?' in url:
            url_without_query_string = url[:url.rfind('?')]
        else:
            url_without_query_string = url
        return url_without_query_string


# parser = GImageSerpApiParser('fd7b843aed225a244f906d11a8161a00b12c3efdea2c12ae91b481d313206b37')
# image_link = parser.getImageLink("PRESIDENTIELLE2017")
# print(image_link)
