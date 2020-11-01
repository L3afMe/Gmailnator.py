# Gmailnator.py

Python wrapper to access [Gmailnator](https://gmailnator.com/) programmatically

---

## What is [Gmailnator](https://gmailnator.com/)?

Gmailnator is a free service that allows getting instant temporary email it is also known as "tempmail", "10 minute mail", "throw away mail", "disposable mail", fake email, and "trash mail". It is used to prevent spam into your personal email address. Most of the sites require to register in order to view content, post comments,or download files like forums, blogs, public WI-FI spots, etc. you can use gmailnator to get instant email without using your real email address.

Gmailnator is the most advanced temporary email service on the web because it offers you to use a Gmail email address in which other temp mail providers are not supported.

---

## Warning

Never use temporary mail for important information. It is a public email and can be accessed by anyone and your mail address is only temporary. Gmailnator email messages are auto-deleted after 24 hours and has a 7 Days Backup of all Emails.

---

## Example

```python
import gmailnator

csrf_token, email = gmailnator.generate_email()
print(f'Email: {email}')
print(f'Token: {csrf_token}')
input('Send email, wait a few minutes to ensure that it has been received then press enter to continue...')
emails = gmailnator.check_emails(csrf_token, email)
print(f'Got {len(emails)} emails')
for mail in emails:
    print(f'Subject: {mail["subject"]}')
    print(f'Body: {mail["body"]}')
    print(f'Link: {mail["link"]}')
    print(f'Time: {mail["time"]}')
    print(f'Full body: {gmailnator.get_message(mail["link"], csrf_token)}')

```