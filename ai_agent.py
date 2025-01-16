from langchain_ollama import OllamaLLM
from langchain.agents import create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain.schema import AgentFinish, AgentAction
from langchain.output_parsers import OutputFixingParser
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
import json
from database import Database
from tools.task_tool import TaskTool
from tools.note_tool import NoteTool
from tools.reminder_tool import ReminderTool
from tools.schedule_tool import ScheduleTool


class AgentOutput(BaseModel):
    thought: str = Field(description="The agent's thought process")
    tool_needed: str = Field(description="The tool needed for the action")
    action_input: str = Field(description="The input for the tool")
    observation: str = Field(description="The result of using the tool")
    final_answer: str = Field(
        description="The final answer to the original input question"
    )


class AIAgent:
    def __init__(self):
        self.db = Database()
        self.llm = OllamaLLM(model="llama3.2:3b", device="cuda", max_tokens=2048)
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
        Tool Needed: The tool to use, should be one of [{tool_names}] or "None" if no tool is needed. Only respond with one of the {tool_names} as the action or "None".
        Action Input: the input to the tool, examples: run, list items, add item, delete item etc...or your direct response if no tool is needed.
        Final Answer: the final answer to the original input question
        Observation: the result of using the tool, or skip this if no tool is needed.

        You must always return valid JSON fenced by a markdown code block and include a Final Answer Section in the response. Do not return any additional text.
        
        Question: {input}
        {agent_scratchpad}"""

        aiPrompt = PromptTemplate.from_template(template)

        self.agent = create_react_agent(self.llm, self.tools, aiPrompt)

        parser = PydanticOutputParser(pydantic_object=AgentOutput)
        self.fixing_parser = OutputFixingParser.from_llm(parser=parser, llm=self.llm)

    def process_query(self, query: str) -> str:
        print("agent query", query)
        try:
            result = self.agent.invoke({"input": query, "intermediate_steps": []})

            if isinstance(result, AgentFinish):
                parsed_output = self.fixing_parser.parse(
                    json.dumps(result.return_values)
                )
            elif isinstance(result, list) and isinstance(result[-1], AgentFinish):
                parsed_output = self.fixing_parser.parse(
                    json.dumps(result[-1].return_values)
                )
            else:
                parsed_output = self.fixing_parser.parse(json.dumps(result))
            return parsed_output.final_answer
        except Exception as e:
            print(f"Error in processing query: {e}")
            return json.dumps({"error": f"An error occurred: {str(e)}"})
