#Author: BinaryBills
#Creation Date: September 10, 2023
#Date Modified: September 11, 2023
#Purpose: After uploading the training data to OpenAI, this file starts the finetuning job.

import openai
import os

def get_finetune_model_id(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            line = file.readline().strip()
            return line
    except FileNotFoundError:
        print(f"The file at '{filepath}' does not exist.")
        return None
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None
    
def save_file(filepath, content):
    with open(filepath, 'w', encoding='utf-8') as outfile: 
        outfile.write(content)

# Usage
filepath = "finetunedmodelid.txt" 
model_id = get_finetune_model_id(filepath)
model_name = "gpt-3.5-turbo"

if model_id:
    print(f"Successfully retrieved model ID: {model_id}")
else:
    print("Failed to retrieve model ID.")
    exit()
    
openai.api_key = os.environ.get("OPENAI_API_KEY")

response = openai.FineTuningJob.create(
   training_file=model_id,
   model=model_name 
)

job_id = response['id']
print(f"Fine-tuning job created successfully with ID: {job_id}")
save_file("jobid.txt", job_id)


