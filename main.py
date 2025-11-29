import streamlit as st

st.set_page_config(page_title="일본어 메타버스 허브", layout="centered")

st.title("🗾 일본어 메타버스 학습 허브")
st.write("원하는 공간을 선택하세요!")

col1, col2, col3 = st.columns(3)

with col1:
    st.image("vr.jpg")
    st.page_link("pages/01_VR_문화탐방.py", label="VR 일본 문화 탐방")

with col2:
    st.image("meta.jpg")
    st.page_link("pages/02_메타버스_회화마을.py", label="메타버스 일본어 회화")

with col3:
    st.image("record.jpg")
    st.page_link("pages/03_말하기_녹음제출.py", label="말하기 녹음 제출")

st.divider()
st.page_link("pages/04_관리자_모드.py", label="👩‍🏫 관리자 모드로 이동")
