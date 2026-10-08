"""
Cria a tabela do projeto no DynamoDB.
"""

import os

import boto3

from dotenv import load_dotenv


load_dotenv()


dynamodb = boto3.resource(

    "dynamodb",

    endpoint_url=os.getenv(
        "DYNAMODB_ENDPOINT"
    ),

    region_name=os.getenv(
        "AWS_DEFAULT_REGION",
        "us-east-1"
    ),

    aws_access_key_id=os.getenv(
        "AWS_ACCESS_KEY_ID",
        "test"
    ),

    aws_secret_access_key=os.getenv(
        "AWS_SECRET_ACCESS_KEY",
        "test"
    )
)


table_name = os.getenv(
    "DYNAMODB_TABLE",
    "articles"
)


try:

    table = dynamodb.create_table(

        TableName=table_name,

        KeySchema=[

            {
                "AttributeName":
                    "article_id",

                "KeyType":
                    "HASH"
            }

        ],

        AttributeDefinitions=[

            {
                "AttributeName":
                    "article_id",

                "AttributeType":
                    "S"
            }

        ],

        BillingMode="PAY_PER_REQUEST"
    )

    table.wait_until_exists()

    print(
        f"Tabela '{table_name}' criada."
    )

except dynamodb.meta.client.exceptions.ResourceInUseException:

    print(
        f"Tabela '{table_name}' já existe."
    )