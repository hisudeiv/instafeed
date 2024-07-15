import streamlit as st
import openai
import json
from datetime import datetime

# OpenAI API 키 설정
openai.api_key = "sk-proj-wRqqcy5cBmA8oF2OIZvCT3BlbkFJUnUYI8twFwIHreVRKmcR"

# 페이지 설정
st.set_page_config(
    page_title="InstaFeed",
    page_icon="📸",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 헤더 설정
header_html = """
    <style>
    .header {
        font-size: 4em;
        text-align: center;
        border-bottom: 5px solid;
        background-image: linear-gradient(to right, red, orange, yellow, green, blue, indigo, violet);
        background-clip: text;
        -webkit-background-clip: text;
        color: transparent;
    }
    </style>
    <div class="header">InstaFeed</div>
"""
st.markdown(header_html, unsafe_allow_html=True)

# 피드 작성 섹션
st.markdown('<h1 class="header-text">피드 작성</h1>', unsafe_allow_html=True)
if "feeds" not in st.session_state:
    st.session_state["feeds"] = []

# 챗GPT로 캡션 생성
content = st.text_area("피드 내용", key="content_input")
if st.button("챗GPT로 캡션 생성"):
    if content:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"이 내용으로 인스타그램 캡션을 생성해줘: {content}"}
            ]
        )
        generated_caption = response.choices[0]['message']['content'].strip()
        st.session_state["generated_caption"] = generated_caption
        st.success("캡션이 생성되었습니다.")
    else:
        st.warning("내용을 입력해주세요.")

# 피드 작성 폼
with st.form(key='feed_form', clear_on_submit=True):
    date_posted = st.date_input("게시 날짜", value=datetime.today())
    image_url = st.text_input("이미지 URL")
    caption = st.text_area("캡션", value=st.session_state.get("generated_caption", ""), height=200, key="caption_input")
    submit_button = st.form_submit_button('저장')
    if submit_button:
        if caption and date_posted and image_url:
            feed_data = {
                "content": caption,
                "date_posted": date_posted.strftime("%Y-%m-%d"),
                "image_url": image_url
            }
            st.session_state["feeds"].append(feed_data)
            st.success("피드가 저장되었습니다.")
            # 저장 후 생성된 캡션 초기화
            st.session_state["generated_caption"] = ""
            st.session_state["content_input"] = ""
            st.session_state["caption_input"] = ""
        else:
            st.warning("모든 정보를 입력해주세요.")

# 피드 목록 섹션
if st.session_state["feeds"]:
    st.markdown('<h1 class="header-text">피드 목록</h1>', unsafe_allow_html=True)
    for feed in st.session_state["feeds"]:
        st.image(feed["image_url"], width=300)
        st.write("게시 날짜: ", feed["date_posted"])
        st.write(feed["content"])

# JSON 데이터로 변환하여 출력
json_feed_data = json.dumps(st.session_state["feeds"], ensure_ascii=False, indent=4)
st.download_button("피드 데이터 다운로드", json_feed_data, file_name="feeds.json", mime="application/json")
