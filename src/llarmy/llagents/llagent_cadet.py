"""LLAgent Cadet - Basic agent with OCR capabilities."""

from llama_index.llms.openai import OpenAI
from llama_index.core.agent import FunctionCallingAgentWorker, AgentRunner
from llarmy.equipment.reading_text_ocr import ReadingTextOCRToolSpec


ocr_tool = ReadingTextOCRToolSpec()
ocr_tool_list = ReadingTextOCRToolSpec().to_tool_list()
llm = OpenAI(model="gpt-3.5-turbo")

agent_worker = FunctionCallingAgentWorker.from_tools(
    tools=list(ocr_tool_list),
    llm=llm,
    verbose=True,
)

agent_cadet = AgentRunner(agent_worker)

response = agent_cadet.query(
    "What is the text in the non printed material image located at ./image_7_vw.jpg ? "
    "Please, any text extracted from the tool try to do your own interpretation "
    "based on the output of the OCR",
)
