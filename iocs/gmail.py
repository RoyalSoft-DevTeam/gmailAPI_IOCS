# import poplib
# import string, random
# # import StringIO, rfc822
# import logging
#
# SERVER = "pop.gmail.com"
# USER = "smile dev"
# PASSWORD = "ghun122919"
#
# # connect to server
# logging.debug('connecting to ' + SERVER)
# server = poplib.POP3_SSL(SERVER)
# #server = poplib.POP3(SERVER)
#
# # log in
# logging.debug('log in')
#
# server.user(USER)
# server.pass_(PASSWORD)


import imaplib
import email

server = 'imap.google.com'
user = 'smiledev10162@gmail.com'
password = 'ghun122919'

mb = imaplib.IMAP4_SSL(server, port)
rv, mesasge = mb.login(user, password)
# 'OK', [b'LOGIN completed']
rv, num_emails = M.select('Inbox')
# 'OK', [b'22']

# Get unread messages
rv, messages = M.search(None, 'UNSEEN')
# 'OK', [b'21 22']

# Download a message
typ, data = M.fetch(b'21', '(RFC822)')

# Parse the email
msg = email.message_from_bytes(data[0][1])
print(msg['From'], ":", msg['Subject'])

# Print the Plain Text (is this always the plain text?)
print(msg.get_payload()[0].get_payload())