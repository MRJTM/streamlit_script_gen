import streamlit as st
from openai import OpenAI
gpt_client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"],base_url=st.secrets["BASE_URL"])

