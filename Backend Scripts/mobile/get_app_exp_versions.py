import requests
import re

UNITE_URL              = "https://s3.nikecdn.com/unite/scripts/unite.min.js"

def getAppExpVersions():
    s                  = requests.session()
    s.headers.update({"User-Agent" : "Mozilla/5.0 (iPhone; CPU iPhone OS 14_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"})
    uniteResponse      = s.get(UNITE_URL)
    uniteText          = uniteResponse.text
    # return UniteText
    # APPVERSION & EXPVERSION use regex to search for version numbers; regex help: https://github.com/CoreyMSchafer/code_snippets/blob/master/Regular-Expressions/snippets.txt

    APPVERSION         = re.search(".appVersion..[0-9]*", uniteText).group().split('|')[2]
    EXPVERSION         = re.search(".experienceVersion..[0-9]*", uniteText).group().split('|')[2]

    print("AppVersion: ", APPVERSION)
    print("ExpVersion: ", EXPVERSION)

    return APPVERSION, EXPVERSION


    
