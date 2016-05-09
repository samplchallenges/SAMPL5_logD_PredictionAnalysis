#!/bin/env python

"""Build single text file containing comma separated list of e-mail addresses of participants, for mass e-mailing the group. Remember to put it in the BCC field!"""

#Read file
file = open('SAMPL5_users.csv', 'r')
emaillist = []
lines = file.readlines()

#Loop over lines, pull e-mails
for line in lines[1:]: 
    email = line.split(',')[2]
    if email not in emaillist:
        emaillist.append(email)

#Dump to file
file = open('../DataFiles/emaillist.txt', 'w')
#Compose string
str = ''
for email in emaillist:
    str += email+', '
file.write(str)
file.close()
