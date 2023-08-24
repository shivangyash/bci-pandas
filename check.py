import os

import streamlit as st
import pandas as pd
from pandasai import PandasAI
from pandasai.llm.openai import OpenAI
from pandasai.middlewares.streamlit import StreamlitMiddleware
import matplotlib.pyplot as plt
from io import StringIO
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv('OPENAI_API_KEY')

if 'prompt_history' not in st.session_state:
    st.session_state.prompt_history = []
if 'df' not in st.session_state: 
    st.session_state.df = None

if st.session_state.df is None:
    uploaded_file = st.file_uploader(
        "Choose a CSV file. This should be in long format (one datapoint per row).",
        type="csv",
    )
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.session_state.df = df

# with st.form("Question"):
#     question = st.text_input("Question", value="", type="default")



submitted = st.button("Submit")
if submitted:
    with st.spinner():
        llm = OpenAI(api_token=st.secrets["openai_api_key"])
        pandas_ai = PandasAI(llm, middlewares=[StreamlitMiddleware()], verbose=False)
        question = '''remove extra spaces from all the column names,  remove % from the column age of borrower, change  the date format to yyyy-mm-dd, remove the british sterling pound symbol from column amount financed, '''
        x = pandas_ai.run(st.session_state.df, prompt=question, is_conversational_answer=False)
        # st.write(x)
        # data = pd.read_csv(StringIO(x))

        # data.to_csv('file.csv')
        st.session_state.prompt_history.append(question)

if st.session_state.df is not None:
    st.subheader("Current dataframe:")
    st.write(st.session_state.df)
    # dff = st.session_state.df
    if submitted:
        st.session_state.df.to_csv('latest.csv')
        st.download_button(label='Download Cleaned File', data=st.session_state.df.to_csv(), mime='text/csv')


# st.subheader("Prompt history:")
# st.write(st.session_state.prompt_history)

if st.button("Clear"):
    st.session_state.prompt_history = []
    st.session_state.df = None
