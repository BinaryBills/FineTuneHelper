#Author: BinaryBills
#Creation Date: September 10, 2023
#Date Modified: September 11, 2023
#Purpose: Uploads the training data to OpenAI.
import openai
import os
  
def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile: 
        outfile.write(content)
        
openai.api_key = os.environ.get("OPENAI_API_KEY")

with open("um_dearborn_data.jsonl", "rb") as file:
    response= openai.File.create(
        file=file,
        purpose='fine-tune'
    )
    
file_id = response['id']
print(f"File uploaded successfully with ID: {file_id}")
save_file("finetunedmodelid.txt", file_id)