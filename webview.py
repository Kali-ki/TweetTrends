import eel
import wikiimages
import os.path

search_terms = ["Thomas Pesquet","Ada Lovelace","Antoine Dupont","Linus Torvalds","Gerard Depardieu"]
images = []


for search in search_terms:
    imagefullname = wikiimages.downloadWikiImage(search_term=search,destdir='web/images/',nospace=True)
    sp= imagefullname.split('/')[-1].split('.')
    imagename = sp[0]+'.'+sp[1]
    images.append(imagename)
    
notloadedimages =images.copy()

while(len(notloadedimages)!=len(images)):
    for image in notloadedimages:
        if(os.path.isfile('web/images/'+image)):
            notloadedimages.remove(image)
            break

eel.init('web')

@eel.expose
def loadImages():
    eel.loadImages(images)

eel.start('index.html')