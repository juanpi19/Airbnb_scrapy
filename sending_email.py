import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from password import password



def send_mail():
    # Create a multipart message
    msg = MIMEMultipart()
    MESSAGE_BODY = 'Here is the list with possible options for your dream vacation'
    body_part = MIMEText(MESSAGE_BODY, 'plain')
    msg['Subject'] = "Filtered list of possible airbnb's"
    msg['From'] = 'projects.creativity.growth@gmail.com'
    msg['To'] =  'juanpablacho19@gmail.com'
    # Add body to email

    msg.attach(body_part)
    # open and read the CSV file in binary
    with open('filtered_data.csv','rb') as file:
    # Attach the file with filename to the email
        msg.attach(MIMEApplication(file.read(), Name='filtered_data.csv'))

    # Create SMTP object
    smtp_obj = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_obj.starttls()
    # Login to the server
    smtp_obj.login('projects.creativity.growth@gmail.com', password)

    # Convert the message to a string and send it
    smtp_obj.sendmail(msg['From'], msg['To'], msg.as_string())
    #smtp_obj.quit()

if __name__ == "__main__":
    send_mail()
