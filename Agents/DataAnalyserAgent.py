from autogen_agentchat.agents import AssistantAgent
from Agents.prompts.DataAnalyzerPrompt import DataAnalyzer_prompt


def get_data_analyser_agent(model_client):
    analyzer_agent = AssistantAgent(
        name = "Data_Analyzer_agent",
        description = "You are an analyzer agent who solves the data analysis part of an user task.",
        system_message= DataAnalyzer_prompt,
        model_client= model_client
    )
    return analyzer_agent
