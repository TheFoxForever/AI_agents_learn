from langchain_ollama import OllamaLLM
from langchain.agents import create_react_agent
from langchain_core.prompts import PromptTemplate
from database import Database
from tools.task_tool import TaskTool
from tools.note_tool import NoteTool
from tools.reminder_tool import ReminderTool
from tools.schedule_tool import ScheduleTool


class AIAgent:
    def __init__(self):
        self.db = Database()
        self.llm = OllamaLLM(model="llama3.2:3b", device="cuda")
        self.tools = [
            TaskTool(self.db),
            NoteTool(self.db),
            ReminderTool(self.db),
            ScheduleTool(self.db),
        ]

        template = """You are an AI assistant with access to the following tools:

        {tools}

        Use the following format:

        Question: the input question you must answer
        Thought: you should always think about what to do
        Tool Needed: The tool to use, should be one of [{tool_names}]. Only respond with one of the {tool_names} as the action.
        Action Input: the input to the tool, examples: run, list items, add item, delete item etc...
        Observation: the result of using the tool
        Thought: I now know the final answer
        Final Answer: the final answer to the original input question

        Always include a Final Answer section in your response.
        
        Question: {input}
        {agent_scratchpad}"""

        aiPrompt = PromptTemplate.from_template(template)

        self.agent = create_react_agent(self.llm, self.tools, aiPrompt)

    def process_query(self, query: str) -> str:
        try:
            print("agent query", query)
            return self.agent.invoke({"input": query, "intermediate_steps": []})
        except Exception as e:
            print(f"Error in processing query: {e}")
            return f"An error occurred: {str(e)}"

    # def process_query(self, query: str) -> str:
    # try:
    #     return self.agent.invoke({
    #         "input": query,
    #         "intermediate_steps": []
    #     })
    # except Exception as e:
    #     print(f"Error in processing query: {e}")
    #     return f"An error occurred: {str(e)}"
