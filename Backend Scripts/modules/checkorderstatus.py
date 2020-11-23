# created 3 years ago;``
ACCOUNTFILE="accounts.txt"
PROXYFILE="proxies.txt"
MAXTHREADS=50
OUTPUTFILE="orderstatus.txt"
MININTERVAL=1

try:
    PROXYLIST=open(PROXYFILE,'r').read().split("\n")
    PROXYLIST=[p.strip() for p in PROXYLIST if p.strip()!=""]
except:
    PROXYLIST=[None]
import Queue
import random
PROXYQUEUE=Queue.Queue()
random.shuffle(PROXYLIST)
for p in PROXYLIST:
    PROXYQUEUE.put(p)
def getproxy():
    v=PROXYQUEUE.get()
    PROXYQUEUE.put(v)
    return v
import requests,uuid, urllib3
from urllib3.exceptions import InsecureRequestWarning,SubjectAltNameWarning
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
urllib3.disable_warnings(urllib3.exceptions.SubjectAltNameWarning)

def checkacc(x):
    v=x.split(":")
    sess=requests.session()
    uid=str(uuid.uuid4())
    sess.cookies["NIKE_COMMERCE_COUNTRY"]="US"
    sess.cookies["NIKE_COMMERCE_LANG_LOCALE"]="en_US"
    sess.cookies["nike_locale"]="us/en_us"
    m_login_data = {'keepMeLoggedIn':True, 'client_id':'PbCREuPr3iaFANEDjtiEzXooFl7mXGQ7','ux_id':'com.nike.commerce.snkrs.droid','grant_type':'password','username':v[0],'password':v[1]}
    prox=getproxy()
    sess.headers.update({"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36","Accept":"*/*","Accept-Encoding":"gzip, deflate, br","Accept-Language":"en-US,en;q=0.9,ms;q=0.8"})
    e=sess.post('https://api.nike.com/idn/shim/oauth/2.0/token',json=m_login_data,verify=False,timeout=30,proxies={"https":prox}).json()
    token=e["access_token"]
    ee=sess.get("https://unite.nike.com/auth/slcheck_cookies/v1?appVersion=417&experienceVersion=352&uxid=com.nike.commerce.nikedotcom.web&locale=en_US&backendEnvironment=identity&browser=Google%20Inc.&os=undefined&mobile=false&native=false&visit=1&visitor="+uid+"&atgSync=true&uxId=com.nike.commerce.nikedotcom.web&cookieType=N",proxies={"https":prox},headers={"Origin":"https://www.nike.com","Referer":"https://www.nike.com/us/en_us/","Authorization":("Bearer "+token),"Accept":"*/*","Accept-Encoding":"gzip, deflate, br","Accept-Language":"en-US,en;q=0.9,ms;q=0.8"})
    ee=sess.post("https://secure-store.nike.com/nikestore/html/services/orders/orderReturnHistory",proxies={"https":prox},headers={"X-Requested-With":"XMLHttpRequest","Origin":"https://secure-store.nike.com","Content-Type":"application/x-www-form-urlencoded","Referer":"https://secure-store.nike.com/common/content/endpoint.html","Accept":"*/*","Accept-Encoding":"gzip, deflate, br","Accept-Language":"en-US,en;q=0.9,ms;q=0.8"},data="lang_locale=en_US&country=US&deviceType=desktop")
    ee=sess.post("https://secure-store.nike.com/nikestore/html/services/orders/orderReturnHistory",proxies={"https":prox},headers={"X-Requested-With":"XMLHttpRequest","Origin":"https://secure-store.nike.com","Content-Type":"application/x-www-form-urlencoded","Referer":"https://secure-store.nike.com/common/content/endpoint.html","Accept":"*/*","Accept-Encoding":"gzip, deflate, br","Accept-Language":"en-US,en;q=0.9,ms;q=0.8"},data="lang_locale=en_US&country=US&deviceType=desktop")
    print (ee.text)
    ee=ee.json()
    for ps in ee["data"]:
        with globallock:
            vb=open(OUTPUTFILE,'a')
            vb.write(v[0]+"\t"+ps["id"]+"\t"+ps["status"]+"\n")
            vb.close()
vl=open(ACCOUNTFILE,'r').read().split("\n")
import Queue
vq=Queue.Queue()
for pl in vl:
    pl=pl.strip()
    if pl!="":
        vq.put(pl)
def dochecks():
    while True:
        try:
            b=vq.get_nowait()
        except:
            return
        try:
            checkacc(b)
        except Exception as e:
            print(e + str(e))
            vq.put(b)
from threading import Thread,Lock
globallock=Lock()
for i in range(0,MAXTHREADS):
    Thread(target=dochecks).start()