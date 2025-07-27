import streamlit as st
import asyncio, os
from Teams.AnalyserGptTeam import get_analyser_gpt_team
from Config.openai_model_client import get_model_client
from Config.Docker_utils import GetDockerCommandLineExecutor,startDockerContainer,stopDockerContainer
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.base import TaskResult
from PIL import Image
st.title("Data Analysis GPT")

file_uploader = st.file_uploader("Upload your Dataset",type=["csv", "xlsx", "xls"])
if "messages" not in st.session_state:
   st.session_state.messages = []
if 'autogen_team_state' not in st.session_state:
   st.session_state.autogen_team_state = None

# task = st.text_input("Enter your task",value="Can you tell me how many rows in dataset?")
task  = st.chat_input("Enter your Task.")
async def run_gpt_analyser(docker,open_ai_model,task):
    try:
        team = get_analyser_gpt_team(docker,open_ai_model)
        await startDockerContainer(docker)
        if st.session_state.autogen_team_state  is not None:
           await team.load_state(st.session_state.autogen_team_state)

        async for message in team.run_stream(task=task):
            if isinstance(message,TextMessage):
                print(msg:=f"{message.source} : {message.content}")
                if msg.startswith('user'):
                   with  st.chat_message('user',avatar="human"):
                    st.markdown(msg)
                if msg.startswith('Data_Analyzer_agent'):
                   with st.chat_message('assistant',avatar="assistant"):
                    st.markdown(msg)
                if msg.startswith('CodeExecutor'):
                   with st.chat_message('assistant',avatar="assistant"):
                    st.markdown(msg)
            st.session_state.messages.append(msg)
                


            if isinstance(message,TaskResult):
                print(msg:=f"Stop Reason : {message.stop_reason}")
                st.markdown(msg)
                st.session_state.messages.append(msg)
        st.session_state.autogen_team_state = await team.save_state()
        return None
    except Exception as e:
        print(e)
        return e
    finally:
        await stopDockerContainer(docker)
if st.session_state.messages:
       for msg in st.session_state.messages:
           st.markdown(msg)
if task:

    if file_uploader is not None and task:
        if not os.path.exists('temp'):
            os.makedirs('temp') 
        with open("temp/data.csv","wb") as file:
            file.write(file_uploader.getbuffer())

    open_ai_model = get_model_client()

    docker  = GetDockerCommandLineExecutor()

    

    error = asyncio.run(run_gpt_analyser(docker,open_ai_model,task)) 
    st.title("Image Analysis - Directory Viewer")
    directory = "temp/analysis"
    # Get list of image files
    image_extensions = (".png", ".jpg", ".jpeg", ".gif", ".bmp")
    image_files = [f for f in os.listdir(directory) if f.lower().endswith(image_extensions)]

    st.write(f"Found {len(image_files)} images in `{directory}`")

    # Display image names and previews
    for img_file in image_files:
        img_path = os.path.join(directory, img_file)
        st.write(f"**{img_file}**")
        image = Image.open(img_path)
        st.image(image, caption=img_file, use_container_width=True)
    if error:
        st.error("An Exception Occured: ",error)
else: 
    st.warning("Please upload a Csv file.")

    