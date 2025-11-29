import streamlit as st
import os

st.title("👩‍🏫 관리자 모드 — 학생 말하기 기록")

DATA_DIR = "data"

if not os.path.exists(DATA_DIR):
    st.warning("아직 제출된 녹음 파일이 없습니다.")
else:
    files = os.listdir(DATA_DIR)
    audio_files = [f for f in files if f.endswith(".wav")]

    if not audio_files:
        st.info("아직 녹음 제출이 없습니다.")
    else:
        for file in audio_files:
            st.write(f"🎧 {file}")
            with open(os.path.join(DATA_DIR, file), "rb") as f:
                st.audio(f.read())
