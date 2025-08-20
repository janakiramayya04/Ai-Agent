import sys
import types
import os

# ---- Patch litserve MCP to avoid NameError if MCP is missing ----
try:
    from mcp.server import Server as MCPServer
except ImportError:
    MCPServer = None

if MCPServer is None:
    fake_mcp = types.ModuleType("mcp")
    fake_server = types.ModuleType("mcp.server")
    fake_server.Server = lambda *a, **kw: None
    sys.modules["mcp"] = fake_mcp
    sys.modules["mcp.server"] = fake_server
# -----------------------------------------------------------------

from crewai import Crew, Task, Agent, LLM
import litserve as ls
import uvicorn
from tools import FireCrawlSearchTool, VectorDBSearchTool
from dotenv import load_dotenv

load_dotenv()


class AgenticRAGAPI(ls.LitAPI):
    def setup(self, device):
        llm = LLM(model="ollama/llama3.2:latest")

        # Define agents
        research_agent = Agent(
            role="Senior Researcher",
            goal="Research the user's query using available tools to find the most relevant and up-to-date information.",
            backstory="You are a skilled researcher, adept at sifting through data to find factual and actionable insights.",
            tools=[FireCrawlSearchTool(), VectorDBSearchTool()],
            llm=llm,
            verbose=True,
        )

        writer_agent = Agent(
            role="Senior Writer",
            goal="Use the insights from the researcher to compose a clear, concise, and comprehensive answer to the user's query.",
            backstory="You are a skilled writer, known for your ability to explain complex topics in an easily understandable way.",
            llm=llm,
            verbose=True,
        )

        # Define tasks
        researcher_task = Task(
            description="Research the following query: {query}. Find the most critical information and provide a detailed summary.",
            expected_output="A comprehensive summary of the research findings, including key facts, figures, and sources.",
            agent=research_agent,
        )

        writer_task = Task(
            description="Based on the research summary, write a final answer to the query: {query}. Your answer should be well-structured and easy to read.",
            expected_output="A polished, final answer that directly addresses the user's query, synthesized from the research findings.",
            agent=writer_agent,
        )

        # Crew setup
        self.crew = Crew(
            agents=[research_agent, writer_agent],
            tasks=[researcher_task, writer_task],
        )

    # Decode input
    def decode_input(self, request):
        return request["query"]

    # Run prediction
    def predict(self, query):
        return self.crew.kickoff(inputs={"query": query})

    # Encode output
    def encode_output(self, output):
        return {"output": output}


if __name__ == "__main__":
    os.environ["LIT_DISABLE_MCP"] = "1"  # extra safeguard

    api = AgenticRAGAPI()
    server = ls.LitServer(api)
    server.run(port=8000)
