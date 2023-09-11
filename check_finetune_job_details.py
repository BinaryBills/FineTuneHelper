#Author: BinaryBills
#Creation Date: September 10, 2023
#Date Modified: September 11, 2023
#Purpose: After starting the finetune job, the user can use this file to examine its status.

import openai
import os

def get_finetune_job_id(filepath):
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

# Set your OpenAI API key
openai.api_key = os.environ.get("OPENAI_API_KEY")

# Get the fine-tune job ID from the file
filepath = "jobid.txt"
job_id = get_finetune_job_id(filepath)

if job_id:
    try:
        # Retrieve the fine-tuning job details
        openai.FineTuningJob.list(limit=1)
        response = openai.FineTuningJob.retrieve(job_id)
        
        # Print the fine-tuning job details
        print(f"Fine-tuning job details: {response}")
    except openai.error.OpenAIError as e:
        print(f"Failed to retrieve fine-tuning job details: {e}")
else:
    print("Failed to retrieve the job ID.")