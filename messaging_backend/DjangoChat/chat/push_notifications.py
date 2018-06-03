import os
import boto3
boto3.set_stream_logger(name='botocore')


class PushClient(object):
    def __init__(self):
        ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
        SECRET_KEY = os.getenv('AWS_SECRET_KEY')
        print(ACCESS_KEY, SECRET_KEY)
        self.client = boto3.client(
                'sns',
                aws_access_key_id=ACCESS_KEY,
                aws_secret_access_key=SECRET_KEY,
                region_name='us-west-1',
        )
        #self.arn = self.create_platform()
        self.arn = os.getenv('AWS_ARN')

    def create_platform(self):
        response = self.client.create_platform_application(
            Name = 'BruinBitePushNotifications',
            Platform = 'APNS_SANDBOX', 
            Attributes = {
                'PlatformCredential': '../../../apnsprivatekey.pem',
                'PlatformPrincipal': '../../../apnscert.pem',
            },
        )
        arn = response.get('PlatformApplicationArn')
        return arn

    def create_endpoint(self, device_token):
        arn = self.arn
        response = self.client.create_platform_endpoint(
            PlatformApplicationArn = arn,
            Token=device_token,
        )
        endpoint_arn = response.get('EndpointArn')
        return endpoint_arn

    def send_apn(self, device_token, message=""):
        arn = self.arn
        response = self.client.publish(
            TargetArn=self.create_endpoint(device_token),
            # TargetArn =
            # 'arn:aws:sns:us-west-1:432856342397:endpoint/APNS_SANDBOX/Bruin-Bite-Development/e1f3640a-0fa0-3c9d-8b65-e415f2b320d2',
            Message=message,
            # Subject="Subject",
            # MessageAttributes={
            #     "" : {
            #         "DataType":"String",
            #     }
            # },
        )

        message_id = response.get('MessageId')
        return message_id

