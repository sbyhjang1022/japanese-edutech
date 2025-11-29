import streamlit as st

st.title("🏯 VR 일본 문화 탐방")

st.write("360° VR로 일본의 대표 지역을 둘러보세요.")

st.components.v1.html(open("vr_scene.html", "r", encoding="utf-8").read(), height=700)
