import datetime
import requests


# https://github.com/zruss11/Nike-InboxCheck/blob/master/classes/login.py

# def login(self, account):
def login():
    nikeLoginHeader = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36"
    }

    # email = account.split(':')[0]
    # password = account.split(':')[1]

    req = requests.session()

    req.headers.update(nikeLoginHeader)
    loginData = {
        "username"       : "acrypto91@gmail.com",
        "password"       : "Charlie123!",
        "keepMeLoggedIn" : "true",
        "client_id"      : "HlHa2Cje3ctlaOqnxvgZXNaAs7T9nAuH",
        "ux_id"          : "com.nike.commerce.nikedotcom.web",
        "grant_type"     : "password"
    }

    while True:
        login = req.post(
            "https://unite.nike.com/login?appVersion=281&experienceVersion=244&uxid=com.nike.commerce.snkrs.ios&locale=en_US&backendEnvironment=identity&browser=Apple+Computer%2C+Inc.&os=undefined&mobile=true&native=true",
            json=loginData)
        if login.status_code == 200:
            break
        else:
            #print(login.json()["error_description"], "error")
            print("Error, Status Code: ", login.status_code)
            return True
    access_token = login.json()['access_token']

    url = "https://api.nike.com/plus/v3/notifications/me/stored?before={}Z&locale=en_US&limit=20".format(datetime.datetime.now().isoformat())

    headers = {
        "authorization" : "Bearer {}".format(access_token)
    }
    messages = req.get(url, headers = headers)

    if len(messages.json()['notifications']) == 0:
        print("Empty Inbox", "error")
    else:
        for i in messages.json()['notifications']:
            print(i['message'].encode("utf8"))


    return True

if __name__ == "__main__":
    login()