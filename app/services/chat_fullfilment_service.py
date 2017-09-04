from flask import jsonify
import json

def process_and_fullfill_chat_request(input_payload):
    if validate_input_payload(input_payload):
        action = input_payload['result']['action']
        parameters = input_payload['result']['parameters']
        context = input_payload['result']['contexts']
        existing_response = input_payload['result']['fulfillment']['speech']
        resp = {
            'speech': existing_response,
            'displayText': existing_response,
            'data': parameters,
            'contextOut': context,
            'source': 'DonnaFulFillmentBackend'
        }
        if action == 'schedule-meeting-request':
            resp = process_schedule_meeting(parameters, resp)
        return json.dumps(resp)
    return json.dumps(input_payload)

def validate_input_payload(input_payload=None):
    if input_payload:
        result = input_payload.get('result', None)
        if result:
            fulfillment = result.get('fulfillment', None)
            contexts = result.get('contexts', None)
            parameters = result.get('parameters', None)
            if fulfillment and fulfillment.get('speech', None) and contexts and len(contexts) > 0 and parameters:
                auth_context = [ c for c in contexts if c.get('name', None) =='auth'][0]
                print(auth_context)
                if auth_context :
                    auth_params = auth_context.get('parameters',None)
                    if auth_params and auth_params.get('token', None):
                        return True


    return False

def process_schedule_meeting(parameters, resp):
    return resp
