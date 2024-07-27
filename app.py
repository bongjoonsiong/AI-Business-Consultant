__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

# Import Libraries

import streamlit as st
import chromadb

from crewai import Agent, Task, Crew
import os
from langchain_cohere import ChatCohere


### 2. Configure Streamlit UI Environment

# Add Streamlit Components

# background
page_bg_img = '''
<style>
.stApp  {
background-image: url("https://www.onemoremoney.com/makemoneyonlinewithai/wp-content/uploads/2024/04/ChatGPT-5-employee-at-work.jpg");
background-size: cover;
}
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

# title
st.title("Jeffrey AI Business Consultants")

# logo
#image_url = "https://cdn-icons-png.flaticon.com/512/1998/1998614.png"
image_url = "https://www.onemoremoney.com/makemoneyonlinewithai/wp-content/uploads/2023/12/Gemini-Google-Disk.jpg"
st.sidebar.image(image_url, caption="", use_column_width=True)
st.sidebar.write(" This AI Business Consultant is built using AI Multi-Agent system. It can give you business insights, statistical analysis and up-to-date information about any business topic. This AI Multi-Agent Business Consultant delivers knowledge on demand and for FREE!")

# text inputs
business = st.text_input('Enter The Required Business Search Area')
stakeholder = st.text_input('Enter The Stakeholder Team')


### 3. Initialize LLM Object

# LLM object and API Key

# Prompt the user to input their API key
#api_key = input("Please enter your Cohere API key: ")
#os.environ['COHERE_API_KEY'] = api_key

api_key = st.secrets["COHERE_API_KEY"]
os.environ['COHERE_API_KEY'] = api_key

llm = ChatCohere()

#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#"""
#os.environ["OPENAI_API_KEY"] = "XXXXXXXXXXXXXXXXXXXXXX"
#llm = OpenAI()
#"""

#"""
#os.environ["GEMINI_API_KEY"] = "XXXXXXXXXXXXXXXXXXXXXX"
#llm = Gemini()
#"""
#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx


### 4. Create CrewAI Agents

# Create 3 Crew Agents


#1. Role: Planner:
planner = Agent(
    role="Business Consultant",
    goal="Plan engaging and factually accurate content about the : {topic}",
    backstory="You're working on providing Insights about : {topic} "
              "to your stakeholder who is : {stakeholder}."
              "You collect information that help them take decisions "
              "Your work is the basis for "
              "the Business Writer to deliver good insights.",
    allow_delegation=False,
 verbose=True,
    llm = llm
)


#2. Role: Writer:
writer = Agent(
    role="Business Writer",
    goal="Write insightful and factually accurate "
         "insights about the topic: {topic}",
    backstory="You're writing a Business Insights document "
              "about the topic: {topic}. "
              "You base your design on the work of "
              "the Business Consultant, who provides an outline "
              "and relevant context about the : {topic}. "
              "and also the data analyst who will provide you with necessary analysis about the : {topic} "
              "You follow the main objectives and "
              "direction of the outline, "
              "as provided by the Business Consultant. "
              "You also provide objective and impartial insights "
              "and back them up with information "
              "provided by the Business Consultant."
              "design your document in a professional way to be presented to : {stakeholder}."
              ,
    allow_delegation=False,
    verbose=True,
    llm=llm
)


#3. Role: Analyst:
analyst = Agent(
    role="Data Analyst",
    goal="Perform Comprehensive Statistical Analysis on the topic: {topic} ",
    backstory="You're using your strong analytical skills to provide a comprehensive statistical analysis with numbers "
              "about the topic: {topic}. "
              "You base your design on the work of "
              "the Business Consultant, who provides an outline "
              "and relevant context about the : {topic}. "
              "You follow the main objectives and "
              "direction of the outline, "
              "as provided by the Business Consultant. "
              "You also provide comprehensive statistical analysis with numbers to the Business Writer "
              "and back them up with information "
              "provided by the Business Consultant.",
    allow_delegation=False,
    verbose=True,
    llm=llm
)


#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
#'''
# If Planner Agent is allowed to delegate some of it's task. 

#if planner.allow_delegation:
#    data_collector = Agent(role="Data Collector", llm=llm)
#    data_analyst = Agent(role="Data Analyst", llm=llm)

#    data = data_collector.collect_data(topic)
#    analysis = data_analyst.analyze_data(data)

#    planner.integrate_results(data, analysis)

#'''
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX


### 5. Create and Assign Tasks to each Agent

# Create Tasks

#1. Task - Plan:
plan = Task(
    description=(
        "1. Prioritize the latest trends, key players, "
            "and noteworthy news on the {topic}.\n"
        "2. Place your business insights.\n"
        "3. Also give some suggestions and things to consider when \n "
            "dealing with International operators.\n"
        "4. Limit the document to only 500 words"
    ),
    expected_output="A comprehensive Business Consultancy document "
        "with an outline, and detailed insights, analysis and suggestions",
    agent=planner,
    # tools = [tool]

)


#2. Task - Write:
write = Task(
    description=(
        "1. Use the business consultant's plan to craft a compelling "
            "document about {topic}.\n"
      "2. Sections/Subtitles are properly named "
            "in an engaging manner.\n"
        "3. Proofread for grammatical errors and "
            "alignment with the brand's voice.\n"
         "3. Limit the document to only 200 words "
         "4. Use impressive images and charts to reinforce your insights "
    ),
    expected_output="A well-written Document "
        "providing insights for {stakeholder} ",
    agent=writer
)


#3. Taks - Analyse: 
analyse = Task(
    description=(
        "1. Use the business consultant's plan to do "
            "the needed statistical analysis with numbers on {topic}.\n"
      "2. to be presented to {stakeholder} "
            "in a document which will be deisgned by the Business Writer.\n"
        "3. You'll collaborate with your team of Business Consultant and Business writer "
            "to align on the best analysis to be provided about {topic}.\n"
 ),
    expected_output="A clear comprehensive data analysis "
        "providing insights and statistics with numbers to the Business Writer ",
    agent=analyst
)


### 6.  Run the Multi Agents Crew (Team)

# Execute the Multi-Agent system :

# Assemble the Team (Crews)
crew = Crew(
    agents=[planner, analyst, writer],
    tasks=[plan, analyse, write],
    verbose=2
)

#if st.button("Run"):
# with st.spinner('Loading...'):
#  result = crew.kickoff(inputs={"topic": business,"stakeholder": stakeholder})
# st.write(result)


#Different Approach
#Consider Security and Error: 

if st.button("Run"):
    with st.spinner('Loading...'):
        if not business or not stakeholder:
            st.error("Please provide both a business topic and a stakeholder.")
        else:
            try:
                result = crew.kickoff(inputs={"topic": business, "stakeholder": stakeholder})
                st.write(result)
            except Exception as e:
                st.error(f"An error occurred: {e}")
