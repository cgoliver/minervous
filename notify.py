import smtplib

def send_mail(gmail_user, gmail_password, to, email_text):
    try:  
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()   # optional
        server.starttls()
        #login
        server.login(gmail_user, gmail_password)
        # ...send emails
        print(email_text)
        # server_ssl.sendmail(gmail_user, to, email_text)
        server.sendmail(gmail_user, to, email_text)
        server.close()
    except Exception as e:  
        print(e)

