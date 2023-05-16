import eel
import shutil
import os
import imagelib
from imagelib import ImageParser
import glob
from wikiparser import WikiParser
from gimageserpapiparser import GImageSerpApiParser
import shutil
import json


UI_FOLDER='web'


def startui(save_ui=True):
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
    keywords = _updateKeywords(periodid)
    eel.loadPeriodJs(keywords)

   @eel.expose
   def illustratePerdiodPy(keywords):
    wikip = WikiParser
    gisp = GImageSerpApiParser
    eel.illustratePeriodJs(_illustrate_keywords(keywords,[wikip, gisp]))


   def close(route,sockets):
       if not save_ui : _deleteUIfolder()
       exit()
   eel.start('index.html',close_callback=close,size=(700,700))



####################
#     INIT UI      #
###################

def _createImagesFolder():
    if not os.path.exists(UI_FOLDER+"/images"):  os.mkdir(UI_FOLDER+'/images')
    source_path = '../images/emptyimage.svg'
    destination_path = UI_FOLDER+'/images/emptyimage.svg'
    shutil.copy(source_path, destination_path)

def _deleteUIfolder():
    if os.path.exists(UI_FOLDER):shutil.rmtree(UI_FOLDER)


def _updateKeywords(period):
    #TODO: interact with tweeter (by example) to find keywords fitting to a period
    return ["griezmann","françois hollande","mario"]
    
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


##########################
#  KEYWORDS ILLUSTRATION #
##########################


def _illustrate_keywords(keywords : list[str],parsers : list[ImageParser],save_illustrations=True):
    '''
    tries to illustrate the maximum of keywords with the parsers.
    returns a list of     objects with the shape :  
    { keyword,  url, illustration} indicating all the illustrated keywords.
    url and illustration can be empty strings if the parsers failed to find an illustration.
    '''
    keywords_existing_illustrations = _getSavedKeywordsIllustrations()
    keywords_url = {key: '' for key in keywords}
    for keyword in keywords:
        if keyword in keywords_existing_illustrations:
            keywords_url[keyword] = keywords_existing_illustrations[keyword]['url']
    for parser in parsers:
        keywords_url = _findImageLinks(parser,keywords_url)
    
    # loads all the new images in the images folder
    keywords_infos = []
    for keyword in list(keywords_url.keys()):
        url = keywords_url[keyword]
        illustration = ''
        if  len(url)>0: # On sauve l'image si on a trouvé une url
            illustration = _imagenameformat(url, keyword)
            if not os.path.exists(UI_FOLDER+'/images/' + illustration):
                saveImage(url, keyword)
        keywords_infos.append({
            "keyword":keyword,
            "url":url,
            "illustration":illustration
        })
    if save_illustrations:
        # transform data in dictionnary and concatenate
        keywords_existing_illustrations.update({d['keyword']: d for d in keywords_infos})
        _saveKeywords_Illustration(keywords_existing_illustrations)
    return keywords_infos


def _imagenameformat(url,imagename=None,background=False):
    '''
    returns the appropriate name for an image to save
    '''
    sp= imagelib.imageNameFromUrl(url)
    if imagename: sp[0]=imagename
    imagename.replace('%','_').replace(' ','_') #file name cannot have '%' in their names
    # we convert automatically the image in png if the bg is removed
    if not background: sp[1]='png'
    imagename = sp[0]+'.'+sp[1]
    return imagename


def saveImage(url : str,imagename=None,background=False):
    """
    loads and saves an image from an url in the UI_FOLDER
    background indicates the presence of background
    imagename is a name of image (without its format)
    """
    img = imagelib.loadimage(url)
    if not background : 
        img = imagelib.rembg(img)
    imagename = _imagenameformat(url,imagename,background)
    path = UI_FOLDER+"/images/"+imagename
    imagelib.saveImage(img,path)
    #waits for the images to be loaded
    while(not os.path.exists(path)):pass
    print(path)
    return imagename
    

def _findImageLinks(parser : ImageParser,keywordsurls:dict[str,str]):
    '''
    tries to illustrate (find an url) the maximum of not illustrated keywords with the given parser
    '''
    for keyword in keywordsurls:
        url = keywordsurls[keyword]
        if len(url)==0: # the url has not been found yet
            keywordsurls[keyword] = parser.getImageLink(keyword)
    return keywordsurls

def _getSavedKeywordsIllustrations():
    try:
        with open(UI_FOLDER+"/keywords_illustration.json", "r") as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return {}
    
def _saveKeywords_Illustration(keywords_infos):
    with open(UI_FOLDER+"/keywords_illustration.json", "w") as json_file:
         # Write the dictionary to the file as JSON data
         json.dump(keywords_infos, json_file)