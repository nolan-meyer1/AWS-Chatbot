import json
import boto3
from datetime import datetime
import getpass
"""
Lambda function that logs missed utterances
to a DynamoDB database. It logs the missed 
utterance, timestamp, and user name. It also
has content filtration that sends an email with
the inapropriate response, timestamp, and user name to
whoever would like to monitor the application. 

Nolan Meyer

January 4, 2024
"""

#Lambda handler that takes in an event
def lambda_handler(event, context):

    #Varaibles for crafting response
    slots = event['sessionState']['intent']['slots']
    intent = event['sessionState']['intent']['name']

    #Missed utterance, Time Stamp, User name
    missedUtterance = event["inputTranscript"]
    timeStamp = str(datetime.now())
    userName = getpass.getuser()

    #Create a dynamoDB client
    dynamodb = boto3.resource("dynamodb")
    table_name = "Missed-Utterance"
    table = dynamodb.Table(table_name)

    #Puts the item in the the tabel if it's not already in the table
    keyValues = table.get_item(Key ={"utterance": missedUtterance})

    if "Item" not in keyValues:
        table.put_item(Item = {"utterance": missedUtterance, "timeStamp": timeStamp, "userName": userName})

        #Checks if the content is negative
        if event["interpretations"][0]["sentimentResponse"]["sentiment"] == "NEGATIVE":
            
            #Creates a client and pushes out a notification to a topic that contains emails
            client = boto3.client("sns")
            result = client.publish(TopicArn = "arn:aws:sns:us-east-1:693700037996:LibraryBot",Subject = "Flagged Response", Message = f"Our systems has flagged '{missedUtterance}'. This was done at {timeStamp} by the user '{userName}'.")

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

            #Response returned if the message hasn't been logged before and the response isn't negative
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