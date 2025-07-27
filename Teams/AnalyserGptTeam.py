from Agents.DataAnalyserAgent import get_data_analyser_agent
from Agents.CodeExecutorAgent import get_code_executor_agent
from Config.openai_model_client import get_model_client
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.conditions import TextMentionTermination
def get_analyser_gpt_team(docker,model_client):

    code_executor_agent = get_code_executor_agent(docker)

    analyser_agent = get_data_analyser_agent(model_client)

    team = RoundRobinGroupChat(
        participants=[analyser_agent,code_executor_agent],
        max_turns=16,
        termination_condition=TextMentionTermination("TERMINATE")
    )
    return team
