import streamlit as st
import pandas as pd
import datetime
import openai

st.header('Document Your _:blue[Dataset]_ :sunglasses:')


openai.api_key = 'OPEN-API-KEY'
data = st.file_uploader("Upload Dataset You Want To Document", type={"csv", "txt"})
if data is not None:
    data_df = pd.read_csv(data)
if st.button('Document Your Dataset'):
    response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "system", "content": "You are a helpful assistant that reads through datasets and makes recommendations"},
            {"role": "user", "content": 'based on the following dataset, write me documentation in yml format describing the dataset and including the name, description, datatype, and tests to run against each column  : ' + str(data_df)}

        ]
    )

    description_of_dataset = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
            {"role": "system", "content": "You are a helpful assistant that reads through datasets and makes recommendations"},
            {"role": "user", "content": 'based on the following dataset, tell me an interesting fact about what you find: ' + str(data_df)}

        ]
    )
    answer = response["choices"][0]["message"]["content"]
    st.write(answer)
    st.sidebar.download_button('Download file', answer, 'text/csv')
    st.sidebar.write(description_of_dataset["choices"][0]["message"]["content"])