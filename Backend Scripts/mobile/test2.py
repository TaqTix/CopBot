import requests

def cookiesDict(session):
    print(requests.utils.dict_from_cookiejar(session.cookies))
    return requests.utils.dict_from_cookiejar(session.cookies)
s3 = requests.session()
s3.cookies["CONSUMERCHOICE"]="us/en_us"
s3.cookies["NIKE_COMMERCE_COUNTRY"]="US"
s3.cookies["NIKE_COMMERCE_LANG_LOCALE"]="en_US"
s3.cookies["nike_locale"]="us/en_US"
s3.headers.update({"User-Agent" : "Mozilla/5.0 (iPhone; CPU iPhone OS 14_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"})
print("Cookies Before Get Request")
cookiesDict(s3)
print("Attempting request")
#res = s3.get("https://www.nike.com/assets/experience/shoebox/snkrs/config/minversion/iOS.json")
res = s3.get("https://unite.nike.com/s3/unite/mobile.html")
print("Res Code: ", res.status_code)
print("Cookies After Request")
cookies = cookiesDict(s3)
print(cookies['_abck'])
s3.cookies['_abck'] = f"{cookies['_abck']}"
print(s3.cookies['_abck'])
#print("s3 cookie", cookies['_abck'])

print("Cookie Keys")
print(cookies.keys())
print("")


s3.close()