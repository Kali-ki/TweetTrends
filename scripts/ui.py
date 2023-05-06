import eel
import shutil
import os
import imagelib
from imagelib import ImageParser
import glob
from wikiparser import WikiParser

UI_FOLDER='web'


def _createHTMLFile(filename='index.html',head='<title>First Page</title>',body='<h1>Hello, World</h1>'):
    with open(filename,"w") as htmlfile:
        htmlfile.write(f"<html>\n<head>{head}\n</head> <body>{body} \n</body></html>")


def _createCSSFile(filename='style.css',content="body{background:yellow;color:white}"):
    with open(filename,"w") as cssfile:
        cssfile.write(content)

def _createJSFile(filename='script.js',content='console.log("Hello, World")'):
    with open(filename,"w") as jsfile:
        jsfile.write(content)

def _createImagesFolder():
    os.mkdir(UI_FOLDER+'/images')

def _deleteUIfolder(_,__):
    if os.path.exists(UI_FOLDER):shutil.rmtree(UI_FOLDER)
    exit()


def saveImage(url : str,imagename=None,background=False):
    """
    loads and saves an image from an url in the UI_FOLDER
    """
    img = imagelib.loadimage(url)
    if not background : img = imagelib.rembg(img)
    if not imagename : 
        sp= imagelib.imageNameFromUrl(url)
        # we convert automatically the image in png if the bh is removed
        if not background: sp[1]='png'
        imagename = sp[0].replace('%','_') +'.'+sp[1]
    imagelib.saveImage(img,UI_FOLDER+"/images/"+imagename)

def _updateLoadedImages( urls: list[str]):
    '''
    Resets the images folder content and loads all the new images in it
    '''
    for f in glob.glob(UI_FOLDER+"/images/*"):os.remove(f)
    for url in urls:
        if(len(url)>0): saveImage(url)

def _updateKeywords():
    #TODO: interact with tweeter (by example) to find keywords fitting to a period
    return ["griezmann","vincent collet","Lune"]
    

def _findImageLinks(parser : ImageParser,keywords:list[str]):
    return [parser.getImageLink(keyword) for keyword in keywords]
   

def startui():
   if not os.path.exists(UI_FOLDER): os.mkdir(UI_FOLDER)
   _initHTMLCSSJSFiles()
   _createImagesFolder()
   eel.init(UI_FOLDER)  
   @eel.expose
   def loadImagesPy():
    ip = WikiParser
    _updateLoadedImages(_findImageLinks(ip,_updateKeywords()))
    eel.loadImagesJs(os.listdir( UI_FOLDER+'/images'))
    print(os.listdir( UI_FOLDER+'/images'))
   eel.start('index.html',close_callback=_deleteUIfolder,size=(700,700))
   


def _initHTMLCSSJSFiles():
    head = '<title>Projet DE</title><link rel="stylesheet" href="style.css"><script type="text/javascript" src="/eel.js"></script><script type="text/javascript" src="script.js"></script>'
    body = '<button id="refresh" onclick="refresh()">Charger les images</button><div id="images"></div>'
    _createHTMLFile(UI_FOLDER+'/index.html',head,body)
    body = 'body{background:orange;color:white}; images{width:50;}'
    _createCSSFile(UI_FOLDER+'/style.css',body)
    body = "eel.expose(loadImagesJs);\n\
        function loadImagesJs(imagesnames) { ;\n\
        document.getElementById('images').innerHTML='';\n\
        for(let name of imagesnames){\n\
            document.getElementById('images').innerHTML+='<img src=images/'+name+' >'\n\
        };} \n\
        function refresh(){eel.loadImagesPy()}";
    _createJSFile(UI_FOLDER+'/script.js',content=body)
