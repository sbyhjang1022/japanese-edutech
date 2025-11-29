# main.py
# Streamlit multipage app combining:
# 1) VR 일본 문화 탐방 웹앱
# 2) 메타버스 일본어 회화 허브
# 기능: 학습 기록 저장, 음성 녹음/업로드, 월드맵 허브, 관리자 모드

import streamlit as st
import os
import json
from datetime import datetime

st.set_page_config(page_title="미래형 일본어 학습 허브", layout="wide")

# --------------------------
# 유틸: 데이터 저장 경로
# --------------------------
DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

USER_LOG_PATH = os.path.join(DATA_DIR, "user_logs.json")
ADMIN_PASSWORD = "teacher123"  # 교사용 관리자 모드 비밀번호

# --------------------------
# 학습 기록 저장/로드
# --------------------------
def load_logs():
    if os.path.exists(USER_LOG_PATH):
        with open(USER_LOG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_logs(logs):
    with open(USER_LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)


def add_log(user, activity, detail):
    logs = load_logs()
    if user not in logs:
        logs[user] = []
    logs[user].append({
        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "activity": activity,
        "detail": detail,
    })
    save_logs(logs)

# --------------------------
# 메인 허브 (월드맵)
# --------------------------

def page_worldmap():
    st.title("🌏 일본어 미래학습 메인 허브")
    st.write("원하는 공간을 선택해 탐험하고 학습을 시작하세요.")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🗼 VR 일본 문화 탐방")
        st.write("일본의 도시·역사·문화 장소를 가상 체험합니다.")
        if st.button("VR 탐방 입장"):
            st.session_state["page"] = "vr"

    with col2:
        st.subheader("🏘️ 메타버스 일본어 회화 마을")
        st.write("역할 기반 일본어 회화를 장소별로 연습합니다.")
        if st.button("회화 마을 입장"):
            st.session_state["page"] = "meta"

    st.markdown("---")
    st.subheader("📚 학습 기록 확인")
    if st.button("내 학습 기록 보기"):
        st.session_state["page"] = "record"

    st.markdown("---")
    st.subheader("🔐 관리자 모드")
    if st.button("관리자 모드 이동"):
        st.session_state["page"] = "admin"

# --------------------------
# VR 일본 문화 탐방 페이지
# --------------------------

def page_vr():
    st.title("🗼 VR 일본 문화 탐방")

    place = st.selectbox("탐방할 장소를 선택하세요", [
        "도쿄 하라주쿠 거리", "교토 후시미이나리", "오사카 도톤보리", "홋카이도 오타루 운하"
    ])

    st.write(f"### {place} 가상 투어")
    st.write("(여기에 360° 이미지 URL 또는 iframe 삽입 가능 — 외부 설치 불필요)")

    st.markdown("---")
    st.write("### ✏️ 학습 메모 남기기")
    note = st.text_area("오늘 느낀 점")
    user = st.text_input("이름")

    if st.button("기록 저장") and user:
        add_log(user, "VR 탐방", f"{place} 탐방 — {note}")
        st.success("저장 완료!")

    st.markdown("---")
    st.write("### 🎤 음성 기록 업로드")
    audio_file = st.file_uploader("일본어 말하기 음성을 업로드하세요", type=["mp3", "wav", "m4a"])
    if audio_file and user:
        save_path = os.path.join(DATA_DIR, f"{user}_{audio_file.name}")
        with open(save_path, "wb") as f:
            f.write(audio_file.read())
        add_log(user, "VR 말하기 업로드", audio_file.name)
        st.success("음성 업로드 완료!")

# --------------------------
# 메타버스 일본어 회화 마을 페이지
# --------------------------

def page_meta():
    st.title("🏘️ 메타버스 일본어 회화 마을")
    st.write("장소를 선택해 역할 기반 회화를 연습하세요.")

    area = st.selectbox("장소 선택", [
        "카페", "역(駅)", "편의점", "식당", "관광 안내소"
    ])

    st.write(f"### {area} 역할 회화 미션")

    sample_dialogues = {
        "카페": "コーヒーを一つください。",
        "역(駅)": "東京駅までの切符をください。",
        "편의점": "このおにぎりはいくらですか。",
        "식당": "おすすめの料理は何ですか。",
        "관광 안내소": "地図をもらえますか。"
    }

    st.info(f"연습 문장 예시: {sample_dialogues[area]}")

    user = st.text_input("이름")

    st.markdown("---")
    st.write("### 🎤 음성 업로드로 말하기 제출")
    audio_file = st.file_uploader("음성 파일 업로드", type=["mp3", "wav", "m4a"])
    if audio_file and user:
        save_path = os.path.join(DATA_DIR, f"{user}_meta_{audio_file.name}")
        with open(save_path, "wb") as f:
            f.write(audio_file.read())
        add_log(user, "메타버스 회화 제출", f"{area} — {audio_file.name}")
        st.success("제출 완료!")

# --------------------------
# 학습 기록 페이지
# --------------------------

def page_record():
    st.title("📚 나의 학습 기록")
    user = st.text_input("이름 입력")

    if user:
        logs = load_logs()
        if user in logs:
            for item in logs[user]:
                st.write(f"- **{item['time']}** | {item['activity']} — {item['detail']}")
        else:
            st.warning("기록이 없습니다.")

# --------------------------
# 관리자 모드 페이지
# --------------------------

def page_admin():
    st.title("🔐 관리자 모드")
    pw = st.text_input("비밀번호", type="password")

    if pw == ADMIN_PASSWORD:
        st.success("관리자 인증 완료")

        logs = load_logs()
        for user, items in logs.items():
            st.write(f"## 👤 {user}")
            for item in items:
                st.write(f"- {item['time']} | {item['activity']} — {item['detail']}")
    else:
        st.info("비밀번호를 입력하세요.")

# --------------------------
# 페이지 라우팅
# --------------------------
if "page" not in st.session_state:
    st.session_state["page"] = "hub"

if st.session_state["page"] == "hub":
    page_worldmap()
elif st.session_state["page"] == "vr":
    page_vr()
elif st.session_state["page"] == "meta":
    page_meta()
elif st.session_state["page"] == "record":
    page_record()
elif st.session_state["page"] == "admin":
    page_admin()
