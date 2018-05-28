import os
import boto3
boto3.set_stream_logger(name='botocore')


class PushClient(object):
    def __init__(self):
        ACCESS_KEY = os.getenv('AWS_ACCESS_KEY')
        SECRET_KEY = os.getenv('AWS_SECRET_KEY')
        self.client = boto3.client(
                'sns',
                aws_access_key_id=ACCESS_KEY,
                aws_secret_access_key=SECRET_KEY,
                region_name='us-west-1',
        )
        self.arn = self.create_platform()

    def create_platform(self):
        response = self.client.create_platform_application(
            Name = 'BruinBitePushNotifications',
            Platform = 'APNS_SANDBOX', 
            Attributes = {
                'PlatformCredential': '-----BEGIN
                CERTIFICATE-----\n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\n-----END
                CERTIFICATE-----',
                'PlatformPrincipal': '-----BEGIN PRIVATE
                KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDEDq66hNsYRk0HOmIa9ivs7LjZ0X4FqoI12z4z4D0Z9OVmFG455ZoVps1cKoNRmzqblY68IKz5Yf46inpMBxAw84mF6iw9e3GrBNPS7R6c/SifMypFzccSSBzl5aZCHjiznnaWO+yCo/FYjA/7puyt9v2U/hAJHGHUUjM3mv4wTyelKZ0ogVU1ATKu2YF3cznPTZpezFC1iQW4afLrdIetoL0R303l3wzfD+oaQ2zc9rAgpQHrhgKPb8SRut4HSe88g9kmvMHuO9HhZ5eDUTJBaHkb6xULxp7rhRLniR6jb5MxLTmSwVEHZ5jdprGknh/Ec6LLjD1m0UTenxrMM6JZAgMBAAECggEAZQ04TBS8JKffffE+razieQyOPl62+M6orH+jcPOMKrvKHTI8mgTYxX4i7PVQmBhNPfH5Dsg8v5Ediyji3hrp4oE0CdzoDox4yvADCf2DwODPNjcV+8KTb73Rf0E9z2hqS1JKxyZ9wdwkQkJ23ntsFEJw84F73GZPmjMACRIPH/BVWJDB3ZjbI/QQ1oIOZtG6xWmV8FQEtjz0kEc50m6aJ5QRp/9k9yOh6sKjsCR5JtQsrEmnuPShj2KtCRG9S8gEg8XROnVUvBm0cvHgH8kPksgTqNBEqn0oLvkMEOqYNajze5lOGktFpWHFc4ydHDx8rrGk3z4ZcQURSRSCv1cegQKBgQDpYCJ9kAg6YvO18jmwWUhxc6CGsACCvK+m6tKc2bGLgGaPdhQKOGHPslAyXnESJH0MaZ+4IC6HUR8GN2OV9pSCjVfLxUjl3hV17fwMtmOyopJwrznnx98A+zXJ3bZwPcAzQnQctC1XlGtjKj9DqLXWtpJWiHxwX6hctPk1DJZbqQKBgQDXEGSmB+9J4MD1ms8dtXd9UCGNBJwYtgPrIrdmm8/CHXZApUwaIot8h49W8rZ6UFWJ2l13TqO5/qUqsxTSRBjoVPfbodY047KVTSQ74ueL6gyqCmWyejjyOFvAfmKyo6t4e7X0aPJUT/+2XnwH8iYqdS63ozCYoMxiVl0e6mG/MQKBgQDewqCpcb4o3SL73UYrik2X3WKwrXcPU8Pmc+atSS4rllhPP8pJJyBV/EKIkZUkWCf0nS2Tt0QybcBLUrt//WosY3YWTy4SHDYn5w3bpIztijh1zwxarXGzohXppfPql0bKpvfmHiXZnxYSBdV1Y6iOVp7Acm81ZFl0hFoLxQQQYQKBgQCyc5vQWM0pVCFIqogpcqYPiSoNxUFxD7b4qPndXnRp8eBpi782AGwVjLZXw1W+8GHJ3TOpB8u7TZznbWldf7vbLIXt7L+9ayKH2Fa0inbvFeokPjRcgCY4dqNLepOS/1QMyToV7+8EHs1kGcp5HWil2k5FelecjfCJuHfUa09oQQKBgBI9QqoQdQ5JmXxQdOA2vLI5nzpMYhhh7ygNqGTlHr3stBDh9fgZxZm+M6Le5PYYDbHX29behBrRU4TnOzMI3DzftM90p9q/Y8hG8SS+p1iYgnTikkycSlHyuG8uhfNUpkfXDCkIadHlW/ZqqkhFj1tnZquN/l9aM+zUWkFKPEUJ\n-----END
                PRIVATE KEY-----',
            },
        )
        arn = response.get('PlatformApplicationArn')
        return arn

    def create_endpoint(self, device_token):
        arn = self.arn
        response = self.client.create_platform_endpoint(
            PlatformApplicationArn = arn,
            Token=device_token,
            CustomUserData='',
        )
        endpoint_arn = response.get('EndpointArn')
        return endpoint_arn

    def send_apn(self, device_token, message="", subject=""):
        arn = self.arn
        response = self.client.publish(
            TargetArn=self.create_endpoint(arn, device_token),
            Message=message,
            Subject=subject,
            # MessageAttributes={
            #     "" : {
            #         "DataType":"String",
            #     }
            # },
        )

        message_id = response.get('MessageId')
        return message_id

