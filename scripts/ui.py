import uibuilder
import eel

UI_FOLDER='web'
TOP_HASHTAGS = '../data/tweets/most_used_hashtags.csv'


####################
#     INIT UI      #
###################

def startui():
#    uibuilder.build()
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
   def illustratePeriodPy(keywords):
    allillustrations =  uibuilder.getSavedKeywordsIllustrations()
    keywordsinfos =  [allillustrations[keyword] for keyword in keywords]
    eel.illustratePeriodJs(keywordsinfos)


   def close(route,sockets):
       exit()
   eel.start('index.html',close_callback=close,size=(700,700))

#    @eel.expose
#    def saveFilePy(file):
#      print(file)