from serpapi import GoogleSearch
import json
import imageloader

def searchGoogleImage(search,lang='fr'):
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
    return images_results

def getImageGoogleImage(imagesearchresults,index=0):
    image_link = imagesearchresults[index]['original']
    image_name = "gimage_"+image_link.split('/')[-1]
    ext = imageloader.getExtension(image_name)
    if len(ext)==0 :
        ext = imageloader.getExtension(imagesearchresults[index]['thumbnail'].split('/')[-1])
        image_name += ext
        if(ext!='.jpg' and ext!='.png'):
            # On n'a pas d'info dans le json à propos du type d'image
            # Et ce n'est ni un jpeg, ni un png
            # Pour l'instant, on dit que cette image n'est pas accessible 
            return  False,None
    sucss,_,img =  imageloader.loadImage(image_link,"g_image_"+str(index)+ext)
    if sucss :
        print(image_name)
        img.show()
    else :print("Pas d'image")

f = open('data/apple_imagesearch.json')
d = json.load(f)

# for i in range(12,len(d)):
# getImageGoogleImage(d)

# # TODO:
# def loadGoogleImage(search,lang='fr'):
    
#loadGoogleImage()