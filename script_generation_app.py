"""
剧本生成的app界面
"""

import streamlit as st
import os
from langchain.document_loaders import TextLoader,Docx2txtLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from openai import OpenAI
from docx import Document

OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
OPENAI_BASE_URL = st.secrets["BASE_URL"]
os.environ['OPENAI_API_KEY'] =OPENAI_API_KEY
os.environ['OPENAI_BASE_URL'] =OPENAI_BASE_URL

# embeddings = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY,openai_api_base=OPENAI_BASE_URL)
persist_directory='text_persist'
collection_name='text_collection'
# model_name="gpt-4o-mini-2024-07-18"
model_name='o1-mini-2024-09-12'
if "openai_model" not in st.session_state:
    st.session_state['openai_model']="gpt-4o-mini-2024-07-18"
if "prompt_tmp" not in st.session_state:
    st.session_state['prompt_tmp']=open("prompts/prompt1.txt").read()
# llm=ChatOpenAI(temperature=0,openai_api_key=OPENAI_API_KEY,openai_api_base=OPENAI_BASE_URL,model_name=model_name)
# chain=load_qa_chain(llm,chain_type='stuff')
client = OpenAI(api_key=OPENAI_API_KEY,base_url=OPENAI_BASE_URL)


# 文本上传，支持读取文件
# def load_file(file_path):
#     docs=Docx2txtLoader(file_path).load()
#     # 将pdf向量化
#     text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
#     split_docs = text_splitter.split_documents(docs)
#
#     vectorstore = Chroma.from_documents(split_docs, embeddings,
#                                         collection_name=collection_name,
#                                         persist_directory=persist_directory)
#     vectorstore.persist()
#     return vectorstore

def load_file(file_path):
    doc = Document(file_path)
    full_text = []
    for para in doc.paragraphs:
        full_text.append(para.text)
    docs = "\n".join(full_text)
    docs=docs[:40000]
    return docs

def response_generator(prompt=''):
    stream = client.chat.completions.create(
        model=st.session_state["openai_model"],
        messages=[
            {"role": 'user', "content": prompt}
        ],
        stream=True,
    )
    return stream

if "messages" not in st.session_state:
    st.session_state["messages"] = []

st.title("VISAL AI剧本生成工具")

st.header("上传文件",divider="grey")

uploaded_file=st.file_uploader("Choose a file")
if uploaded_file is not None and (not st.session_state.get("uploaded_file") or uploaded_file.name != st.session_state.uploaded_file.get("name")):
    # Update the session state
    st.session_state["uploaded_file"] = {"name": uploaded_file.name, "data": uploaded_file}
    path=os.path.join('.',uploaded_file.name)
    with open(path,'wb') as f:
        f.write(uploaded_file.getbuffer())

    current_vectorstore = load_file(path)
    st.text_area(label="文件内容",value=current_vectorstore)
    st.session_state["current_vectorstore"]=current_vectorstore
    os.unlink(uploaded_file.name)

# prompt输入
st.header("产生剧本",divider="grey")
# 增加时长的输入
secs = st.number_input("产生视频时长（单位：秒）",value=60)

if st.button(label="生成"):
    script="demo剧本"
    if "current_vectorstore" in st.session_state:
        # 获取读取文件的内容
        current_vectorstore=st.session_state['current_vectorstore']
        # 组成prompt
        prompt=st.session_state['prompt_tmp'].replace('aaaaa',current_vectorstore).replace('bbbbb',str(secs))
        st.session_state["messages"].append(['user', prompt])

        # docs = current_vectorstore.similarity_search(prompt, 6)
        # answer=chain.run(input_documents=docs,question=prompt)
        with st.chat_message("assistant"):
            answer = st.write_stream(response_generator(prompt))
        st.session_state["messages"].append(['assistant',answer])

    else:
        st.write("请先上传文件")




