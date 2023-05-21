import json
import boto3
from botocore.exceptions import ClientError
import chargebee

ssm_client = boto3.client('ssm')

API_PARAM_NAME = "chargebee-apikey" # Replace this value with the name of your API SSM Parameter if different
SITE_PARAM_NAME = "chargebee-sitename" # Replace this value with the name of your Site SSM Parameter if different

def lambda_handler(event, context):

    # Securely collects the values of the Chargebee Site Name and API key from SSM
    chargebee_site, chargebee_api_key = get_chargebee_params()

    # Initializes and configures the Chargebee client
    chargebee.configure(chargebee_api_key, chargebee_site)

    # Makes a call to the Chargebee API to initiate Export for new event
    if event["Status"] in ['', 'INITIATED']:
        export_id = initiate_export()
        event['ExportId'] = export_id
        event['Status'] = "in-progress"
    # Makes a call to Chargebee API to check on the export status for in-progress events
    elif event['Status'] in ['in-progress']:
        export_id = event['ExportId']
        export_status_output = get_export_status(export_id).__dict__
        export_values = export_status_output['values']

        status = export_values['status']

        # Retrieves the download URL for requested export when ready and marks event as complete
        if status in ['completed']:
            event['Url'] = export_values['download']['download_url']

        if "in_process" in status:
          event['Status'] = "in-progress"
        else:
          event['Status'] = status
        
    return event

def get_chargebee_params():

    param_names = [API_PARAM_NAME, SITE_PARAM_NAME]

    chargebee_site = ""
    chargebee_api_key = ""

    for name in param_names:
        response = ssm_client.get_parameter(
            Name=name,
            WithDecryption=True
        )

        param_value = response['Parameter']['Value']

        if "sitename" in name:
            chargebee_site = param_value
        elif "apikey":
            chargebee_api_key = param_value

    return chargebee_site, chargebee_api_key

def initiate_export():  
    result = chargebee.Export.customers({})
    export_id = result.export.id

    return export_id

def get_export_status(export_id):

    result = chargebee.Export.retrieve(export_id)
    export = result.export
    return export
