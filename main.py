import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI
import streamlit.components.v1 as components
import json

def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
     
    return "%d:%02d:%02d" % (hour, minutes, seconds)

def load_LLM(openai_api_key):
    """Logic for loading the chain you want to use should go here."""
    # Make sure your openai_api_key is set as an environment variable
    llm = OpenAI(temperature=.7, openai_api_key=openai_api_key)
    return llm

def gen_markdown_url(text,url):
    return f"[{text}]({url})"


def get_contents(video_id):
    with open(f"data/{video_id}.json","r") as fh:
        return json.load(fh)

def display_qa_content(vid_id,qa_info,prefix_index):
    st.markdown("---")
    question = qa_info["question"]
    vid_url = get_video_url(vid_id,qa_info["start"])
    q_start_time = convert(qa_info["start"])
    st.write(f" **[{prefix_index}. {question}]({vid_url})**")
    answer = "".join(qa_info["answer"])
    st.write(answer)


def qa_content_function(vid_id,qa,qa_text):
    prefix_index = int(qa_text.split(".")[0])-1
    qa_info = qa[prefix_index]
    question = qa_info["question"]
    vid_url = get_video_url(vid_id,qa_info["start"])
    q_start_time = convert(qa_info["start"])
    st.subheader(f" **[{question}]({vid_url})**")
    answer = "".join(qa_info["answer"])
    st.write(answer)
        

def chapter_content_function(vid_id,chapters,chap_text):
    prefix_index = int(chap_text.split(".")[0])-1
    chapter = chapters[prefix_index]
    chap_title = chapter["title"]
    vid_url = get_video_url(vid_id,chapter["start"])
    chap_start_time = convert(chapter["start"])
    st.subheader(f" **[{chap_start_time} - {chap_title}]({vid_url})**")
    chap_description = "".join(chapter["description"])
    st.write(chap_description)


def get_qa_contents(vid_id):
    with open(f"data/{video_id}_qa.json","r") as fh:
        return json.load(fh)

    
def show_qa(vid_id,qa_contents):
    st.markdown("Curated Question Answers from the video")
    qa = qa_contents["qa"]
    first = True
    q_titles = []

    for i,qa_info in enumerate(qa):        
        question = qa_info["question"]
        q_titles.append(f"{i+1}. {question}")
        
    question_sel = st.selectbox(
        "",
        q_titles)
    qa_content_function(vid_id,qa,question_sel)
    
def show_chapters(vid_id,video_contents):
    st.markdown("### Chapter Summary")
    chapters = video_contents["chapter_summary"]
    first = True
    chap_titles = []

    for i,chapter in enumerate(chapters):
        chap_title = chapter["title"]
        vid_url = get_video_url(vid_id,chapter["start"])
        chap_start_time = convert(chapter["start"])
        chap_titles.append(f"{i+1}. ({chap_start_time}) {chap_title} ")
        
    chapter_sel = st.selectbox(
        "",
        chap_titles)
    
    chapter_content_function(vid_id,chapters,chapter_sel)


def show_speakers(video_contents):
    st.markdown("## Speaker Summary")
    speakers = video_contents["speaker_summary"]
    sps = []
    for sp in speakers:
        sps.append(sp)
    s_tabs = st.tabs(sps)
    for i,s_tab in enumerate(s_tabs):
        s_tab.write("".join(speakers[sps[i]]))
    st.divider()

def get_video_url(vid_id,secs):
    return f"https://www.youtube.com/watch?v={video_id}&t={secs}"

title = "All-In Podcast GPT"
channel = "All-IN Podcast"
video_id = "mpC6c6iYji8"
video_url = get_video_url(video_id,0)
video_title = "E138: Presidential Candidate Vivek Ramaswamy in conversation with the Besties"

st.set_page_config(page_title=title, page_icon=":robot:")
st.header(title)
st.markdown(f" This page contains GPT generated output for {channel}  **{video_title}** ")
st.divider()

# video_display = get_youtube_window(video_id)
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("### Video Summary")
    video_contents = get_contents(video_id=video_id)
    st.markdown("".join(video_contents["summary"]))
    st.divider()
    show_speakers(video_contents=video_contents)
    st.divider()
    show_chapters(video_id,video_contents=video_contents)
    # qa_contents = get_qa_contents(video_id)   
    # st.divider()
    # show_qa(video_id,qa_contents)    
    
with col2:
    st.video(video_url) 
    st.markdown(video_title)
    st.divider()

st.divider()

st.markdown("## Curated Question Answers from the video")
st.markdown("== I will add dynamic Q and A in next video")
qa_contents = get_qa_contents(video_id)   
for i,qa in enumerate(qa_contents["qa"]):
    display_qa_content(video_id,qa,i)
