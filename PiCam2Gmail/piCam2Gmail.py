# This sketch takes a photo from the PiCam and sends it from a gmail account
# to a recipient.

from picamera import PiCamera
import time
from gpiozero import Button
import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart

button = Button(26)
myCamera = PiCamera()

COMMASPACE = ', '

def saveImage():
    global event

    event = time.asctime() # sample the current time and date
    file = open('/home/pi/Documents/myCamPics/{}.jpg'.format(event), 'wb')

    myCamera.start_preview() # optional, open a live preview
    time.sleep(3)
    myCamera.capture(file) # take a picture, store as jpeg
    file.close()
    myCamera.stop_preview() # close the live preview

def sendEmail():
    sender = 'SENDEREMAIL' # senders email address
    gmail_password = 'SENDERPASSWORD' # senders password - keep this document secure
    recipients = ['RECIPIENTEMAIL'] # recipients email(s) seperated by commas

    # Create the enclosing message
    outer = MIMEMultipart()
    outer['Subject'] = 'New Image From Pi Cam at {}'.format(event)
    outer['To'] = COMMASPACE.join(recipients)
    outer['From'] = sender
    outer.preamble = 'You will not this in a MIME-aware mail reader.\n'

    # List of attachments
    attachments = ['/home/pi/Documents/myCamPics/{}.jpg'.format(event)]

    # Add the attachments to the message
    for file in attachments:
        try:
            with open(file, 'rb') as fp:
                msg = MIMEBase('application', "octet-stream")
                msg.set_payload(fp.read())
            encoders.encode_base64(msg)
            msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
            outer.attach(msg)
        except:
            print("Unable to open one of the attachments. Error: ", sys.exc_info()[0])
            raise

    composed = outer.as_string()

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as s:
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(sender, gmail_password)
            s.sendmail(sender, recipients, composed)
            s.close()
        print("Email Sent!")
    except:
        print("Unable to send the email. Error: ", sys.exc_info()[0])
        raise

def main():
    while True:
        if button.is_pressed:
            print("Button pressed, taking photo...")
            print(time.asctime())
            saveImage()
            print("Image saved. Sending mail...")
            time.sleep(1)
            sendEmail()

if __name__ == '__main__':
    main()
