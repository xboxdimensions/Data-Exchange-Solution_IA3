import smtplib
from config import sysemail,syspassword

to="EMAIL" #their email
link = 'link.com' #Randomised/Unique for each user
smtpObj = smtplib.SMTP('smtp-mail.outlook.com', 587)
smtpObj.ehlo()
smtpObj.starttls()
smtpObj.login(sysemail,syspassword)
SUBJECT = "FSANZ Data Analysis: Reset Password"
TEXT = f"Hello, you requested a password reset.\n Click this link {link}. \n If this was not you, ignore this email." 
message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
smtpObj.sendmail(sysemail,to,message)
smtpObj.quit()