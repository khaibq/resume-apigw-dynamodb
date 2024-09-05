<!-- TOC -->
  * [Deploy AWS API Gateway to read and update DynamoDB without Lambda](#deploy-aws-api-gateway-to-read-and-update-dynamodb-without-lambda)
    * [1. CDK (Python)](#1-cdk-python)
    * [2. Install required packages](#2-install-required-packages)
    * [3. DynamoDB table created<!-- TOC -->](#3-dynamodb-table-created---toc---)
    * [4. Api Gateway created](#4-api-gateway-created)
    * [5. Integration](#5-integration)
    * [6. Output value for later use.](#6-output-value-for-later-use)
    * [7. Test and deploy.](#7-test-and-deploy)
    * [8. Cleanup](#8-cleanup)
<!-- TOC -->
## Deploy AWS API Gateway to read and update DynamoDB without Lambda
### 1. CDK (Python)
    - cdk init app --language python
### 2. Install required packages
    - pip install -r requirements.txt
### 3. DynamoDB table created
    - From CDK API documentation - [Table](https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_dynamodb/Table.html#aws_cdk.aws_dynamodb.Table)
### 4. Api Gateway
    - From CDK API documentation - [API Gateway](https://docs.aws.amazon.com/cdk/api/v2/python/aws_cdk.aws_apigateway/README.html)
### 5. Integration and add GET & POST method
### 6. Output value for later use.
    - TableName: ResumeApiGwStack-resumeTable****
    - APIUrl: https://****.execute-api.zone***.amazonaws.com/prod/
### 7. Test and deploy.
    - cdk synth
    - cdk deploy
### 8. Cleanup
    - cdk destroy
