from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import db

app = FastAPI()

shared_context = {}

@app.get("/")
async def read_root():
    return {"Hello": "World"}

@app.post("/")
async def handle_request(request: Request):
    payload = await request.json()
    intent = payload['queryResult']['intent']['displayName']
    


    intent_handler_dict = {
    'job.title': find_job,
    'job.title.extend': find_details,
    'contact.details': find_contacts,
    'add.details': add_details
    }
    return intent_handler_dict[intent](payload)

        


def find_job(payload: dict):
    parameters = payload['queryResult']['parameters']
    job_items = parameters.get('job-items') 
    company = db.get_company(job_items)
    

    if company:
        fulfillment_text = f"{company} has a vacancy for {job_items}. Do you need to know more details? (Yes or No)"
    else:
        fulfillment_text = f"No job vacancies for {job_items}"  

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text,
    }) 


def find_details(payload: dict):
    output_contexts = payload['queryResult']['outputContexts']
    for context in output_contexts:
        if 'parameters' in context and 'job-items' in context['parameters']:
            context['parameters']['job-items'] = context['parameters']['job-items'].replace('\xa0', ' ')
            parameters = context.get('parameters', {})
            
        
    job_items = parameters.get('job-items')
    qualification = db.get_Qualifications(job_items)
    
    details = db.get_details(job_items)
    if details:
        if details == 'freshers':
            fulfillment_text = f"They need {qualification} qualifications.They accept {details}, No need industrial experinces. Do you need to apply for this?"
        else:
            fulfillment_text = f"They need {qualification} qualifications and {details}. Do you need to apply for this?"
    else:
        fulfillment_text = f"No more deatils for {job_items}"  

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text
    })


def find_contacts(payload: dict):
    output_contexts = payload['queryResult']['outputContexts']
    for context in output_contexts:
        if 'parameters' in context and 'job-items' in context['parameters']:
            context['parameters']['job-items'] = context['parameters']['job-items'].replace('\xa0', ' ')
            parameters = context.get('parameters', {})
            
        
    job_items = parameters.get('job-items')
    contacts = db.get_contact(job_items)
    email = db.get_email(job_items)
  

    if contacts:
        fulfillment_text = f"To apply for this job, please send your application to {email} or contact them at {contacts}."
    else:
        fulfillment_text = f"No any contacts mentioned here."  

    return JSONResponse(content={
        "fulfillmentText": fulfillment_text,
    }) 


from fastapi.responses import JSONResponse
from typing import Optional

def add_details(payload: dict):
    try:
        parameters = payload['queryResult']['parameters']
        query_text = payload['queryResult']['queryText']

        # Extract values from the comma-separated queryText
        job_items, qualification, company, work_exp, contact, email = map(str.strip, query_text.split(','))

        if not job_items or not qualification or not company or not work_exp or not contact or not email:
            raise ValueError("Incomplete job details provided")

        # Add details to the database
        db.add_job_details(job_items, qualification, company, work_exp, contact, email)

        fulfillment_text = f"Details for {job_items} have been successfully added. Thanks for interacting with us!"

        return JSONResponse(content={
            "fulfillmentText": fulfillment_text
        })
    except Exception as e:
        error_message = f"Error processing job details: {e}"
        print(error_message)
        return JSONResponse(content={
            "fulfillmentText": error_message
        })

'''
print(job_items)
        print(qualification)
        print(company)
        print(work_exp)
        print(contact)
        print(email)
        '''