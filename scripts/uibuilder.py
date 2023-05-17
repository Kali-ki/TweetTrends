import pandas as pd
import os
import shutil
from imagelib import ImageParser
import imagelib
from imagelib import ImageParser
import json


TOP_HASHTAGS = '../data/tweets/most_used_hashtags.csv'
UI_FOLDER='web'



def build(parsers):
    if not os.path.exists(UI_FOLDER): os.mkdir(UI_FOLDER)
    buildtemplate()
    _createImagesFolder()
    _illustrateAllPeriods(parsers)


def _createImagesFolder():
    if not os.path.exists(UI_FOLDER+"/images"):  os.mkdir(UI_FOLDER+'/images')
    source_path = '../images/emptyimage.svg'
    destination_path = UI_FOLDER+'/images/emptyimage.svg'
    shutil.copy(source_path, destination_path)
    source_path = '../images/hashtags_evolution.png'
    destination_path = UI_FOLDER+'/hashtags_evolution_default.png'
    shutil.copy(source_path, destination_path)

def _illustrateAllPeriods(parsers):
    for period in getAllPeriods():
        print("Chargement "+period)
        keywords = getAllKeywords(period)
        _illustrate_keywords(keywords,parsers)

def getDfPeriod(periodid):
    # get a data frame with columns that match only the corresponding period
    df =pd.read_csv(TOP_HASHTAGS)
    df = df[df.columns[df.columns.map(lambda x: periodid in x)]]
    return df


def getAllPeriods():
    '''load all available periods on init '''
    df = pd.read_csv(TOP_HASHTAGS)
    # the regex finds all the columns that are 4 digits
    year_columns = df.columns[df.columns.str.match(r'^\d{4}$')]
    return year_columns


def getAllKeywords(period):
    '''retrives all the most important keywords related to a period'''
    df = pd.read_csv(TOP_HASHTAGS).sort_values('score '+period,ascending=False)
    return df[period].tolist()


def getSavedKeywordsIllustrations():
    try:
        with open(UI_FOLDER+"/keywords_illustration.json", "r") as json_file:
            return json.load(json_file)
    except FileNotFoundError:
        return {}
    
def saveKeywordsIllustrations(keywords_infos):
    with open(UI_FOLDER+"/keywords_illustration.json", "w") as json_file:
         # Write the dictionary to the file as JSON data
         json.dump(keywords_infos, json_file)



def buildtemplate():
    indexlines = []
    # read the template
    with open('../uitemplate.html', 'r') as template:
        for line in template:
            if '<!--datestopropose-->' in line:
                # create dropdown list containing all the available periods
                for period in getAllPeriods():
                    name = period.replace(' ','-').lower()
                    option = f'<option value="{name}">{period}</value>'
                    indexlines.append(option)
            else :  indexlines.append(line.strip())

    # write the ui file
    with open(UI_FOLDER+"/index.html", 'w') as fileindex:
        fileindex.write('\n'.join(indexlines))


def _illustrate_keywords(keywords : list[str],parsers : list[ImageParser],save_illustrations=True):
    '''
    tries to illustrate the maximum of keywords with the parsers.
    returns a list of     objects with the shape :  
    { keyword,  url, illustration} indicating all the illustrated keywords.
    url and illustration can be empty strings if the parsers failed to find an illustration.
    '''
    keywords_existing_illustrations = getSavedKeywordsIllustrations()
    keywords_url = {key: '' for key in keywords}
    for keyword in keywords:
        if keyword in keywords_existing_illustrations:
            keywords_url[keyword] = keywords_existing_illustrations[keyword]['url']
    for parser in parsers:
        keywords_url = _findImageLinks(parser,keywords_url)

    # loads all the new images in the images folder
    keywords_infos = []
    for keyword in list(keywords_url.keys()):
        if keyword in keywords_existing_illustrations:
            url = keywords_existing_illustrations[keyword]['url']
            illustration = keywords_existing_illustrations[keyword]['illustration']
        else :
            url = keywords_url[keyword]
            illustration = ''
            if  len(url)>0: # On sauve l'image si on a trouvé une url
              illustration = _imagenameformat(url, keyword)
              if not os.path.exists(UI_FOLDER+'/images/' + illustration):
                im_saved = saveImage(url, keyword,both=True)
                if im_saved!=None : illustration= im_saved
                else : 
                    url =''
                    illustration=''
        keywords_infos.append({
            "keyword":keyword,
            "url":url,
            "illustration":illustration
        })
    if save_illustrations:
        # transform data in dictionnary and concatenate
        keywords_existing_illustrations.update({d['keyword']: d for d in keywords_infos})
        saveKeywordsIllustrations(keywords_existing_illustrations)
    return keywords_infos
        

def _findImageLinks(parser : ImageParser,keywordsurls:dict[str,str]):
    '''
    tries to illustrate (find an url) the maximum of not illustrated keywords with the given parser
    '''
    for keyword in keywordsurls:
        url = keywordsurls[keyword]
        if len(url)==0: # the url has not been found yet
            keywordsurls[keyword] = parser.getImageLink(keyword)
    return keywordsurls

def _imagenameformat(url,imagename=None,background=False):
    '''
    returns the appropriate name for an image to save
    '''
    sp= imagelib.imageNameFromUrl(url)
    # some url do not end with extension name, we suppose they are correct and so we add .png
    if(len(sp)==1):
        sp.append('png')
        print(sp)
    if imagename: sp[0]=imagename
    # we convert automatically the image in png if the bg is removed
    if not background: sp[1]='png'
    imagename = sp[0]+'.'+sp[1]
    imagename =imagename.replace('%','_').replace(' ','_') #file name cannot have '%' in their names
    return imagename


def saveImage(url : str,imagename=None,background=False,both=False):
    """
    loads and saves an image from an url in the UI_FOLDER
    background indicates the presence of background
    imagename is a name of image (without its format)
    if both is true, it saves the image with AND without the bg
    """
    img = imagelib.loadimage(url)
    
    if img ==None:
        return None
    root = UI_FOLDER+"/images/"
    if  background or both:
        fullname = _imagenameformat(url,imagename,False)
        imagelib.saveImage(img,root+fullname)
    if not background or both:
        img_nobg = imagelib.rembg(img)
        croppedname = _imagenameformat(url,imagename+'_cropped',False)
        imagelib.saveImage(img_nobg,root+croppedname)
    return fullname
    