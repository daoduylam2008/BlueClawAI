from langchain_ollama import ChatOllama
from langchain.agents import create_agent
import utils


class LLM:
    def __init__(self,user_id, model="llama3.1", temperature=0.1, num_predict=70, **kwargs):
        self.user_id = user_id
        self.__llm = ChatOllama(model=model, temperature=temperature, num_predict=num_predict, **kwargs)
        self.agent = create_agent(self.__llm, tools=utils.load_tools())
    def invoke(self, messages):
        return self.agent.invoke(messages)
    
    def request(self, query):
        messages = {"messages": [
            {
                "role": "user",
                "content": query
            }
        ]}
        return self.invoke(messages=messages)

    
