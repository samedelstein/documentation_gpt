import streamlit as st
import pandas as pd
import datetime
import openai


directions_expander = st.expander("Directions to make this app work")
directions_expander.write(
    '''
    First, you need an OpenAI API key which you can sign up for [here](https://platform.openai.com/signup?__cf_chl_rt_tk=VKUHnuTzDpc3gfI4Cy8m.HtdJ4UYoDSj3Nd1cRYRUEo-1680459300-0-gaNycGzNC9A)
    NOTE: There is a cost to using the OpenAI API - it should be minimal (less than a penny per recommendation). You get $18 of free use over three months, then you will have to subscribe.
    
    Once you have the key, please paste it on the left hand menu of this app in the text box that say "Add OpenAI API Key here". Assuming they are valid, you'll see a green box  with the text "API credentials valid"

    Next, select a dataset you would like to document. Right now I have it set up so that you should upload the selected dataset, and it should be in a csv format. Maybe in the future I'll add an ability to paste a URL.
    '''
)

st.header('Document Your _:blue[Dataset]_ :sunglasses:')


open_api_key_input = st.sidebar.text_input("Add OpenAI API Key here")
openai.api_key = open_api_key_input 
# Check if API credentials are valid
try:
    prompt = "Hello, World!"
    openai.Completion.create(engine="text-davinci-002", prompt=prompt)
    st.sidebar.success("API credentials valid")
except:
    st.sidebar.error("Invalid API credentials")

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