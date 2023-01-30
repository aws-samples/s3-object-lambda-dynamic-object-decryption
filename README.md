## Decrypting object with S3-Object Lambda
Amazon S3 lunched Object lambda 2021, via this Amazon S3 capabilities so many possibilities opened up to transform the s3 object centrally. This S3 capabililties can be used with many AWS services. More examples and documentation can be find here - https://aws.amazon.com/s3/features/object-lambda/

There are many Customers who use customer side Encryption for their S3 objects. It becomes a very high maintance job to maintain and distribute keys to all their users. The Solution sample proposed here describes how to store encryption key in AWS Secrets Manager as a datastore. This sample code utilizes the Lambda extension for Secert Manager to retieve key and usage of S3 Lambda Object to decrypt the S3 object before rendering to the users.

These files contains the sample code, which can be leavered to implement more extensive decryption capabilities.

### lambda_function.py
This is a python script for decryption Lambda function. This python Lambda function, connects to AWS Secrets Manager via Lambda connections api and extract secret decryption, decrypt the targeted Amazon S3 object and return the object to the client.

### requirements.txt
Define the required python libraries
  1. requests
  2. cryptography

### template.yaml
This is a SAM template to deplpy the code in the env. This deploys Lambda function, configures Secrets Manager connections to Lambda function, create S3 unique bucket, S3 Access Points for corresponding bucket, and S3 Object Lambda Access Points for corresponding Access Points.

### sample files
### s3encryptionkey
This is a sample key-pair file for secret. 
### test-doc.txt
This is a sample encrypted file. This is encypted via s3encryptionkey.

## Getting started
### Prerequisite
Upload sample key-pair to AWS Secrets Manager.
### Deploy code
The Serverless Application Model Command Line (SAM CLI) requires following tools -
  1. SAM CLI [download here](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
  2. Docker [download here](https://hub.docker.com/search/?offering=community&q=)

To build and deploy application for the first time, run below commands - 
  #### 
    sam build
    sam deploy --guided

While guided deploying application with sam will prompt severally - 
  #### Stack Name: 
  Choose unique stack name. This will create unique stack in cloud formation.
  #### AWS region: 
  Select AWS region code needs to be deployed
  #### Confirm changes before deploy:
  If set to Yes, changes will be shown for manual confirmation, if set to No, SAM will deploy changes without manual verification.
  
  To see more information SAM commands please [review here](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-cli-command-reference-sam-deploy.html)
### Post deployment
Copy sample test-doc.txt in the newly created S3 bucket.

## Test the Sample
### Postman
You can use Postman get request to test the sample. https:// <AccessPointName> - <AccountId>.s3-object-lambda.<Region>.amazonaws.com
### AWS Cloudshell
  
### Clean up
  ####
    sam delete

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

