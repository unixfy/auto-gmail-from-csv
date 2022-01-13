import csv
import smtplib

SMTP_HOST = 'smtp.gmail.com'
SMTP_PORT = 587

##########
# CONFIG HERE
##########
SMTP_EMAIL = 'youremail@gmail.com'
SMTP_PASSWORD = 'apppassword'
# Note: If you have MFA enabled, use an app password here
# Otherwise use your real password and enable "less secure apps"
YOUR_NAME = 'John Doe'
SUBJECT = 'An inquiry on something'

EMAIL_TMPL = """From:  {name} <{from_email}>
To: {to_email}
Cc: {cc_email}
Subject: {subject}

Dear {teamName} {teamGender} Swimming,

My name is John Doe and I am a senior at Fake High School in Podunk, Michigan. As an AP Research student, my year long research project is on Fortnite gaming in teams. I was wondering if it would be possible for your team members to potentially be a part of the research. 

This would entail your team members filling out a multiple choice survey evaluating attitudes towards Fortnite. I would appreciate your support and I look forward to hearing back from you.

Thank you,

John Doe
"""


def sendEmails():
    """
    This function reads all the data from "data.csv" and sends templated emails to each email contained within
    :return:
    """
    email_queue = []

    with open('data.csv', mode='r') as csvfile:
        # Read our CSV file into a list of dicts
        read_csv = list(csv.DictReader(csvfile))
        print(f"I read the following data from the CSV: {read_csv}")

        #         Loop through the csv data and queue emails up to send
        for item in read_csv:
            # Replace spaces with commas in the CC email field
            if item['carbonCopiedEmail']:
                item['carbonCopiedEmail'] = item['carbonCopiedEmail'].replace(" ", ",")

            queued_email = EMAIL_TMPL.format(from_email=SMTP_EMAIL, to_email=item['sendEmail'],
                                             cc_email=item['carbonCopiedEmail'], teamName=item['teamName'],
                                             teamGender=item['teamGender'], subject=SUBJECT, name=YOUR_NAME)

            item['generated_message'] = queued_email
            # All to / cc addrs
            item['to_addrs'] = item['sendEmail'] + ',' + item['carbonCopiedEmail']
            email_queue.append(item)

            # print(f"My queue now looks like {str(email_queue)}")

        #         Now we send the emails
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
            smtp.starttls()
            smtp.ehlo()
            smtp.login(SMTP_EMAIL, SMTP_PASSWORD)

            for email in email_queue:
                # Note that smtp.sendmail takes a LIST for to-addrs, not a string
                # that is why we have to use the .split() method on the string
                smtp.sendmail(SMTP_EMAIL, email['to_addrs'].split(','), email['generated_message'])
                print(f"Sent email to {email['to_addrs']}")


sendEmails()
