import langchain_core
import tools as tls

from inspect import getmembers


def load_tools():
    functions = []
    for name, function in list(getmembers(tls)):
        if (type(function) == langchain_core.tools.structured.StructuredTool):
            functions.append(function)

    return functions     


def tool_sort(responses):
    tool_responses = []

    for response in responses['messages']:
        if type(response) == langchain_core.messages.ai.AIMessage:
            if response.content == '':
                tool_responses.append(response)
            
    return tool_responses


def ai_sort(responses):
    ai_responses = []

    for response in responses['messages']:
        if type(response) == langchain_core.messages.ai.AIMessage:
            if response.content != '':
                ai_responses.append(response)
        
    return ai_responses

def human_sort(responses):
    human_responses = []

    for response in responses['messages']:
        if type(response) == langchain_core.messages.human.HumanMessage:
            human_responses.append(response)
        
    return human_responses