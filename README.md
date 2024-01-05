# AWS-Chatbot
This was a personal project that I created using Amazon Web Services (AWS). This project was focused around creating a Chatbot that could anwser questions about Ball State University's library. I used a Cloud Formation script template (link below) to launch a static website hosted in S3. I then created a Lambda function backend that would be called when the bot didn't recognize the user's questions. It would then log the missed utterances into DynamoDB. I did this so I could update the bot's recognition to different worded phrases and add questions that it didn't have the answer to. Below is a diagram of the architecutre: 


![ChatBotDiagram](https://github.com/nolan-meyer1/AWS-Chatbot/assets/145584308/a3d396ff-fbe2-4988-a05a-6c804524e53c)
Cloud Formation Template Link- https://github.com/aws-samples/aws-lex-web-ui
