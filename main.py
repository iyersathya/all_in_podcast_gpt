import streamlit as st
from langchain import PromptTemplate
from langchain.llms import OpenAI
import streamlit.components.v1 as components
import json
import os


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
    llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
    return llm


def gen_markdown_url(text, url):
    return f"[{text}]({url})"


def get_contents(video_id):
    with open(f"data/{video_id}.json", "r") as fh:
        return json.load(fh)


def display_qa_content(vid_id, qa_info, prefix_index):
    st.markdown("---")
    question = qa_info["question"]
    vid_url = get_video_url(vid_id, qa_info["start"])
    q_start_time = convert(qa_info["start"])
    st.write(f" **[{prefix_index}. {question}]({vid_url})**")
    answer = "".join(qa_info["answer"])
    st.write(answer)


def qa_content_function(vid_id, qa, qa_text):
    prefix_index = int(qa_text.split(".")[0]) - 1
    qa_info = qa[prefix_index]
    question = qa_info["question"]
    vid_url = get_video_url(vid_id, qa_info["start"])
    q_start_time = convert(qa_info["start"])
    st.subheader(f" **[{question}]({vid_url})**")
    answer = "".join(qa_info["answer"])
    st.write(answer)


def chapter_content_function(vid_id, chapters, chap_text):
    prefix_index = int(chap_text.split(".")[0]) - 1
    chapter = chapters[prefix_index]
    chap_title = chapter["title"]
    vid_url = get_video_url(vid_id, chapter["start"])
    chap_start_time = convert(chapter["start"])
    st.markdown(
        f'[<p style="font-size:22px; color:gray;">{chap_start_time} - {chap_title}</p>]({vid_url}) ',
        unsafe_allow_html=True,
    )
    chap_description = "".join(chapter["description"])
    st.write(chap_description)


def get_qa_contents(output_path, video_id):
    with open(f"{output_path}/{video_id}/qa.json", "r") as fh:
        return json.load(fh)


def show_qa(output_path, video_id):
    st.markdown("Curated Question Answers from the video")
    with open(f"{output_path}/{video_id}/qa.json", "r") as fh:
        qa = json.load(fh)
        first = True
        q_titles = []

        for i, qa_info in enumerate(qa):
            question = qa_info["question"]
            q_titles.append(f"{i+1}. {question}")

        question_sel = st.selectbox("", q_titles)
        qa_content_function(video_id, qa, question_sel)


def show_chapters(
    output_path,
    video_id,
):
    st.markdown("### Chapter Summary")
    with open(f"{output_path}/{video_id}/chapter_summary.json", "r") as fh:
        chapters = json.load(fh)
        first = True
        chap_titles = []

        for i, chapter in enumerate(chapters):
            chap_title = chapter["title"]
            vid_url = get_video_url(video_id, chapter["start"])
            chap_start_time = convert(chapter["start"])
            chap_titles.append(f"{i+1}. ({chap_start_time}) {chap_title} ")

        chapter_sel = st.selectbox("", chap_titles)

        chapter_content_function(video_id, chapters, chapter_sel)


def show_speakers(output_path, video_id):
    st.markdown("## Speaker Summary")
    with open(f"{output_path}/{video_id}/speaker_summary.json", "r") as fh:
        speakers = json.load(fh)
        sps = []
        for sp in speakers:
            sps.append(sp)
        s_tabs = st.tabs(sps)
        for i, s_tab in enumerate(s_tabs):
            s_tab.write("".join(speakers[sps[i]]))
        st.divider()


def get_video_url(video_id, secs):
    return f"https://www.youtube.com/watch?v={video_id}&t={secs}"


title = "All-In Podcast GPT"
channel = "All-IN Podcast"
all_in_directory = f"data/all_in"

dir_list = [
    "hn-9ffDhGAo",
    "gpDzcCHERX4",
    "mpC6c6iYji8",
]
video_summary_info = {}
video_titles = []
for video_id_path in dir_list:
    with open(f"{all_in_directory}/{video_id_path}/video_summary.json", "r") as fh:
        video_summary = json.load(fh)
        video_title = video_summary["title"]
        video_summary_info[video_title] = {
            "video_id": video_id_path,
            "summary": video_summary["summary"],
        }
        video_titles.append(video_title)

st.set_page_config(page_title=title, page_icon=":robot:")
st.header(title)
st.markdown(
    f" This page contains GPT generated output for {channel} ",
    unsafe_allow_html=True,
)


def display_video_content(video_title):
    video_info = video_summary_info[video_title]
    video_id = video_info["video_id"]

    # video_display = get_youtube_window(video_id)
    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown("### Video Summary")
        st.markdown("".join(video_info["summary"]))
        st.divider()
        show_speakers(
            all_in_directory,
            video_id,
        )
        st.divider()
        show_chapters(
            all_in_directory,
            video_id,
        )

        st.divider()
        show_qa(all_in_directory, video_id)

    with col2:
        video_url = get_video_url(video_id, 0)
        st.video(video_url)
        st.markdown(video_title)
        st.divider()

    st.divider()

    st.markdown("## Curated Question Answers from the video")
    st.markdown(
        "<small>I will add support for dynamic question and answering in next video",
        unsafe_allow_html=True,
    )
    qa_contents = get_qa_contents(all_in_directory, video_id)
    for i, qa in enumerate(qa_contents):
        display_qa_content(video_id, qa, i)


episodes_selection = st.selectbox(
    "Select the episode for generating video details!!", video_titles, index=0
)
st.divider()
display_video_content(episodes_selection)

st.divider()
