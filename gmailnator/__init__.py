# ##############################################################################
#                                                                              #
#  Clover - __init__.py                                                        #
#  Copyright (C) 2020 L3af                                                     #
#                                                                              #
#  This program is free software: you can redistribute it and/or modify it     #
#  under the terms of the GNU General Public License as published by the       #
#  Free Software Foundation, either version 3 of the License, or (at your      #
#  option) any later version.                                                  #
#                                                                              #
#  This program is distributed in the hope that it will be useful, but         #
#  WITHOUT ANY WARRANTY; without even the implied warranty of                  #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See  the GNU General   #
#  Public License for more details.                                            #
#                                                                              #
#  You should have received a copy of the GNU General Public License           #
#  along with this program. If not, see <https://www.gnu.org/licenses/>.       #
#                                                                              #
# ##############################################################################
import json
import re
from typing import Dict, List, Optional, Tuple
from urllib import parse

import requests
from requests import Response


def get_token(html: str) -> Optional[str]:
    """
    Extracts csrf token from gmailnator HTML body

    :param html: HTML body to extract csrf token from
    :return: csrf token if found, else None
    """
    csrf_match: List[str] = re.findall('(?<=csrf-token" content=")(?:(?!").)*', html)
    if len(csrf_match) == 0:
        return None
    return csrf_match[0]


def get_new_csrf_token(email: str) -> Optional[str]:
    return get_token(requests.get(f'https://gmailnator.com/inbox/#{email}', headers = {
        'Accept'         : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-US,en;q=0.5', 'Connection': 'keep-alive',
        'DNT'            : '1', 'Host': 'gmailnator.com', 'Upgrade-Insecure-Requests': '1',
        'User-Agent'     : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
    }).text)


def generate_email() -> Optional[Tuple[str, str]]:
    """
    Generates csrf token and email address

    :return: csrf token and email address
    """
    
    res: Response = requests.get('https://gmailnator.com/', headers = {
        'Accept'         : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-US,en;q=0.5',
        'Connection'     : 'keep-alive', 'DNT': '1', 'Host': 'gmailnator.com', 'Upgrade-Insecure-Requests': '1',
        'User-Agent'     : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0'
    })
    
    csrf_token: str = get_token(res.text)
    if not csrf_token:
        return None
    
    body: str = f'csrf_gmailnator_token={csrf_token}&action=GenerateEmail&data%5B%5D=2&data%5B%5D=1&data%5B%5D=3'
    
    res: Response = requests.post(f'https://gmailnator.com/index/indexquery', data = body, headers = {
        'Accept'          : '*/*',
        'Accept-Encoding' : 'gzip, deflate, br',
        'Accept-Language' : 'en-US,en;q=0.9',
        'Connection'      : 'keep-alive',
        'Content-Length'  : str(len(body)),
        'Content-Type'    : 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie'          : f'csrf_gmailnator_cookie={csrf_token}',
        'DNT'             : '1',
        'Host'            : 'gmailnator.com',
        'Origin'          : 'https://gmailnator.com',
        'Referer'         : 'https://gmailnator.com/',
        'TE'              : 'Trailers',
        'User-Agent'      : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
        'X-Requested-With': 'XMLHttpRequest'
    })
    
    return csrf_token, res.text


def check_emails(csrf_token: str, email: str) -> Optional[List[Dict[str, str]]]:
    """
    Gets mail from specified email

    :param csrf_token: token generated alongside with email
    :param email: email to get mail from
    :return: List of mail in mailbox
    """
    
    if not re.match('^(([^<>()\[\].,;:s@"]+(.[^<>()\[\].,;:s@"]+)*)|(".+"))@gmail.com', email):
        return None
    body: str = f'csrf_gmailnator_token={csrf_token}&action=LoadMailList&Email_address={parse.quote_plus(email)}'
    
    res: Response = requests.post(f'https://gmailnator.com/mailbox/mailboxquery', data = body, headers = {
        'Accept'          : 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding' : 'gzip, deflate, br',
        'Accept-Language' : 'en-GB,en;q=0.9',
        'Connection'      : 'keep-alive',
        'Content-Length'  : str(len(body)),
        'Content-Type'    : 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie'          : f'csrf_gmailnator_cookie={csrf_token}',
        'DNT'             : '1',
        'Host'            : 'gmailnator.com',
        'Origin'          : 'https://gmailnator.com',
        'Referer'         : 'https://gmailnator.com/inbox/',
        'TE'              : 'Trailers',
        'User-Agent'      : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
        'X-Requested-With': 'XMLHttpRequest'
    })
    
    data: json = json.loads(res.text)
    emails: List[Dict[str, str]] = []
    for email_data in data:
        email_data = str(email_data)
        matches = re.findall('(?<=<td>)(?:(?!<).)*', email_data)
        subject: str = str(matches[0])
        body: str = str(matches[1])
        link: str = str(re.findall('(?<=a href=\\")(?:(?!\\").)*', email_data)[0])
        time: str = str(re.findall('(?<=<td class=\\"text-right\\">)(?:(?!<).)*', email_data)[0])
        emails.append({
            'subject': subject,
            'body'   : body,
            'link'   : link,
            'time'   : time
        })
    
    return emails


def get_message(mail_link: str, csrf_token: str) -> Optional[str]:
    """
    Gets full body from main link

    :param mail_link: Mail link to get details from
    :param csrf_token: csrf token generated alongside the email address
    :return: HTML mail body as string
    """
    
    if len(mail_link) == 0 or len(csrf_token) == 0:
        return None
    
    email: str = re.findall('(?<=.com/)(?:(?!/).)*', mail_link)[0]
    message_id: str = re.findall('(?<=#).*', mail_link)[0]
    
    body: str = f'csrf_gmailnator_token={parse.quote_plus(csrf_token)}&action=get_message' \
                f'&message_id={parse.quote_plus(message_id)}&email={parse.quote_plus(email)}'
    
    res: Response = requests.post(f'https://gmailnator.com/mailbox/get_single_message', data = body, headers = {
        'Accept'          : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding' : 'gzip, deflate, br',
        'Accept-Language' : 'en-US,en;q=0.5',
        'Connection'      : 'keep-alive',
        'Content-Length'  : str(len(body)),
        'Content-Type'    : 'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie'          : f'csrf_gmailnator_cookie={csrf_token}',
        'DNT'             : '1',
        'Host'            : 'gmailnator.com',
        'Origin'          : 'https://gmailnator.com/',
        'Referer'         : 'https://gmailnator.com/inbox/',
        'TE'              : 'Trailers',
        'User-Agent'      : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
        'X-Requested-With': 'XMLHttpRequest'
    })
    
    return res.text.split('<hr />')[1]
