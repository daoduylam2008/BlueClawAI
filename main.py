import llm
import utils
model = llm.LLM(0)

# messages = "What is the weather like in San Fransisco?"

messages = {"messages": [
    {
        "role": "user",
        "content": "What is the weather like in San Fransisco?"
    }
]}

# messages = [
#     {
#         "role": "user",
#         "content": "What is the weather in San Fransisco?"
#     }
# ]
responses = (model.invoke(messages))
print(utils.ai_sort(responses))


