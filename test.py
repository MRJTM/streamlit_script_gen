import streamlit as st
import pandas as pd
import numpy as np

st.write("""
# My first app
Hello *world!*
""")

st.write("------- [Text Input Test] ---------")
st.text_input("Your name", key="name")
st.write("Get Your name: ",st.session_state.name)

st.write("------- [Slider Test] ---------")
x = st.slider('x')  # 👈 this is a widget
st.write(x, 'squared is', x * x)

st.write("------- [Checkbox Test] ---------")
if st.checkbox('Show dataframe'):
    chart_data = pd.DataFrame(
       np.random.randn(20, 3),
       columns=['a', 'b', 'c'])
    st.write(chart_data)

st.write("------- [SelectBox Test] ---------")
df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40]
    })

option = st.selectbox(
    'Which number do you like best?',
     df['first column'])

'You selected: ', option