import uibuilder
import urllib.parse
import eel
import base64
import imagelib
from PIL import Image
import json

UI_FOLDER='web'
TOP_HASHTAGS = '../data/tweets/most_used_hashtags.csv'


####################
#     INIT UI      #
###################

def buildui(parsers):
   uibuilder.build(parsers)

def startui():
   uibuilder.buildtemplate()
   eel.init(UI_FOLDER)  
   @eel.expose
   def loadPeriodPy(periodid):
    '''
    Applies changes on the UI, according to a new period selection by the user
    The keywords of the periods are retreived
    The  illustration images are downloaded and their background are removed
    '''
    keywords = uibuilder.getAllKeywords(periodid)
    eel.loadPeriodJs(keywords)

   @eel.expose
   def saveExternalfile(keyword,filename,data_url):
    # Remove the "data:image/png;base64," part from the data URL
    base64_data = data_url.split(',')[1]
    # Decode the Base64 string into bytes
    file_data = base64.b64decode(base64_data)
    # Save the file or process it as needed
    root_name =  keyword.replace('%','_').replace(' ','_')
    extension = imagelib.extract_extension(filename)[1]
    final_name = UI_FOLDER+'/images/'+ root_name+extension
    cropped_name = UI_FOLDER+'/images/'+ root_name+'_cropped.png'
    with open(final_name, 'wb') as f:
        f.write(file_data)
    with open(cropped_name, 'wb') as f:
        f.write(file_data)
    imagelib.saveImage(imagelib.rembg(Image.open(cropped_name)),cropped_name)
    allillustrations = uibuilder.getSavedKeywordsIllustrations()
    allillustrations[keyword]['illustration']=root_name+extension
    uibuilder.saveKeywordsIllustrations(allillustrations)


   @eel.expose
   def illustratePeriodPy(periodid,keywords):
    allillustrations =  uibuilder.getSavedKeywordsIllustrations()
    keywordsinfos =  [allillustrations[keyword] for keyword in keywords]
    for keywordinfo in keywordsinfos:
       df = uibuilder.getDfPeriod(periodid)
       keywordinfo['link']= df.loc[df[periodid] == keywordinfo['keyword'], 'context link '+periodid].values[0]
       keywordinfo['score']= str(df.loc[df[periodid] ==  keywordinfo['keyword'], 'score '+periodid].values[0])
    eel.illustratePeriodJs(keywordsinfos)


   def close(route,sockets):
       exit()
   eel.start('index.html',close_callback=close,size=(700,700))
