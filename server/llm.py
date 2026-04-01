from langchain_ollama import ChatOllama
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain.agents.middleware import SummarizationMiddleware
import utils


class LLM:
    def __init__(self, model="llama3.1", summarized_model='qwen2.5:3b', temperature=0.1, num_predict=70, **kwargs):
        # Define models for llm and summarized text in the middleware
        self.llm = ChatOllama(model=model, temperature=temperature, num_predict=num_predict, **kwargs)
        self.summarized_llm = ChatOllama(model=summarized_model, num_predict=50)

        # LLM Agent
        self.agent = create_agent(
            self.llm, 
            tools=utils.load_tools(),
            checkpointer=InMemorySaver(),
            middleware=[
                SummarizationMiddleware(
                    model=self.summarized_llm,
                    trigger=("tokens", 4000),
                    keep=("messages", 20)
                )
            ]
        )
        
    def invoke(self, messages, config=None):
        return self.agent.invoke(messages, config=config)
    
    def request(self, query):
        config = {"configurable": {"thread_id": "1"}}
        messages = {"messages": [
            {
                "role": "user",
                "content": query
            }
        ]}

        response = self.invoke(messages=messages, config=config)
        return response
