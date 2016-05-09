# Written by David L Mobley for SAMPL4
# Adapted by Caitlin C Bannan and David L Mobley for SAMPL5
# Used to e-mail participants when we want to send information to an individual participant
import os
import pickle
import smtplib
import email
import email.mime.application

def send_email( attachments, bodytext, titletext, smtp_session, emailaddress):
    """Send e-mails to SAMPL participants, returning generic files (i.e. comparing all participants), files specific to their user id, and so on.

    ARGUMENTS:
      - attachments: Files to attach
      - bodytext: Text of email
      - titletext: Title of email
      - smtp_session: Already open smtp session handle
      - emailaddress: Who to send to
From is assumed to be dmobley@gmail.com.

    Attachments currently handled are assumed to be text or PDF.
"""

    #Code loosely based on http://stackoverflow.com/questions/1966073/how-do-i-send-attachments-using-smtp
    msg = email.mime.Multipart.MIMEMultipart()
    msg['Subject'] = titletext
    msg['From'] = 'dmobley@gmail.com'

    #DEBUG BY CHANGING OUTGOING EMAIL ADDRESS
    #emailaddress='dmobley@uci.edu'
    #END DEBUG

    msg['To'] = emailaddress

    #Handle body as an attachment
    body = email.mime.Text.MIMEText(bodytext)
    msg.attach(body)

    #Register attachment types
    pdffiles = [ filenm for filenm in attachments if '.pdf' in filenm.lower() ]
    txtfiles = [ filenm for filenm in attachments if '.txt' in filenm.lower() ]

    #Attach PDFs
    for filename in pdffiles:
        fp = open(filename, 'rb')
        att = email.mime.application.MIMEApplication( fp.read(), _subtype = "pdf")
        fp.close()
        att.add_header('Content-Disposition', 'attachment', filename = os.path.basename(filename) )
        msg.attach(att)
    #Attach text files
    for filename in txtfiles:
        #att = email.MIMEBase('application', "octet-stream")
        #att.set_payload( open(filenm, 'rb').read() )
        att = email.mime.text.MIMEText( open(filename, 'rb').read(), _subtype='plain' )
        #email.Encoders.encode_base64(part)
        att.add_header('Content-Disposition', 'attachment; filename = "%s"' % os.path.basename(filename) )
        msg.attach(att)
        print "Text file:", filename

    #Send mail
    smtp_session.sendmail( 'dmobley@gmail.com', emailaddress, msg.as_string() )


def start_session( user, temppw):
    """Open SMTP session and return handle"""

    #Store various e-mail info
    server = 'smtp.gmail.com'
    port = 587
    session = smtplib.SMTP(server, port)
    session.ehlo()
    session.starttls()
    session.ehlo()
    session.login( user,  temppw)

    return session

# Load dictionary so I can get contact information
database = pickle.load(open('DataFiles/predictions.p','rb'))

#EMAIL SETTINGS
sender = 'dmobley@gmail.com'
temppw = 'blather'

# ======================================================================
# Insert body of e-mail here:
# I had to assign everyone a Submission Number in order to have IDs down to 2 digits, I name in num in the for loop below, you'll probably want to tell people what their number is.
# I've included First and Last Name in the for loop below if you want them
# I included all of the error files in the attachement list for now, but if you're putting them in the 

#OPEN EMAIL SESSION
print "Starting e-mail session"
session = start_session( sender, temppw)


#Loop over submission ids, building lists of attachments and sending messages
for num, e in database.items():
#for sid, e in database.items()[2:3]: #Temporary debugging
    #Build subject line
    subject = "SAMPL5 distribution coefficient results for submission %s" % sid 
    #CONTACT INFORMATION:
    firstName = e['firstName']
    lastName = e['lastName']
    emailaddress = e['email'] 
    # This is the 'Name:' given to the entry, I don't know if it's helpful or not
    shortName = e['name:']
    # This is where their data file is stored, once again, I don't know if it's helpful. It has the format "./predictionFiles/submissionID-282-DC-anyname-num.txt"
    fileName = e['fileName']
    # SUBMISSION NUMBER:

    #Build body text of e-mail
    body="""Dear SAMPL5 participant,

This e-mail provides preliminary results for the SAMPL5 distribution coefficient challenge. You should have already received overall statistics comparing the performance of your submissions to that of others in the challenge, and these should also be posted to the SAMPL5 website shortly. But this e-mail provides a scatter plot of your calculated values versus experiment, and a Q-Q clot comparing how well your model uncertainty estimates matched up with the actual error in your predictions. (This methodology is explained in our report on the SAMPL4 challenge, available at http://dx.doi.org/10.1007/s10822-014-9718-2; PDF available on request.).

These results should still be considered somewhat preliminary, as some re-inspection of the experimental data is ongoing. Additionally, we plan on calculating some new metrics which may result in additional plots being provided. But this should provide a good starting point, we hope.

This e-mail in particular concerns your submission ID %s, method name %s, with file name %s, which we have assigned the short submission number %s for the purposes of our graphs, etc. 

We hope to see you at the workshop in San Diego shortly, and please don't hesitate to contact me personally with any questions.

Sincerely,
David Mobley
dmobley@uci.edu""" % (sid, shortName[0], fileName, num) 
 
    #Build list of files
    # This includes all of the histogram plots and the table of data, delete the first line below if you only want to e-mail the individualized plots and point people to the website for everything else
    #attachments = glob.glob("statsPlots/*")
    attachments = []
    attachments.append("QQPlots/%02d_QQ.pdf" % num) 
    attachments.append("ComparePlots/%02d_compare.pdf" % num) 

    #Send mail
    send_email( attachments, body, subject, session, emailaddress)

    print "Emailed %s about submission %s..." % ( emailaddress, sid)
    #raw_input()

session.close()    
