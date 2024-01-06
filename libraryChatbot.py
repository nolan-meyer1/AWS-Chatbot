import json
import boto3
from datetime import datetime
"""
Lambda function that logs missed utterances
to a DynamoDB database. 

Nolan Meyer

January 4, 2024
"""

#Lambda handler that takes in an event
def lambda_handler(event, context):

    #Varaibles for crafting response
    slots = event['sessionState']['intent']['slots']
    intent = event['sessionState']['intent']['name']

    #Missed utterance and Time Stamp
    missedUtterance = event["inputTranscript"]
    timeStamp = str(datetime.now())

    #Create a dynamoDB client
    dynamodb = boto3.resource("dynamodb")
    table_name = "Missed-Utterance"
    table = dynamodb.Table(table_name)

    #Puts the item in the the tabel if it's not already in the table
    keyValues = table.get_item(Key ={"utterance": missedUtterance})

    if "Item" not in keyValues:
        table.put_item(Item = {"utterance": missedUtterance, "timeStamp": timeStamp})

        #Checks if the content is negative
        if event["interpretations"][0]["sentimentResponse"]["sentiment"] == "NEGATIVE":

            #Response returned if the content is negative
            return {
                "sessionState": {
                    "dialogAction": {
                        "type": "Close"
                    },
                    "intent": {
                        "name": intent,
                        "slots": slots,
                        "state": "Fulfilled"
                    }

                },
                "messages": [
                    {
                        "contentType": "PlainText",
                        "content": "Please refrain from using inapropraite language. Everything is logged and will be reported automatically if necessary."
                    }
                ]
            }

        else:

            #Response returned if the message hasn't been logged before
            return {
                "sessionState": {
                    "dialogAction": {
                        "type": "Close"
                    },
                    "intent": {
                        "name": intent,
                        "slots": slots,
                        "state": "Fulfilled"
                    }

                },
                "messages": [
                    {
                        "contentType": "PlainText",
                        "content": "Sorry I don't know the anwser to that yet! Please try rephrasing your sentence or emailing a librarian at https://lib.bsu.edu/forms/emailalibrarian.php . You can also visit the Library help desk!"
                    }
                ]
            }

    #Response returned to the user if the utterance has already been logged before. 
    else:

        return {
            "sessionState": {
                "dialogAction": {
                    "type": "Close"
                },
                "intent": {
                    "name": intent,
                    "slots": slots,
                    "state": "Fulfilled"
                }

            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": "Hmmmmm. This is a frequently asked question I don't know the answer to yet. I will learn this soon! If you have any other questions email a librarian here https://lib.bsu.edu/forms/emailalibrarian.php . You can also visit the Library help desk!"
                }
            ]
        }