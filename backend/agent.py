import os
from typing import Annotated, TypedDict, List
from langgraph.graph import StateGraph, END, START
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, SystemMessage, ToolMessage
from langchain_groq import ChatGroq
from langgraph.prebuilt import ToolNode

from tools import tools

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]

# 1. Initialize the LLM
llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0)
llm_with_tools = llm.bind_tools(tools)

# 2. Define the Nodes
import json # Add this to imports at the top

# ... inside agent.py ...

def call_model(state: AgentState):
    messages = state["messages"]
    
    print("\n" + "="*60)
    print("🤖 AGENT THINKING STEP STARTED")
    print("="*60)
    
    # --- DYNAMIC SYSTEM PROMPT ---
    # We check if we are coming back from a tool. 
    # If so, we force the AI to STOP.
    last_message = messages[-1]
    
    if isinstance(last_message, ToolMessage):
        print("🛑 DETECTED TOOL RESULT. FORCING FINAL ANSWER.")
        # Force a system prompt to stop looping
        stop_instruction = SystemMessage(content=(
            "You have received the result from a tool. "
            "Do NOT call any other tools. "
            "Summarize the result for the user in a friendly sentence and then STOP."
        ))
        messages = messages + [stop_instruction]
    
    # Initial System Prompt
    elif not messages or not isinstance(messages[0], SystemMessage):
        system_instruction = SystemMessage(content=(
            "You are a CRM Data Assistant with 7 tools.\n"
            "1. log_interaction\n"
            "2. get_hcp_history\n"
            "3. edit_interaction_by_id\n"
            "4. smart_edit_last_interaction\n"
            "5. search_by_topic\n"
            "6. submit_sample_request\n"
            "7. get_interaction_stats\n\n"
            "IMPORTANT: Perform the user's request. Once you get a tool result, DO NOT call another tool."
        ))
        messages = [system_instruction] + messages

    # Call LLM
    response = llm_with_tools.invoke(messages)
    
    # LOGGING
    print(f"💭 LLM THOUGHT: {response.content}")
    if response.tool_calls:
        print(f"🔧 TOOL CALLS: {len(response.tool_calls)}")
        for i, tc in enumerate(response.tool_calls):
            print(f"   -> Tool: {tc['name']}")
    else:
        print("🚫 ENDING CONVERSATION")
        
    print("="*60 + "\n")
    
    return {"messages": [response]}

tool_node = ToolNode(tools)

def should_continue(state: AgentState):
    """Checks if the Agent wants to call tools"""
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return END

# 3. NEW ROUTER: Check Tool Result
def check_if_finished(state: AgentState):
    """
    Runs AFTER the tools execute.
    We always route back to Agent to let it summarize,
    but the System Prompt above forces it to stop.
    """
    messages = state["messages"]
    last_message = messages[-1]
    
    # If there was an error, let the agent try to fix it? 
    # For this project, let's just route back to agent.
    return "agent"
# 4. Build the Graph with the NEW logic
workflow = StateGraph(AgentState)
workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

workflow.add_edge(START, "agent")

# Agent -> Tools (or End)
workflow.add_conditional_edges(
    "agent",
    should_continue,
    {
        "tools": "tools",
        END: END
    }
)

# Tools -> NEW ROUTER -> Agent (or End)
workflow.add_conditional_edges(
    "tools",
    check_if_finished, # We use the new function here
    {
        "agent": "agent",
        END: END
    }
)

app = workflow.compile()