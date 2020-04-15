
import csv
import pandas as pd 
from google.cloud import language_v1
from google.cloud.language_v1 import enums

trendQuestions= pd.read_csv("questions.csv")
print(trendQuestions)

df=pd.DataFrame()
def analyze_entities(text_content):
    client = language_v1.LanguageServiceClient()
    type_ = enums.Document.Type.PLAIN_TEXT
    language = "en"
    document = {"content": text_content, "type": type_, "language": language}

    # Available values: NONE, UTF8, UTF16, UTF32
    encoding_type = enums.EncodingType.UTF8
    response = client.analyze_entities(document, encoding_type=encoding_type)
    entities=response.entities
    goog_entities=[]
   
    # Loop through entitites returned from the API
    for e in entities:
        entity=e.name
        e_type=enums.Entity.Type(e.type).name
        saliance_score=e.salience
        mentions=e.mentions
        metadata=[]
        if e.metadata:
            for k, v in e.metadata.items():
                metadatas={k:v}
                metadata.append(metadatas)
        else: 
            metadata.append("None")
        google_entities= {'questions':text_content,'entity':entity,'types':e_type,'salience':saliance_score,
        'mentions':mentions,'metadata':metadata}
        goog_entities.append(google_entities)
        return goog_entities

for i,question in trendQuestions.iterrows():
    
    results=analyze_entities(question[0])
    print(results[0]['entity'])
  

