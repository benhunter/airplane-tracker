#!/usr/bin/env python3


# Check a list of airplane registration numbers and email when a flight is found.
# List regisration numbers in registration_numbers.txt
# Needs RapidAPI key and Gmail credentials.

import re
import http.client
import smtplib
import sys


def main():
    if len(sys.argv) != 3:
        help()
        sys.exit(1)

    registration_numbers_filename = sys.argv[1]
    rapidapi_key = sys.argv[2]

    # open the text file and read the registration numbers into a list
    with open(registration_numbers_filename, "r") as f:
        registration_numbers = f.read().splitlines()
        registration_numbers = filter(lambda x: len(x) > 0, registration_numbers)

    # Gmail credentials, note no longer able to use Less Secure APPs
    gmail_user = "gmail address"
    gmail_password = "gmail app password"
    conn = http.client.HTTPSConnection("adsbexchange-com1.p.rapidapi.com")
    headers = {
        'X-RapidAPI-Key': rapidapi_key,
        'X-RapidAPI-Host': "adsbexchange-com1.p.rapidapi.com"
        }

    # iterate over the registration numbers
    for registration_number in registration_numbers:
        path = f"/v2/registration/{registration_number}/"
        conn.request("GET", path, headers=headers)
        res = conn.getresponse()
        data = res.read()
        data_str = data.decode("utf-8").strip()
        match = re.search('"r":"([A-Z0-9]{1,6})"', data_str)

        if match:
            # registration number found
            print(f"Plane found with registration number {registration_number}")

            # send an email
            to = "insert email address to send to"
            subject = "Plane found"
            body = f"We found the plane {registration_number}. Go to https://globe.adsbexchange.com now and search for it."
            email_text = f"To: {to}\nSubject: {subject}\n\n{body}"

            try:
                server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
                server.ehlo()
                server.login(gmail_user, gmail_password)
                server.sendmail(gmail_user, to, email_text)
                server.close()
                print("Email sent!")
            except:
                print("Something went wrong and the email was not sent.")

        else:
            # registration number not found
            print(f"No plane found with registration number {registration_number}")


def help():
    print("Usage: ./airplane_tracker.py <registration_numbers_filename> <RapidAPI_key>")


if __name__ == "__main__":
    main()
