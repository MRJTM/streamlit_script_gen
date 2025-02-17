"""
剧本生成的app界面
"""
from utils import *
st.set_page_config(page_title="剧本创作", page_icon="📷",layout='wide')
st.sidebar.header("请创作你的剧本")
import io


if "openai_model" not in st.session_state:
    st.session_state['openai_model']="gpt-4o-mini-2024-07-18"
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# prompts
if "prompt_tmp" not in st.session_state:
    st.session_state['prompt_tmp']=open("prompts/prompt1.txt").read()
if "prompt_tmp_actor" not in st.session_state:
    st.session_state['prompt_tmp_actor']=open("prompts/prompt_actor.txt").read()
if "prompt_tmp_story_structure" not in st.session_state:
    st.session_state['prompt_tmp_story_structure']=open("prompts/prompt_story_structure.txt").read()
if "prompt_tmp_ep_summary" not in st.session_state:
    st.session_state['prompt_tmp_ep_summary']=open("prompts/prompt_ep_summary.txt").read()


st.title("VISAL AI剧本生成工具")

left_column, right_column = st.columns(2,gap='large',vertical_alignment='top')
with left_column:
    st.header("Step1：上传素材",divider="orange")
    # 通过radio来选择上传文件还是手动输入
    story_source=st.radio(label="素材来源",options=["文件","手动填写"],horizontal=True,index=0)

    if story_source=="文件":
        uploaded_file=st.file_uploader("Choose a file")
        if uploaded_file is not None and (not st.session_state.get("uploaded_file") or uploaded_file.name != st.session_state.uploaded_file.get("name")):
            # Update the session state
            st.session_state["uploaded_file"] = {"name": uploaded_file.name, "data": uploaded_file}
            path=os.path.join('..', uploaded_file.name)
            with open(path,'wb') as f:
                f.write(uploaded_file.getbuffer())

            current_vectorstore = load_file(path)
            st.text_area(label="文件内容",value=current_vectorstore)
            st.session_state["raw_story"]=current_vectorstore
            os.unlink(path)
    else:
        # 增加手动输入一些文字的功能
        user_input_text=st.text_area(label='请输入你的原始素材和故事',value="")
        if st.button(label='提交'):
            if user_input_text is not None and len(user_input_text)>2:
                st.session_state["raw_story"]=user_input_text[:40000]

    # Step2: 选择主题
    st.header("Step2：设置主题", divider="red")
    theme=st.text_input(label="请输入主题",value="爱情")
    if theme is not None and len(theme)>0:
        st.session_state["主题"]=theme

    st.write("当前主题：",theme)

    # Step3: 选择角色
    # prompt输入
    st.header("Step3：角色设定",divider="green")
    # 增加人数选择
    actor_num = st.text_input(label="请输入人物数量",value="2")

    if st.button(label="产生人物"):
        if "raw_story" in st.session_state:
            story=st.session_state['raw_story']

            # 组成prompt
            prompt=st.session_state['prompt_tmp_actor'].replace('aaaaa',story).replace('bbbbb',theme).replace('ccccc',actor_num)
            st.session_state["messages"].append(['user', prompt])

            # docs = current_vectorstore.similarity_search(prompt, 6)
            # answer=chain.run(input_documents=docs,question=prompt)
            with st.chat_message("assistant"):
                answer=st.write_stream(response_generator(prompt))
                json_parsed_res=parse_json_response(answer)
            st.session_state["messages"].append(['assistant',answer])
            st.session_state["故事梗概"]=json.dumps(json_parsed_res['故事梗概'],ensure_ascii=False)
            st.session_state["角色列表"]=json.dumps(json_parsed_res['角色列表'],ensure_ascii=False,indent=4)
        else:
            st.write("请先上传素材")


    # Step4: 确定故事大纲
    st.header("Step4：确定故事大纲", divider=True)
    if st.button(label='产生故事大纲'):
        raw_story=st.session_state['raw_story']
        theme=st.session_state['主题']
        story_summary=st.session_state['故事梗概']
        role_list=st.session_state['角色列表']
        prompt=st.session_state['prompt_tmp_story_structure'].replace('aaaaa',raw_story).replace('bbbbb',theme).replace('ccccc',story_summary).replace('ddddd',role_list)
        st.session_state["messages"].append(['user', prompt])
        with st.chat_message("assistant"):
            answer = st.write_stream(response_generator(prompt))
            json_parsed_res = parse_json_response(answer)
        st.session_state["messages"].append(['assistant', answer])
        st.session_state["故事大纲"]=json.dumps(json_parsed_res,ensure_ascii=False,indent=4)

    # Step5: 产生分集梗概
    st.header("Step5：产生分集梗概",divider=True)
    ep_num = st.text_input(label="请输入集数",value="2")

    if st.button(label='产生分集梗概'):
        raw_story=st.session_state['raw_story']
        theme=st.session_state['主题']
        story_summary=st.session_state['故事梗概']
        role_list=st.session_state['角色列表']
        story_outline=st.session_state['故事大纲']
        prompt=st.session_state['prompt_tmp_ep_summary'].replace('aaaaa',raw_story).replace('bbbbb',theme).replace('ccccc',story_summary).replace('ddddd',role_list).replace('eeeee',story_outline).replace('fffff',ep_num)
        st.session_state["messages"].append(['user', prompt])
        with st.chat_message("assistant"):
            answer = st.write_stream(response_generator(prompt))
            json_parsed_res = parse_json_response(answer)
        st.session_state["messages"].append(['assistant', answer])
        st.session_state["分集梗概"]=json.dumps(json_parsed_res,ensure_ascii=False,indent=4)
with right_column:
    st.header("剧本总览",divider="grey")
    total_script=""
    for key in ["主题","故事梗概","角色列表","故事大纲","分集梗概"]:
        if key in st.session_state:
            total_script+='[{}]\n'.format(key)+st.session_state[key]+'\n\n'
    st.text_area(label="剧本内容",value=total_script,height=1000)




