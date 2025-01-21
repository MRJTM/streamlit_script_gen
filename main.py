import streamlit as st
import pandas as pd

st.write("""
# My first app
Hello *world!*
""")

# df = pd.read_csv("my_data.csv")
# df改为不从本底读取文件,而是直接写入数据
df = pd.DataFrame({
  'first column': [1, 2, 3, 4],
  'second column': [10, 20, 30, 40]
})
st.line_chart(df)