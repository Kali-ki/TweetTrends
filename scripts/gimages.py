from serpapi import GoogleSearch
import json

def loadGoogleImage(search,lang='fr'):
    params = {
    "q": search,
    "tbm": "isch",
    "ijn": "0",
    "api_key": "400100a67a253da696341b00365545083de9ac31f1f3372c4782b7614bc48df5",
    "gl": lang,
    "hl": lang
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    images_results = results["images_results"]
    print(images_results)
    with open(search+'_imagesearch.json', 'w') as fp:
        json.dump(images_results, fp)

#loadGoogleImage()
    
