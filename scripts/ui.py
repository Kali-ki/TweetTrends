import eel
import shutil
import os
import imagelib
from imagelib import ImageParser
import glob
from wikiparser import WikiParser
from gimageserpapiparser import GImageSerpApiParser
import shutil


UI_FOLDER='web'


def _createImagesFolder():
    os.mkdir(UI_FOLDER+'/images')

def _deleteUIfolder(_,__):
    if os.path.exists(UI_FOLDER):shutil.rmtree(UI_FOLDER)
    exit()


def saveImage(url : str,imagename=None,background=False):
    """
    loads and saves an image from an url in the UI_FOLDER
    background indicates the presence of background
    """
    img = imagelib.loadimage(url)
    if not background : img = imagelib.rembg(img)
    if not imagename : 
        sp= imagelib.imageNameFromUrl(url)
        # we convert automatically the image in png if the bh is removed
        if not background: sp[1]='png'
        imagename = sp[0].replace('%','_') +'.'+sp[1]
    path = UI_FOLDER+"/images/"+imagename
    imagelib.saveImage(img,path)
    while(not os.path.exists(path)):pass
    print(path)
    return imagename
    


def _updateKeywords(period):
    #TODO: interact with tweeter (by example) to find keywords fitting to a period
    return ["griezmann","vincent collet","mario"]
    
def _initPeriods():
    #TODO: load all available periods on init 
    return ["Decembre 2020", "Janvier 2021","Fevrier 2021"]

def _initHTMLCSSJSFiles():
    indexlines = []
    # read the template
    with open('../uitemplate.html', 'r') as template:
        for line in template:
            if '<!--datestopropose-->' in line:
                # create dropdown list containing all the available periods
                for period in _initPeriods():
                    name = period.replace(' ','-').lower()
                    option = f'<option value="{name}">{period}</value>'
                    indexlines.append(option)
            else :  indexlines.append(line.strip())

    # write the ui file
    with open(UI_FOLDER+"/index.html", 'w') as fileindex:
        fileindex.write('\n'.join(indexlines))


def startui():
   if not os.path.exists(UI_FOLDER): os.mkdir(UI_FOLDER)
   _initHTMLCSSJSFiles()
   _createImagesFolder()
   eel.init(UI_FOLDER)  

   @eel.expose
   def loadPeriodPy(periodid):
    '''
    Applies changes on the UI, according to a new period selection by the user
    The keywords of the periods are retreived
    The  illustration images are downloaded and their background are removed
    '''
    wikip = WikiParser
    gisp = GImageSerpApiParser
    keywords = _updateKeywords(periodid)
    eel.loadPeriodJs(_illustrate_keywords(keywords,[wikip, gisp]))

   eel.start('index.html',close_callback=_deleteUIfolder,size=(700,700))


def _findImageLinks(parser : ImageParser,keywordsurls:dict[str,str]):
    for keyword in keywordsurls:
        url = keywordsurls[keyword]
        if len(url)==0: # the url has not been found yet
            keywordsurls[keyword] = parser.getImageLink(keyword)
    return keywordsurls

def _illustrate_keywords(keywords : list[str],parsers : list[ImageParser]):
    keywords_url = {key: '' for key in keywords}
    for parser in parsers:
        keywords_url = _findImageLinks(parser,keywords_url)
    
    #Resets the images folder content and loads all the new images in it
    for f in glob.glob(UI_FOLDER+"/images/*"):os.remove(f)
    keywords_infos = []
    for keyword in list(keywords_url.keys()):
         url = keywords_url[keyword]
         illustration = saveImage(url) 
         keywords_infos.append({
             "keyword":keyword,
             "url":url,
             "illustration":illustration
         })
    eel.reload()
    return keywords_infos