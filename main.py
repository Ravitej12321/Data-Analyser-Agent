import asyncio 
from Teams.AnalyserGptTeam import get_analyser_gpt_team
from Config.openai_model_client import get_model_client
from Config.Docker_utils import GetDockerCommandLineExecutor,startDockerContainer,stopDockerContainer
from Config.dataset_read import read_dataframe
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.base import TaskResult
async def main():
    open_ai_model = get_model_client()

    docker  = GetDockerCommandLineExecutor()

    analyser_team = get_analyser_gpt_team(docker,open_ai_model)

    try :
        # path = "Dataset\\Titanic_dataset.csv"
        # dataframe = read_dataframe(path)
        task1 = f"Can you tell me how many rows are there  in the Titanic_dataset.csv in the Directory"
        task2 = f"Can you draw a graph for people lived vs died from my dataset in the directory and save it as Output.png"
        task = f" Perform complete data analysis and give me the useful insights \
        and store all the graphs analysis output_images_with timestamp in analysis folder"
        await startDockerContainer(docker)
        
        async for message in analyser_team.run_stream(task=task):
            print("="*40)
            if isinstance(message,TextMessage):
                print(message.source,":",message.content)
            if isinstance(message,TaskResult):
                print("Stop Reason :",message.stop_reason)

    except Exception as e:
        print("Exception Triggered.",e)
    finally :
        await stopDockerContainer(docker)


if __name__ == "__main__":
    asyncio.run(main())
