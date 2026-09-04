import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from gmail_service import fetch_yesterdays_emails
from calendar_service import fetch_todays_schedule
from meeting_service import transcribe_audio
from dotenv  import load_dotenv
load_dotenv()

# 2. Initialize the LangChain Groq Model
# We use llama3-8b-8192 because it is very fast for text analysis
llm = ChatGroq(temperature=0, model_name="qwen/qwen3.8-27b")

# 3. Create the Prompt Template
# This is the "brain" instruction. We tell the AI exactly how to format the output.
prompt_template = PromptTemplate.from_template(
    """
    You are an elite executive assistant. 
    I am giving you emails, schedule, and meeting transcript. 
    Include meeting insights in the briefing. 
    
    Here are the emails from the last 24 hours:
    {emails_data}
    
    Here is today's calendar schedule:
    {calender_data}
    
    Here are the meeting transcripts:
    {meeting_notes}
    
    Please write a Morning Briefing. Provide:
    1. A cohesive summary of everything that happened.
    2. A consolidated master list of Action Items I need to do today.
    """
)

# Combine the prompt and the LLM into a chain
ai_chain = prompt_template | llm

def run_assistant():
    print("Fetching emails from Gmail service...\n")
    email_text = fetch_yesterdays_emails()
    if not email_text:
        email_text ="No emails found today"

    print("Fetching today's schedule from Calender...\n")
    calender_text = fetch_todays_schedule()
    if not calender_text:
        calender_text="Calender unavailable today"
    
    x = input( "\nDo you have a meeting recording to analyze? (yes=1/no=0): ")
    if x == "1":
        folder_path = input("\nEnter Folder Path where recorded meeting are present:")
        while True:
            meeting_text =""
            if os.path.exists(folder_path):
                for filename in os.listdir(folder_path):
                    if filename.endswith((".mp3" , ".wav")):
                        file_location = os.path.join(folder_path, filename)
                        result = transcribe_audio(file_location)
                        if result:
                            meeting_text += result
                            meeting_text += "\n--- Next Meeting ---\n"
                break
            else:
                folder_path = input("\nEnter valid Folder Path:")
    else:
        meeting_text = "No meeting recordings provided today."

    print("Sending to AI for Morning Briefing...\n")

    # Invoke the LangChain! Pass the giant string into the prompt variable
    response =ai_chain.invoke({
        "emails_data":email_text,
        "calender_data":calender_text,
        "meeting_notes":meeting_text
    })

    print(response.content)
           
if __name__ == '__main__':
    run_assistant()