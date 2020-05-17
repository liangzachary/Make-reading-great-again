import boto3

location = 'book_home/bookaudio.mp3'

session = boto3.Session(
    aws_access_key_id='AKIAYFU3DBC6GP6IFQGL',
    aws_secret_access_key='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',
)
Matthew = session.client('polly', 'us-east-1')

def gen_audio(book_text):
  response = Matthew.synthesize_speech(    
      OutputFormat='mp3',    
      Text=book_text,
      TextType='text',
      VoiceId='Matthew',
      LanguageCode='en-US'
  )
  print(response)
  f = open(location, 'wb')
  f.write(response['AudioStream'].read())
  f.close()