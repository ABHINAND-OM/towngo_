from django.shortcuts import render

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

import google.cloud.dialogflow_v2 as dialogflow


def chatbot(request):
    return render(request, 'chatbot.html')


def chatbot1(request):
    # Get user input from the chat interface
    user_query = request.POST.get('user_query', '')

    # Use Dialogflow to get a response
    dialogflow_response = get_dialogflow_response(user_query)

    # Return the response to the chat interface
    return JsonResponse({'bot_response': dialogflow_response})


def get_dialogflow_response(user_query):
    project_id = 'your-project-id'  # Replace with your Dialogflow project ID

    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, 'your-session-id')  # Replace with your Dialogflow session ID

    text_input = dialogflow.TextInput(text=user_query, language_code='en')
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(session=session, query_input=query_input)

    return response.query_result.fulfillment_text
