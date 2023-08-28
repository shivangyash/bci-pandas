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
        llm = OpenAI(api_token=API_KEY)
        pandas_ai = PandasAI(llm, middlewares=[StreamlitMiddleware()], verbose=False)
        question = '''remove extra spaces from all the column names, convert dates into 'yyyy-mm-dd' format,
             convert the column amount financed, fixed contractual repayment, interest received, capital received, current principe o/s, arrears amount to numeric type by replacing , and pound symbol to '', replace the values of column remaining term_v1 with the value come after subtracting 6 from value in term,
              convert column ('Case Status Live or Arrears', 'Client >=21 years Old', 'Min Balance €2,000 and Max Balance €8,000', 'Term Max 60 mths', 'Monthly Arrears Payments <=2', 'Weekly Arrears Payments <=5', 'Weekly Impaired Loans: DD <63 days old 40%', 'Monthly impaired loans DD<180 days 40%') into boolean type that is 'FALSE' if original value is 0 and 'TRUE' if it is 1'''
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
        st.write('Cleaned dataframe')
        st.session_state.df.to_csv('latest.csv')
        st.download_button(label='Download Cleaned File', data=st.session_state.df.to_csv(), mime='text/csv')


# st.subheader("Prompt history:")
# st.write(st.session_state.prompt_history)

if st.button("Clear"):
    st.session_state.prompt_history = []
    st.session_state.df = None
