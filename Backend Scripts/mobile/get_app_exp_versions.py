import requests
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

UNITE_URL              = "https://s3.nikecdn.com/unite/scripts/unite.min.js"



def getAppExpVersions():
    global APPVERSION, EXPVERSION
    s                  = requests.session()
    s.headers.update({"User-Agent" : "Mozilla/5.0 (iPhone; CPU iPhone OS 14_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"})
    uniteResponse      = s.get(UNITE_URL)
    uniteText          = uniteResponse.text
    # return UniteText
    # APPVERSION & EXPVERSION use regex to search for version numbers; regex help: https://github.com/CoreyMSchafer/code_snippets/blob/master/Regular-Expressions/snippets.txt
    try:
        APPVERSION         = re.search(".appVersion..[0-9]*", uniteText).group().split('|')[2]
        EXPVERSION         = re.search(".experienceVersion..[0-9]*", uniteText).group().split('|')[2]
        print("+[getAppExpVersions]: Successfully updated nike app version & experience version")
    except Exception as err:
        print("+[getAppExpVersions]: COULDN'T UPDATE APP & EXPERIECE VERSIONS, SETTING DEFAULTS='847'", str(err))
        APPVERSION         = '847'
        EXPVERSION         = '847'


    print("AppVersion: ", APPVERSION)
    print("ExpVersion: ", EXPVERSION)
def login(email, password):
    s   = requests.session()
    s.cookies["CONSUMERCHOICE"]="us/en_us"
    s.cookies["NIKE_COMMERCE_COUNTRY"]="US"
    s.cookies["NIKE_COMMERCE_LANG_LOCALE"]="en_US"
    s.cookies["nike_locale"]="us/en_US"
    s.headers.update({"User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36"})
    res = s.post("")

    # this needs to happen after going to nike.com/launch page;
    # https://unite.nike.com/auth/slcheck_cookies/v1?appVersion=847&experienceVersion=847&uxid=com.nike.commerce.snkrs.web&locale=en_US&backendEnvironment=identity&browser=&os=Windows%20NT%2010.0%3B%20Win64%3B%20x64&mobile=false&native=false&visit=1&visitor=7636db26-5c82-4b25-8e30-8a2d91ed51b1&atgSync=false&uxId=com.nike.commerce.snkrs.web&cookieType=N

    #e=sess.post("https://unite.nike.com/loginWithSetCookie?appVersion={0}&experienceVersion={1}&uxid=com.nike.commerce.nikedotcom.web&locale=en_US&backendEnvironment=identity&browser=Google%20Inc.&os=undefined&mobile=false&native=false".format(APPVERSION,EXPVERSION),json={"username":email,"password":password,"client_id":"HlHa2Cje3ctlaOqnxvgZXNaAs7T9nAuH","ux_id":"com.nike.commerce.nikedotcom.web","grant_type":"password"},verify=False)
    
    
    
    
    # my tries for mobile, couldnt get working due to mobile ID or its checking the browswer;
    #https://unite.nike.com/login?appVersion=847&experienceVersion=847&uxid=com.nike.commerce.snkrs.web&locale=en_US&backendEnvironment=identity&browser=Google%20Inc.&os=undefined&mobile=false&native=false&visit=1&visitor=bc77740b-57f5-4ddf-ae7c-50ac56604613
    
    
    
    # my trys ; response = s.post("https://unite.nike.com/loginWithSetCookie?appVersion={0}&experienceVersion={1}&uxid=com.nike.commerce.snkrs.ios&locale=en_US&backendEnvironment=identity&browser=Apple%20Computer%2C%20Inc.&os=undefined&mobile=true&native=true".format(APPVERSION,EXPVERSION),json={"username":email,"password":password,"client_id":"G64vA0b95ZruUtGk1K0FkAgaO3Ch30sj","ux_id":"com.nike.commerce.snkrs.ios","grant_type":"password"},verify=False)
    # response = s.post("https://secure-store.nike.com/us/services/profileService",data={"action":"getprofile","rt":"JSON"},headers={"X-Requested-With":"XMLHttpRequest"})
    


    
