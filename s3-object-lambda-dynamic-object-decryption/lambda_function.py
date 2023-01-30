import json
import requests
import os
import boto3
from cryptography.fernet import Fernet
from botocore.exceptions import ClientError
import requests
import shutil

headers = {"X-Aws-Parameters-Secrets-Token": os.environ.get('AWS_SESSION_TOKEN')}
secrets_extension_http_port = os.environ['PARAMETERS_SECRETS_EXTENSION_HTTP_PORT']
testsecret = 's3encryptionkey'
secrets_extension_endpoint = "http://localhost:" + secrets_extension_http_port + "/secretsmanager/get?secretId=" + testsecret

print(secrets_extension_endpoint)
def get_key():
    r = requests.get(secrets_extension_endpoint, headers=headers)
    print('***'+r.text+'***')
    secret = json.loads(r.text)["SecretString"] # load the Secrets Manager response into a Python dictionary, access the secret
    print(secret)
    print(type(secret))
    key = json.loads(secret)["s3encryptionkey"]
    print(key)
    return key
    
def lambda_handle(event, context):
    print(event)
     
    object_context = event["getObjectContext"]
    request_route = object_context["outputRoute"]
    request_token = object_context["outputToken"]
    user_request_url = event["userRequest"]["url"]
    supporting_access_point_arn = event["configuration"]["supportingAccessPointArn"]
    
    print("USER REQUEST URL: ", user_request_url)
    
    encryptedText = get_s3_file(supporting_access_point_arn)
    
    decryptedText = decrypt_file(encryptedText)
  
    s3Client = boto3.client('s3')
    s3Client.write_get_object_response(
                                #Body = out_file,
                                Body = decryptedText,
                                RequestRoute= request_route,
                                RequestToken= request_token)
    return {'status_code':200}
    

def decrypt_file(encryptedText):
    print("decrypt_file")

    
    key = get_key()
    cipher = Fernet(key)
    
    decryptText = cipher.decrypt(encryptedText)
    print(decryptText)
    
    return decryptText

def get_s3_file(supporting_access_point_arn):
    print('getting s3 obj')
    s3 = boto3.resource('s3')
    s3Obj = s3.Object(supporting_access_point_arn, 'test-doc.txt').get()
    encryptedText = s3Obj['Body'].read()
    encryptedText = encryptedText.decode('utf-8')
    print('encryptedText:', encryptedText)
    return encryptedText
    
