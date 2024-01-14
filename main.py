import streamlit as st
import streamlit.components.v1 as components
import json
import os
import streamlit as st
from PIL import Image
import base64
import datetime


def get_formated_time(sec):
    return str(datetime.timedelta(seconds=sec))


def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "%d:%02d:%02d" % (hour, minutes, seconds)


# def load_LLM(openai_api_key):
#     """Logic for loading the chain you want to use should go here."""
#     # Make sure your openai_api_key is set as an environment variable
#     llm = OpenAI(temperature=0.7, openai_api_key=openai_api_key)
#     return llm


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
    # st.subheader(f" **[{question}]({vid_url})**")
    st.markdown(f" **[{question}]({vid_url})**")
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
    st.divider()
    st.markdown("Some interesting Question Answers from the video")
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
    st.markdown("### Speaker Summary")
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


def get_image_seconds(image_file_name):
    splits = image_file_name[:-4].split("_")
    if len(splits) > 0:
        return int(splits[len(splits) - 1])
    return -1


def get_image_base_64(image_file_path):
    with open(image_file_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode()


def get_image_file_list(image_dir, video_id):
    try:
        image_list = os.listdir(image_dir)
        # grab last 4 characters of the file name:
        return sorted(image_list, key=get_image_seconds)
    except:
        return None


def show_clips(video_id):
    image_dir = f"data/all_in/{video_id}/images"
    image_list = get_image_file_list(image_dir, video_id)
    # st.header("Interesting Content clips")
    # st.header("Clips")
    st.subheader("Interesting Content clips")
    if image_list:
        for index, image_fi in enumerate(image_list):
            seconds = get_image_seconds(image_fi)
            v_url = get_video_url(video_id, seconds)

            # encoded_img = get_image_base_64(f"{image_dir}/{image_fi}")
            # html = f"<a href='{v_url}'><img width=640 height=480 src='data:image/png;base64, {encoded_img}'></a>"
            # st.markdown(html, unsafe_allow_html=True)
            st.image(f"{image_dir}/{image_fi}")
            time_str = get_formated_time(seconds)
            st.markdown(f"### [Clip at {time_str}]({v_url})", unsafe_allow_html=True)
            # st.markdown(f"**Jump to {seconds}**")
            if index < len(image_list) - 1:
                st.divider()
    else:
        st.markdown("No content generated for this video")


title = "The All-In Podcast GPT"
channel = "**The All-IN Podcast**"
all_in_directory = f"data/all_in"

dir_list = [
    "EJEAq0Nsesc",
    "ID8T71m7Ics",
    "vT4ejH4ZfF4",
    "2OzpWVlt5Ok",
    "w85An9FVsb0",
    "IeKUcpU5-Xk",
    "4pLY1X46H1E",
    "1hh8lcoJ1NA",
    "3EFk40AbO94",
    "gFoHAl9MwZU",
    "7imwAJ0XcqQ",
    "65-x2YVUugE",
    "2RAfff-oMKw",
    "UZtQcnt12SM",
    "4spNsmlxWVQ",
    "X-Sb8sIi22g",
    "yHi7g_Tq3DU",
    "7InV_thsIv0",
    "t6ETJjVNP4M",
    "CfnF7dA-8UQ",
    "7TGJRzRSzL4",
    "F9cO3-MLHOM",
    "tKqJ5-kkUGk",
    "rid9NMSeqXQ",
    "odWe7qsrrGk",
    "F5UN2Yi_3AE",
    "gPiRgEVvlKE",
    "dlzobkV_CgU",
    "QAAfDQx8DDQ",
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
    f" This page is generated by running GPT on each episode of {channel}",
    unsafe_allow_html=True,
)


def display_video_content(video_title):
    video_info = video_summary_info[video_title]
    video_id = video_info["video_id"]

    # video_display = get_youtube_window(video_id)
    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown("### Video Summary")
        st.divider()
        st.markdown("".join(video_info["summary"]))
        show_speakers(
            all_in_directory,
            video_id,
        )
        show_chapters(
            all_in_directory,
            video_id,
        )

        st.divider()
        # show_qa(all_in_directory, video_id)

        # st.markdown("### Curated Question Answers from the video")
        # st.markdown(
        #     "<small>I will add support for dynamic question and answering in next video",
        #     unsafe_allow_html=True,
        # )
        # qa_contents = get_qa_contents(all_in_directory, video_id)
        # for i, qa in enumerate(qa_contents):
        #     display_qa_content(video_id, qa, i)

    with col2:
        video_url = get_video_url(video_id, 0)
        st.video(video_url)
        st.markdown(video_title)
        show_qa(all_in_directory, video_id)
        # seconds_list = []
        # seconds_int = []
        # for image_fi in image_list:
        #     seconds = get_image_seconds(image_fi)
        #     seconds_list.append(str(seconds) + " secs")
        #     seconds_int.append(seconds)

        # output = st.tabs(seconds_list)
        # for index, out in enumerate(output):
        #     with out:
        #         image_fi = image_list[index]
        #         secs = seconds_int[index]
        #         v_url = get_video_url(video_id, secs)
        #         encoded_img = get_image_base_64(f"{image_dir}/{image_fi}")
        #         html = f"<a href='{v_url}'><img width=320 height=240 src='data:image/png;base64, {encoded_img}'></a>"
        #         st.markdown(html, unsafe_allow_html=True)

    show_clips(video_id)
    st.divider()


episodes_selection = st.selectbox(
    "Select the episode for generating video details!!", video_titles, index=0
)
st.markdown(
    "[Go to Interesting content clips from this video](#interesting-content-clips)",
    unsafe_allow_html=True,
)
st.markdown(
    "Contact sathya.iyer@gmail.com for details about creating this GPT content",
    unsafe_allow_html=True,
)

st.divider()
display_video_content(episodes_selection)
