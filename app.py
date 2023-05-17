import scripts.ui as ui

# Make sure the UI is already there
ui.startui()

########## IF YOU WANT TO BUILD THE UI FROM SCRATCH AGAIN ################
# import json
# from scripts.wikiparser import WikiParser
# from scripts.gimageserpapiparser import GImageSerpApiParser
# SERPAPITOKEN = json.load(open('config.json'))['SERPAPITOKEN'] #REPLACE IT WITH YOUR API TOKEN (STRING)

# ui.buildui([GImageSerpApiParser(SERPAPITOKEN),WikiParser])

