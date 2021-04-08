import os
import random
from datetime import datetime

import boto3
# from twilio.rest import Client

from config import mail

MEDIA_LOC = 'media'
s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('AWS_SECRET_KEY'),
)

sns = boto3.client(
    'sns',
    region_name='ap-south-1',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('AWS_SECRET_KEY'),
)

# twilio_client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTHTOKEN'))


class Image:

    def save_image(self, file):
        self.image_meta()
        if not self.image_field:
            raise Exception('Image key not specified')
        if not self.save_to:
            raise Exception('Save location not specified')
        timestamp = str(datetime.now().timestamp()).replace('.', '')
        file_path = f"{MEDIA_LOC}/image/{self.save_to}/{timestamp}.{file.filename.split('.')[-1]}"
        s3.upload_fileobj(
            file, os.getenv('S3_BUCKET_NAME'), file_path,
            ExtraArgs={'ACL': 'public-read'}
        )
        file_url = f"https://{os.getenv('S3_BUCKET_NAME')}.s3.{os.getenv('S3_BUCKET_REGION')}.amazonaws.com/{file_path}"
        setattr(self, self.image_field, file_url)


def send_otp(otp, mobile):
    sns.set_sms_attributes(
        attributes={
            'DefaultSMSType': 'Transactional'
        }
    )
    # Send your sms message.
    sns.publish(
        PhoneNumber=mobile,
        Message=f'Wellhest OTP number is {otp}'
    )


def generate_otp():
    return random.randint(100000, 999999)


def send_email(recipient):
    mail.send_message(
        'wellhest_support',
        sender='wellhestcare@gmail.com',
        recipients=[recipient],
        body="""
WELCOME  TO  WELLHEST
_______________________________________________________________




You have successfully registered with wellhest.
Our team will contact you soon helping you put your business on wellhest.


Our best
 wellhest team.

______________________________________________________________


Contact us at
 wellhest@gmail.com
+91 96 2884 2884
+91 96 2885 2885
        """
    )


def send_message(mobile):
    sns.set_sms_attributes(
        attributes={
            'DefaultSMSType': 'Transactional'
        }
    )
    # Send your sms message.
    sns.publish(
        PhoneNumber=mobile,
        Message="""
WELCOME  TO  WELLHEST
_______________________________________________________________




You have successfully registered with wellhest.
Our team will contact you soon helping you put your business on wellhest.


Our best
 wellhest team.

______________________________________________________________


Contact us at
 wellhest@gmail.com
+91 96 2884 2884
+91 96 2885 2885"""
    )
