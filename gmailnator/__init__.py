# ##############################################################################
#     By TOT900                                   GPT-2                        #
#  Clover - __init__.py                                                        #
#  Copyright (C) Public Domain                                                 #
#    FREE FOR EVERYONE TO DO WHATEVER THEY WANT-                               #
#                          -AND RELEASE IT UNDER THEIR NAME                    #
# ##############################################################################
import requests,time,re
from bs4 import BeautifulSoup

class Gmailnator:
    def __init__(self):
        self.s = requests.Session()
        self.email = str()

        self.csrf_gmailnator_cookie = str()
        self.ci_session = str()
        self.__cfduid = str()

    def getEmail(self):
        r =  self.s.get("https://www.gmailnator.com/")

        self.csrf_gmailnator_cookie=self.s.cookies['csrf_gmailnator_cookie']
        self.ci_session=self.s.cookies['ci_session']
        self.__cfduid=self.s.cookies['__cfduid']

        headers = {
            'authority': 'www.gmailnator.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'accept': '*/*',
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'cookie':f'ci_session={ self.ci_session }; __cfduid={ self.__cfduid }; csrf_gmailnator_cookie={ self.csrf_gmailnator_cookie };',
            'origin': 'https://www.gmailnator.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.gmailnator.com/',
            'accept-language': 'en-US,en;q=0.9',
        }
        data = [
            ('csrf_gmailnator_token', self.csrf_gmailnator_cookie),
            ('action', 'GenerateEmail'),
            ('data[]', '3'),
        ]
        r = self.s.post("https://www.gmailnator.com/index/indexquery",cookies=self.s.cookies,data=data)
        self.email = r.text
        return self.email
    def receiveInbox(self):
        headers = {
            'authority': 'www.gmailnator.com',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.104 Safari/537.36',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://www.gmailnator.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.gmailnator.com/inbox/',
            'accept-language': 'en-US,en;q=0.9',
            'cookie':f'ci_session={ self.ci_session }; __cfduid={ self.__cfduid }; csrf_gmailnator_cookie={ self.csrf_gmailnator_cookie };',
        }
        #self.email='sea.n.bern.ar.d.e.t.tet.mp@gmail.com'#testing and debugging if needed
        data = {
            'csrf_gmailnator_token': self.csrf_gmailnator_cookie,
            'action': 'LoadMailList',
            'Email_address': self.email#'sea.n.bern.ar.d.e.t.tet.mp@gmail.com'#self.email
        }

        emailNodots = (self.email).strip('@gmail.com')
        while "." in emailNodots:
            emailNodots = emailNodots.replace('.', '')
        
        while True:
            try:
                r = self.s.post('https://www.gmailnator.com/mailbox/mailboxquery', headers=headers, data=data)
                
                if len(r.json()) >= 1:#if the 
                    responseJson= (r.json() )[0]#Always the latest email (if needed older one you may use a FOR LOOP)
                    
                    r = re.compile('(?<=href=").*?(?=")')
                    viewEmail = r.findall(responseJson['content'])[0]
                    messageid = viewEmail.split("#")[1]
                    
                    print(messageid)
                    data = {
                        'csrf_gmailnator_token': self.csrf_gmailnator_cookie,
                        'action': 'get_message',
                        'message_id': messageid,
                        'email': emailNodots,
                    }

                    while True:
                        try:
                            print("wtf?")
                            r = self.s.post('https://www.gmailnator.com/mailbox/get_single_message/', headers=headers, data=data)
                            ###        ######         ###
                            ###  r.json()['content']  ###
                            ###  r.json()['subject']  ###
                            return (r.json()['content'])
                        except:
                            pass
                        time.sleep(5)
                time.sleep(5)
            except:
                pass

#Gmailnator.getEmail() == returns a email
#Gmailnator.receiveInbox() returns the 'contents' of the latest email

"""Example:
#Gmailnator = Gmailnator()
#print(Gmailnator.getEmail())
#print(Gmailnator.receiveInbox())
"""
### Optional for regexing herf=""
#receiveEmail = email.receiveInbox()
# match = re.search(r'href=[\'"]?([^\'" >]+)', receiveEmail)
# if match:
#     receiveEmail_Url = match.group(1)
# print(receiveEmail_Url)

