import streamlit as st

page1 = st.Page("pages/1_☁️_项目简介.py")
page2 = st.Page("pages/2_📚_陪你聊天.py")
page3 = st.Page("pages/3_🔍_热点搜索.py")
page4 = st.Page("pages/4_📷_剧本创作.py")

pg = st.navigation([page1, page2, page3, page4])
pg.run()