import boto3
import json

def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        text = body.get('text')
        target_language = body.get('targetLanguageCode')

        if not text or not target_language:
            return {
                "statusCode": 400,
                "body": {"message": "Please provide text and target language code."}
            }

        translate = boto3.client('translate')
        response = translate.translate_text(
            Text=text,
            SourceLanguageCode='en',  # Assuming English source
            TargetLanguageCode=target_language
        )

        return {
            "statusCode": 200,
            "body": {"translatedText": response.get("TranslatedText")}
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "body": {"message": f"Error translating text: {str(e)}"}
        }
