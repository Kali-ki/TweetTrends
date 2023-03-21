import eel
import wikiimages
import os.path
import imagetreating

search_terms = ["Thomas Pesquet","Ada Lovelace","Antoine Dupont","Linus Torvalds","Gerard Depardieu"]
images = []


for search in search_terms:
    sucess,imagefullname,img = wikiimages.loadWikiImage(search_term=search,destdir='images/',nospace=True)
    if not sucess:
        print("Image de "+search+" non chargée")
    else :
        sp= imagefullname.split('/')[-1].split('.')
        imagename = sp[0]+'.'+sp[1]
        imgname = imagetreating.rembg(img,"web/images/"+sp[0])
        images.append(sp[0]+".png")
        print("Image de "+search+" ("+sp[0]+")"+" chargée")

notloadedimages =images.copy()

while(len(notloadedimages)>0):
    for image in notloadedimages:
        if(os.path.isfile("web/images/"+image)):
            notloadedimages.remove(image)
            break

eel.init('web')

@eel.expose
def loadImages():
    eel.loadImages(images)

eel.start('index.html')