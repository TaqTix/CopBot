import requests
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

UNITE_URL              = "https://s3.nikecdn.com/unite/scripts/unite.min.js"

def getAppExpVersionsDict(mobile=False):
    global APPVERSION, EXPVERSION
    s                  = requests.session()
    if(mobile):
        s.headers.update({"User-Agent" : "Mozilla/5.0 (iPhone; CPU iPhone OS 14_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"})
    else:
        s.headers.update({"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36"})

    uniteResponse      = s.get(UNITE_URL)
    uniteText          = uniteResponse.text
    # APPVERSION & EXPVERSION use regex to search for version numbers; regex help: https://github.com/CoreyMSchafer/code_snippets/blob/master/Regular-Expressions/snippets.txt
    try:
        APPVERSION         = re.search(".appVersion..[0-9]*", uniteText).group().split('|')[2]
        EXPVERSION         = re.search(".experienceVersion..[0-9]*", uniteText).group().split('|')[2]
        print("+[getAppExpVersions]: Successfully updated nike app version & experience version (", str(APPVERSION), ",", str(EXPVERSION), ")")
    except Exception as err:
        print("+[getAppExpVersions]: COULDN'T UPDATE APP & EXPERIECE VERSIONS, SETTING DEFAULTS='847'", str(err))
        APPVERSION         = '847'
        EXPVERSION         = '847'

    d = dict()
    d['APPVERSION'] = APPVERSION
    d['EXPVERSION'] = EXPVERSION
    
    return d
