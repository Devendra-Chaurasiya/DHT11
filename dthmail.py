# -*- coding: utf-8 -*-
import time
import board
import adafruit_dht
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Set temperature threshold (in Celsius)
TEMP_THRESHOLD = 28  # Change as per your requirement

# Sensor data pin is connected to GPIO 4
sensor = adafruit_dht.DHT11(board.D4)

# Email sending function using SMTP
def send_email(subject, body):
    sender_email = "demoraspi43@gmail.com"  # Sender email (your email)
    receiver_email = "devendrachaurasia12@example.com"  # Replace with recipient's email
    password = "uqyx sluk xtuk iole"  # Use your Gmail password or App Password if 2FA is enabled

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        # Connect to Gmail's SMTP server and send the email
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Secure connection
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
    finally:
        server.quit()

while True:
    try:
        # Read temperature and humidity values from the sensor
        temperature_c = sensor.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = sensor.humidity

        print(f"Temp={temperature_c:0.1f}ºC, Temp={temperature_f:0.1f}ºF, Humidity={humidity:0.1f}%")

        # Check if temperature exceeds threshold
        if temperature_c > TEMP_THRESHOLD:
            # Send an email alert if temperature exceeds the threshold
            subject = "Alert: High Temperature"
            body = f"The temperature has reached {temperature_c:.2f}ºC ({temperature_f:.2f}ºF)."
            send_email(subject, body)

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        sensor.exit()
        raise error

    time.sleep(3.0)

