# AWS-Chatbot
This was a personal project that I created using Amazon Web Services (AWS). This project was focused around creating a Chatbot that could anwser questions about Ball State University's library. I used a Cloud Formation script template (link below) to launch a static website hosted in S3. I then created a Lambda function backend that would be called when the bot didn't recognize the user's questions. It would then log the missed utterances into DynamoDB. I did this so I could update the bot's recognition to different worded phrases and add questions that it didn't have the answer to. Lastly, I have a content filtration system using AWS comprehend that does an anylasis on every missed utterance. If the utterance is deemed negative it will send an email using Amazon SNS(Simple Notification Service) to the list of people who have signed up to recieve those types of alerts. The email contains the inapropriate phrase, the time it was said, and the user name of the person who did it. Below is a diagram of the architecutre: 


![Screenshot 2024-01-17 at 9 35 59 AM](https://github.com/nolan-meyer1/AWS-Chatbot/assets/145584308/e91552cf-8d95-478d-8de9-89a1d74e99f4)

Cloud Formation Template Link- https://github.com/aws-samples/aws-lex-web-ui

Current Features:
  1.	Collections Locations
  2.	Printer Costs
  3.	Priniting locations
  4.	Printing Instructions. 
  5.	Direct Users towards research guides and database pages. 
  6.	Library Locations
  7.	Library Hours
  8.	What are ball state’s collections?
  9.	Collection descriptions
  10.	Direct users to library services
  11.	Logs Unrecognized phrases which can be used to update the bot with frequently asked questions it doesn’t understand or the reconigzation of the phrases.
  12.	Has content filtration for inappropriate responses using AWS Comprehend.
  13.	Sends notifications to emails that have signed up to recieve alerts of the inapropriate responses. 

Link to test out project: - https://d264fgbdoxlnp0.cloudfront.net/index.html
